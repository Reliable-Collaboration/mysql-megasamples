#!/usr/bin/env python3
"""Download and verify the upstream artifacts listed in manifest.yaml -- each exactly once.

  python3 -m megasamples fetch [dataset ...] [--id ID] [--jobs N] [--all] [--list] [--plain]

Every artifact is fetched from its `url`, then from each `mirrors` entry in turn, with curl
(`--fail --location --retry 5 -C -`); the file is verified against the manifest's `sha256` (and its
`size_bytes` when recorded) and a `downloads/<id>.ok` marker records the verified digest. A file
whose marker matches is never fetched again -- not on this run, not on the next -- so re-running a
build after an interruption costs nothing for what already arrived.

A monitor shows every transfer as it happens: bytes, rate, time left, then the verification pass,
then one permanent line per artifact. On a terminal the block redraws in place; with `--plain`, or
when output is not a terminal, it prints one line per state change instead. `--jobs` transfers run
at once (default: `downloads.concurrency` in megasamples.yaml, 3).

Hangs are treated as what they usually are on this project's build machines -- an IPv6 path that
never answers: a transfer that makes no progress for `--stall` seconds (120) is killed and retried
over IPv4, the fallback is recorded in the artifact's .meta.json, and `ipv4_first: true` in the
manifest skips straight to IPv4 for hosts known to do this (ARCHITECTURE.md section 2).

An artifact whose manifest `sha256` is empty has never been fetched here; the build refuses it
unless MEGASAMPLES_TRUST_FIRST_FETCH=1 is set, in which case the observed digest is written back
into the manifest and printed for the executor to record as a Verification in knowledge/log.md. An
artifact marked `manual: true` cannot be fetched by a build (a click-through, a share link): fetch
names the URL and the path, and verifies what the maintainer puts there.
"""
import argparse, hashlib, json, os, queue, re, subprocess, sys, threading, time

from megasamples.paths import DOWNLOADS, MANIFEST, ROOT

CURL_RETRYABLE = {7, 28, 35, 52, 55, 56, 92}  # connect, timeout, TLS, empty/recv/send, HTTP/2
STALL_RC = 28
_manifest_lock = threading.Lock()


# --- manifest ---------------------------------------------------------------------------------------
def load_manifest(path):
    import yaml
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    return data.get("artifacts") or []


def write_manifest_size(manifest_path, art_id, size):
    """Backfill size_bytes for an artifact whose entry left it at 0."""
    with _manifest_lock:
        lines = open(manifest_path, encoding="utf-8").read().split("\n")
        for i, line in enumerate(lines):
            if line.strip() == f"- id: {art_id}":
                for j in range(i, min(i + 12, len(lines))):
                    if lines[j].strip() == "size_bytes: 0":
                        lines[j] = lines[j].replace("size_bytes: 0", f"size_bytes: {size}")
                        open(manifest_path, "w", encoding="utf-8").write("\n".join(lines))
                        return True
                return False
    return False


def write_manifest_sha(manifest_path, art_id, digest):
    """Write a first-fetch digest back into the manifest without disturbing anything else."""
    with _manifest_lock:
        text = open(manifest_path, encoding="utf-8").read()
        block = re.search(r"(^  - id: " + re.escape(art_id) + r"$.*?)(?=^  - id: |\Z)", text, re.M | re.S)
        if not block:
            return False
        updated = re.sub(r'^(\s+sha256: )""\s*$', r'\1"' + digest + '"', block.group(1), count=1, flags=re.M)
        if updated == block.group(1):
            return False
        open(manifest_path, "w", encoding="utf-8").write(text[:block.start(1)] + updated + text[block.end(1):])
        return True


# --- one artifact -----------------------------------------------------------------------------------
class Job:
    """One artifact's progress, read by the monitor and written by its worker."""

    def __init__(self, art):
        self.art = art
        self.id = art["id"]
        self.size = int(art.get("size_bytes") or 0)
        self.state = "queued"       # queued | downloading | verifying | ok | cached | manual | failed
        self.done = 0               # bytes transferred or hashed so far
        self.rate = 0.0             # bytes per second over the last window
        self.detail = ""            # source in use, fallback notes, or the failure
        self.started = None
        self.finished = None
        self.verdict = ""
        self._window = (time.time(), 0)

    def progress(self, done):
        now = time.time()
        t0, b0 = self._window
        if now - t0 >= 0.5:
            self.rate = (done - b0) / (now - t0)
            self._window = (now, done)
        self.done = done

    @property
    def eta(self):
        if self.state == "downloading" and self.size and self.rate > 0:
            return max(0.0, (self.size - self.done) / self.rate)
        return None


def sha256_of(path, job=None):
    h = hashlib.sha256()
    done = 0
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
            done += len(chunk)
            if job is not None:
                job.progress(done)
    return h.hexdigest()


def curl(url, dest, ipv4, job, stall, timeout=1800):
    """One curl transfer, watched: returns (rc, write_out, stderr). Kills a transfer that stalls."""
    cmd = ["curl", "--fail", "--location", "--retry", "5", "--retry-all-errors",
           "--connect-timeout", "20", "-C", "-", "--silent", "--show-error",
           "--write-out", "%{http_code} %{size_download} %{time_total}",
           "-o", dest, url]
    if ipv4:
        cmd.insert(1, "-4")
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    started = last_change = time.time()
    last_size = -1
    while True:
        try:
            out, err = p.communicate(timeout=0.25)
            return p.returncode, out.strip(), err.strip()
        except subprocess.TimeoutExpired:
            pass
        size = os.path.getsize(dest) if os.path.exists(dest) else 0
        if size != last_size:
            last_size, last_change = size, time.time()
            job.progress(size)
        now = time.time()
        if now - last_change > stall:
            p.kill()
            p.communicate()
            return STALL_RC, "", f"no progress for {int(now - last_change)}s (stalled)"
        if now - started > timeout:
            p.kill()
            p.communicate()
            return STALL_RC, "", "curl exceeded the local timeout"


def download(job, dest_path, stall):
    """Try url then mirrors, each over the flagged stack and then forced IPv4. Returns meta or raises."""
    art = job.art
    attempts, sources = [], [art["url"]] + list(art.get("mirrors") or [])
    for source in sources:
        for ipv4 in ([True] if art.get("ipv4_first") else [False, True]):
            job.detail = f"{'IPv4 ' if ipv4 else ''}{source.split('//', 1)[-1].split('/', 1)[0]}"
            job._window = (time.time(), os.path.getsize(dest_path) if os.path.exists(dest_path) else 0)
            started = time.time()
            rc, out, err = curl(source, dest_path, ipv4, job, stall)
            attempts.append({"url": source, "ipv4": ipv4, "rc": rc, "detail": (err or out)[:200]})
            if rc == 0:
                return {"source": source, "ipv4_forced": ipv4, "curl": out,
                        "seconds": round(time.time() - started, 2), "attempts": attempts}
            if rc == STALL_RC and not ipv4:
                job.detail = "stalled; retrying over IPv4"
            if rc not in CURL_RETRYABLE and ipv4 is False:
                break  # a 404 will not be fixed by changing address family; go to the next mirror
    raise RuntimeError("all sources failed: " + "; ".join(
        f"{a['url']} ipv4={a['ipv4']} rc={a['rc']} {a['detail']}" for a in attempts))


def fetch_one(job, dest_root, manifest_path, trust_first, stall):
    """Fetch and verify one artifact, updating `job` as it goes. Returns the final state."""
    art, art_id = job.art, job.id
    dest = os.path.join(dest_root, art_id)
    ok_marker = dest + ".ok"
    expected = (art.get("sha256") or "").strip()
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    job.started = time.time()

    if os.path.exists(ok_marker) and os.path.exists(dest):
        recorded = open(ok_marker, encoding="utf-8").read().strip()
        if expected and recorded == expected:
            job.verdict = "verified earlier"
            return "cached"
        if not expected:
            job.verdict = "cached; manifest has no sha256"
            return "cached"
        job.detail = f"cached digest {recorded[:12]} != manifest {expected[:12]}, refetching"

    if art.get("manual"):
        if not os.path.exists(dest):
            raise RuntimeError(f"maintainer-supplied and not present.\n"
                               f"      Obtain it from: {art['url']}\n"
                               f"      Then put it at: {dest}")
        job.state = "verifying"
        digest, size = sha256_of(dest, job), os.path.getsize(dest)
        want_size = art.get("size_bytes") or 0
        if want_size and size != want_size:
            raise RuntimeError(f"size {size} != manifest size_bytes {want_size}")
        if expected and digest != expected:
            raise RuntimeError(f"sha256 {digest} != manifest {expected}")
        if not expected:
            if not trust_first:
                raise RuntimeError(f"manifest has no sha256; rerun with MEGASAMPLES_TRUST_FIRST_FETCH=1 to pin {digest}")
            write_manifest_sha(manifest_path, art_id, digest)
            job.detail = f"VERIFICATION for knowledge/log.md: sha256 {digest} size {size}"
        open(ok_marker, "w", encoding="utf-8").write(digest + "\n")
        job.verdict = "maintainer-supplied, " + ("verified" if expected else "digest recorded")
        return "manual"

    tmp = dest + ".part"
    if os.path.exists(tmp):
        os.remove(tmp)
    job.state = "downloading"
    meta = download(job, tmp, stall)
    job.state = "verifying"
    job.size = os.path.getsize(tmp)
    job._window = (time.time(), 0)
    digest, size = sha256_of(tmp, job), os.path.getsize(tmp)

    want_size = art.get("size_bytes") or 0
    if want_size and size != want_size:
        os.remove(tmp)
        raise RuntimeError(f"size {size} != manifest size_bytes {want_size}")
    if expected:
        if digest != expected:
            os.remove(tmp)
            raise RuntimeError(f"sha256 {digest} != manifest {expected}")
        job.verdict = "verified"
    elif trust_first:
        wrote = write_manifest_sha(manifest_path, art_id, digest)
        write_manifest_size(manifest_path, art_id, size)
        job.verdict = "first fetch, digest recorded" if wrote else "first fetch, MANIFEST NOT UPDATED"
        job.detail = f"VERIFICATION for knowledge/log.md: sha256 {digest} size {size}"
    else:
        os.remove(tmp)
        raise RuntimeError(f"manifest has no sha256; rerun with MEGASAMPLES_TRUST_FIRST_FETCH=1 "
                           f"to pin the observed digest {digest}")

    os.replace(tmp, dest)
    open(ok_marker, "w", encoding="utf-8").write(digest + "\n")
    meta.update({"id": art_id, "sha256": digest, "size_bytes": size,
                 "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    with open(dest + ".meta.json", "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2, sort_keys=True)
    if meta["ipv4_forced"] and not art.get("ipv4_first"):
        job.verdict += " (IPv4 fallback used)"
    return "fetched"


# --- the monitor ------------------------------------------------------------------------------------
def human(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1000 or unit == "GB":
            return f"{n:.1f} {unit}" if unit != "B" else f"{int(n)} B"
        n /= 1000
    return f"{n:.1f} GB"


def bar(frac, width=20):
    filled = int(round(frac * width))
    return "#" * filled + "-" * (width - filled)


def live_line(job, width):
    name = job.id if len(job.id) <= 40 else "…" + job.id[-39:]
    if job.state == "downloading":
        if job.size:
            frac = min(1.0, job.done / job.size)
            eta = job.eta
            tail = f"{human(job.done)}/{human(job.size)}  {human(job.rate)}/s" + \
                   (f"  {int(eta)}s left" if eta is not None else "")
            line = f"  {name:<40} [{bar(frac)}] {int(frac * 100):>3}%  {tail}"
        else:
            line = f"  {name:<40} {human(job.done)}  {human(job.rate)}/s"
    elif job.state == "verifying":
        frac = min(1.0, job.done / job.size) if job.size else 0
        line = f"  {name:<40} [{bar(frac)}] {int(frac * 100):>3}%  verifying sha256"
    else:
        line = f"  {name:<40} {job.state}"
    if job.detail:
        line += f"  {job.detail}"
    return line[:width]


def final_line(job, state):
    mark = {"fetched": "+", "cached": "=", "manual": "=", "failed": "x"}[state]
    if state == "failed":
        return f"  {mark} {job.id} FAILED: {job.detail}"
    took = f" in {job.finished - job.started:.1f}s" if state == "fetched" and job.finished else ""
    size = f" {human(job.size)}" if job.size else ""
    return f"  {mark} {job.id}{size}{took}, {job.verdict}"


class Monitor:
    def __init__(self, jobs, plain):
        self.jobs = jobs
        self.plain = plain or not sys.stdout.isatty()
        self.lock = threading.Lock()
        self.live_lines = 0
        self.width = 120
        try:
            self.width = os.get_terminal_size().columns
        except OSError:
            pass

    def _erase(self):
        if self.live_lines:
            sys.stdout.write(f"\x1b[{self.live_lines}A")
            for _ in range(self.live_lines):
                sys.stdout.write("\x1b[2K\n")
            sys.stdout.write(f"\x1b[{self.live_lines}A")
            self.live_lines = 0

    def announce(self, job, state):
        with self.lock:
            if not self.plain:
                self._erase()
            print(final_line(job, state))
            if job.detail.startswith("VERIFICATION"):
                print(f"      {job.detail}")
            sys.stdout.flush()

    def redraw(self):
        if self.plain:
            return
        with self.lock:
            self._erase()
            active = [j for j in self.jobs if j.state in ("downloading", "verifying")]
            queued = sum(1 for j in self.jobs if j.state == "queued")
            done = sum(j.done for j in active)
            lines = [live_line(j, self.width) for j in active]
            if active or queued:
                lines.append(f"  {len(active)} in flight, {queued} queued; "
                             f"{human(sum(j.rate for j in active))}/s")
            for line in lines:
                sys.stdout.write(line + "\n")
            self.live_lines = len(lines)
            sys.stdout.flush()


# --- orchestration ----------------------------------------------------------------------------------
def fetch(arts, dest_root=DOWNLOADS, manifest_path=MANIFEST, jobs=3, stall=120, plain=False,
          trust_first=None):
    """Fetch every artifact in `arts`. Returns (results, failures) where results maps state -> [ids]."""
    if trust_first is None:
        trust_first = os.environ.get("MEGASAMPLES_TRUST_FIRST_FETCH") == "1"
    work = [Job(a) for a in arts]
    monitor = Monitor(work, plain)
    q = queue.Queue()
    for j in work:
        q.put(j)
    results = {"fetched": [], "cached": [], "manual": [], "failed": []}
    failures = []
    rlock = threading.Lock()

    def worker():
        while True:
            try:
                job = q.get_nowait()
            except queue.Empty:
                return
            try:
                state = fetch_one(job, dest_root, manifest_path, trust_first, stall)
            except Exception as exc:  # noqa: BLE001 - reported per artifact; the build stops at the end
                state = "failed"
                job.detail = str(exc)
                with rlock:
                    failures.append(f"{job.id}: {exc}")
            job.finished = time.time()
            job.state = state
            with rlock:
                results[state].append(job.id)
            monitor.announce(job, state)
            q.task_done()

    total = sum(j.size for j in work)
    print(f"fetch: {len(work)} artifact(s), {human(total)} listed, into {os.path.relpath(dest_root, ROOT)}/"
          f"  ({jobs} at a time; verified files are never fetched twice)")
    threads = [threading.Thread(target=worker, daemon=True) for _ in range(max(1, min(jobs, len(work))))]
    for t in threads:
        t.start()
    while any(t.is_alive() for t in threads):
        monitor.redraw()
        time.sleep(0.25)
    monitor.redraw()
    fetched = [j for j in work if j.state == "fetched"]
    print(f"fetch: {len(results['fetched'])} fetched ({human(sum(j.size for j in fetched))}), "
          f"{len(results['cached']) + len(results['manual'])} already verified, {len(results['failed'])} failed")
    return results, failures


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("datasets", nargs="*", help="dataset names (default: every artifact, with --all)")
    ap.add_argument("--id", action="append", default=[], help="fetch one artifact by id")
    ap.add_argument("--all", action="store_true", help="every artifact in the manifest")
    ap.add_argument("--jobs", type=int, help="transfers at once (default: megasamples.yaml downloads.concurrency)")
    ap.add_argument("--stall", type=int, default=120, help="seconds without progress before a transfer is retried over IPv4")
    ap.add_argument("--plain", action="store_true", help="one line per event; no redrawing")
    ap.add_argument("--manifest", default=MANIFEST)
    ap.add_argument("--dest", default=DOWNLOADS)
    ap.add_argument("--list", action="store_true", help="list artifacts and exit")
    a = ap.parse_args(argv)

    arts = load_manifest(a.manifest)
    if a.list:
        for art in arts:
            print(f"{art['id']:<48} {human(art.get('size_bytes') or 0):>10}  {art.get('license', '-')}")
        return 0
    if a.id:
        arts = [x for x in arts if x["id"] in a.id]
    elif a.datasets:
        arts = [x for x in arts if x.get("dataset") in a.datasets]
    elif not a.all:
        ap.error("name datasets, --id an artifact, or pass --all")
    if not arts:
        if a.datasets and not a.id:
            # generated datasets, and those built from another dataset's download, own no artifact
            print(f"  . nothing to fetch for {' '.join(a.datasets)}: no artifacts of their own in the manifest")
            return 0
        print("no matching artifacts in the manifest")
        return 2
    jobs = a.jobs
    if not jobs:
        from megasamples import config as stack
        jobs = int(stack.load().downloads.get("concurrency", 3))
    _results, failures = fetch(arts, a.dest, a.manifest, jobs=jobs, stall=a.stall, plain=a.plain)
    for f in failures:
        print("ERROR", f)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
