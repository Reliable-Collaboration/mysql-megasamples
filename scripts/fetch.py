#!/usr/bin/env python3
"""Download and verify the upstream artifacts listed in manifest.yaml.

Usage:
  python3 scripts/fetch.py                     # every artifact
  python3 scripts/fetch.py sakila chinook      # by dataset
  python3 scripts/fetch.py --id sakila/sakila-db.zip
  python3 scripts/fetch.py --list

Each artifact is fetched from `url`, falling back to each entry of `mirrors` in order. A download is verified
against the manifest's `sha256` (and `size_bytes` when non-zero); a verified file is recorded by a
`<id>.ok` marker so repeated runs are cheap and offline-safe.

An artifact whose manifest `sha256` is empty has never been fetched here. The build refuses to accept it
unless MEGASAMPLES_TRUST_FIRST_FETCH=1 is set, in which case the observed digest is written back into the
manifest and a line is printed for the executor to record as a Verification in knowledge/log.md.

IPv6: `ipv4_first: true` forces `curl -4` for hosts known to hang. Independently of the flag, a connect or
transfer failure is retried once with `-4` and the fallback is recorded in the artifact's .meta.json, so a
host that starts failing over IPv6 keeps working without a manifest edit (PLAN.md section 2.6).
"""
import argparse, hashlib, json, os, re, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURL_RETRYABLE = {7, 28, 35, 52, 55, 56, 92}  # connect, timeout, TLS, empty/recv/send, HTTP/2


def load_manifest(path):
    import yaml
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    return data.get("artifacts") or []


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def curl(url, dest, ipv4, timeout=1800):
    cmd = ["curl", "--fail", "--location", "--retry", "5", "--retry-all-errors",
           "--connect-timeout", "20", "-C", "-", "--silent", "--show-error",
           "--write-out", "%{http_code} %{size_download} %{time_total}",
           "-o", dest, url]
    if ipv4:
        cmd.insert(1, "-4")
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return 28, "", "curl exceeded the local timeout"
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def download(art, dest_path):
    """Try url then mirrors, each with the flagged stack and then forced IPv4. Returns meta or raises."""
    attempts, sources = [], [art["url"]] + list(art.get("mirrors") or [])
    for source in sources:
        for ipv4 in ([True] if art.get("ipv4_first") else [False, True]):
            started = time.time()
            rc, out, err = curl(source, dest_path, ipv4)
            attempts.append({"url": source, "ipv4": ipv4, "rc": rc, "detail": (err or out)[:200]})
            if rc == 0:
                return {"source": source, "ipv4_forced": ipv4, "curl": out,
                        "seconds": round(time.time() - started, 2), "attempts": attempts}
            if rc not in CURL_RETRYABLE and ipv4 is False:
                break  # a 404 will not be fixed by changing address family; go to the next mirror
    raise RuntimeError("all sources failed:\n  " + "\n  ".join(
        f"{a['url']} ipv4={a['ipv4']} rc={a['rc']} {a['detail']}" for a in attempts))


def write_manifest_sha(manifest_path, art_id, digest):
    """Write a first-fetch digest back into the manifest without disturbing anything else."""
    text = open(manifest_path, encoding="utf-8").read()
    block = re.search(r"(^  - id: " + re.escape(art_id) + r"$.*?)(?=^  - id: |\Z)", text, re.M | re.S)
    if not block:
        return False
    updated = re.sub(r'^(\s+sha256: )""\s*$', r'\1"' + digest + '"', block.group(1), count=1, flags=re.M)
    if updated == block.group(1):
        return False
    open(manifest_path, "w", encoding="utf-8").write(text[:block.start(1)] + updated + text[block.end(1):])
    return True


def fetch_one(art, dest_root, manifest_path, trust_first):
    art_id = art["id"]
    dest = os.path.join(dest_root, art_id)
    ok_marker = dest + ".ok"
    expected = (art.get("sha256") or "").strip()
    os.makedirs(os.path.dirname(dest), exist_ok=True)

    if os.path.exists(ok_marker) and os.path.exists(dest):
        recorded = open(ok_marker, encoding="utf-8").read().strip()
        if expected and recorded == expected:
            print(f"  = {art_id} (verified, cached)")
            return "cached"
        if not expected:
            print(f"  = {art_id} (cached; manifest has no sha256)")
            return "cached"
        print(f"  ! {art_id} cached digest {recorded[:12]} != manifest {expected[:12]}, refetching")

    # An artifact behind a login, a click-through or a share link with no static URL cannot be
    # fetched by a build. The maintainer supplies it once; this verifies what they supplied and
    # never reaches the network. See PLAN.md section 2.5.
    if art.get("manual"):
        if not os.path.exists(dest):
            raise RuntimeError(
                f"{art_id} is maintainer-supplied and is not present.\n"
                f"  Obtain it from: {art['url']}\n"
                f"  Then put it at: {dest}")
        digest, size = sha256_of(dest), os.path.getsize(dest)
        want_size = art.get("size_bytes") or 0
        if want_size and size != want_size:
            raise RuntimeError(f"{art_id}: size {size} != manifest size_bytes {want_size}")
        if expected and digest != expected:
            raise RuntimeError(f"{art_id}: sha256 {digest} != manifest {expected}")
        if not expected:
            if not trust_first:
                raise RuntimeError(f"{art_id}: manifest has no sha256; rerun with "
                                   f"MEGASAMPLES_TRUST_FIRST_FETCH=1 to pin {digest}")
            write_manifest_sha(manifest_path, art_id, digest)
            print(f"  VERIFICATION for knowledge/log.md: {art_id} sha256 {digest} size {size}")
        open(ok_marker, "w", encoding="utf-8").write(digest + "\n")
        print(f"  = {art_id} (maintainer-supplied, {'verified' if expected else 'digest recorded'})")
        return "manual"

    tmp = dest + ".part"
    if os.path.exists(tmp):
        os.remove(tmp)
    meta = download(art, tmp)
    digest, size = sha256_of(tmp), os.path.getsize(tmp)

    want_size = art.get("size_bytes") or 0
    if want_size and size != want_size:
        os.remove(tmp)
        raise RuntimeError(f"{art_id}: size {size} != manifest size_bytes {want_size}")

    if expected:
        if digest != expected:
            os.remove(tmp)
            raise RuntimeError(f"{art_id}: sha256 {digest} != manifest {expected}")
        verdict = "verified"
    elif trust_first:
        wrote = write_manifest_sha(manifest_path, art_id, digest)
        verdict = "first fetch, digest recorded" if wrote else "first fetch, MANIFEST NOT UPDATED"
        print(f"  VERIFICATION for knowledge/log.md: {art_id} sha256 {digest} size {size}")
    else:
        os.remove(tmp)
        raise RuntimeError(f"{art_id}: manifest has no sha256; rerun with MEGASAMPLES_TRUST_FIRST_FETCH=1 "
                           f"to pin the observed digest {digest}")

    os.replace(tmp, dest)
    open(ok_marker, "w", encoding="utf-8").write(digest + "\n")
    meta.update({"id": art_id, "sha256": digest, "size_bytes": size,
                 "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    with open(dest + ".meta.json", "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2, sort_keys=True)
    fallback = " (IPv4 fallback used)" if meta["ipv4_forced"] and not art.get("ipv4_first") else ""
    print(f"  + {art_id} {size} bytes in {meta['seconds']}s, {verdict}{fallback}")
    return "fetched"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("datasets", nargs="*", help="dataset names (default: all)")
    ap.add_argument("--id", action="append", default=[], help="fetch one artifact by id")
    ap.add_argument("--manifest", default=os.path.join(ROOT, "manifest.yaml"))
    ap.add_argument("--dest", default=os.path.join(ROOT, "downloads"))
    ap.add_argument("--list", action="store_true", help="list artifacts and exit")
    a = ap.parse_args()

    arts = load_manifest(a.manifest)
    if a.list:
        for art in arts:
            print(f"{art['id']:<40} {art.get('size_bytes') or '?':>12}  {art.get('license', '-')}")
        return
    if a.id:
        arts = [x for x in arts if x["id"] in a.id]
    elif a.datasets:
        arts = [x for x in arts if x.get("dataset") in a.datasets]
    if not arts:
        print("no matching artifacts in the manifest"); sys.exit(2)

    trust_first = os.environ.get("MEGASAMPLES_TRUST_FIRST_FETCH") == "1"
    print(f"fetching {len(arts)} artifact(s) into {a.dest}")
    failures = []
    for art in arts:
        try:
            fetch_one(art, a.dest, a.manifest, trust_first)
        except Exception as exc:  # noqa: BLE001 - reported per artifact, build stops at the end
            failures.append(f"{art['id']}: {exc}")
            print(f"  x {art['id']} FAILED")
    for f in failures:
        print("ERROR", f)
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
