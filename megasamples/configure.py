#!/usr/bin/env python3
"""Choose the stack interactively -- engines, the engine x dataset matrix, consoles -- and write it.

  python3 -m megasamples configure [--out megasamples.yaml]
  python3 -m megasamples configure --defaults
  python3 -m megasamples configure --engines mysql --datasets quick --consoles landing,adminer

On a terminal this is a full-screen chooser (arrow keys, space to toggle, Enter to continue). With
`--defaults` or explicit flags, or when there is no terminal, it writes the configuration without
asking. Either way the result is `megasamples.yaml`, which `make run`, `make up` and every other
command read -- so the interactive session and a checked-in file are two ways to say the same thing.

The matrix shows, per dataset, its tier, what it costs to download and whether that download has
already been verified on this machine, so the choice is made with the bill in view.
"""
import argparse, os, sys

from megasamples import config as stack, consoles as console_registry, datasets as inventory, engines as engine_registry
from megasamples.paths import CONFIG, DOWNLOADS, rel

TIER_LABEL = {"core": "core — in the image", "core-medium": "core (medium) — in the image",
              "extended": "extended — opt-in, larger", "generated": "generated on this machine",
              "user-fetched": "user-fetched", "not-shipped": "loaders only; never redistributed"}
TIER_ORDER = ["core", "core-medium", "extended", "generated", "user-fetched", "not-shipped"]


# --- the model: what is chosen, and what it costs --------------------------------------------------
def fetched_bytes(name):
    """Bytes of this dataset's artifacts already verified in downloads/ (the .ok marker exists)."""
    sizes = inventory.manifest_sizes()
    have = 0
    for art in inventory.inventory()[name].get("artifacts") or []:
        if os.path.exists(os.path.join(DOWNLOADS, art + ".ok")):
            have += sizes.get(art, 0)
    return have


class Selection:
    def __init__(self, cfg=None):
        cfg = cfg or stack.load()
        known = engine_registry.names()
        self.engine_names = list(known)
        self.engines = [e for e in cfg.engines if e in known] or known[:1]
        self.matrix = {e: set(cfg.engines.get(e, [])) for e in known}
        self.consoles = set(cfg.consoles)
        self.ports = dict(cfg.ports)
        self.build = dict(cfg.build)
        self.downloads = dict(cfg.downloads)
        self.datasets = inventory.names()

    # engines
    def toggle_engine(self, name):
        if name in self.engines:
            if len(self.engines) > 1:
                self.engines.remove(name)
        else:
            self.engines.append(name)
            self.engines.sort(key=self.engine_names.index)

    # matrix
    def has(self, engine, dataset):
        return dataset in self.matrix.get(engine, set())

    def toggle(self, engine, dataset):
        cell = self.matrix.setdefault(engine, set())
        if dataset in cell:
            cell.discard(dataset)
        else:
            cell.add(dataset)

    def set_column(self, engine, names):
        self.matrix[engine] = set(names)

    def rows(self):
        """[(tier, [dataset...])] in display order."""
        out = []
        for tier in TIER_ORDER:
            names = inventory.by_tier(tier)
            if names:
                out.append((tier, names))
        return out

    def column_totals(self, engine):
        chosen = self.matrix.get(engine, set())
        total = sum(inventory.download_bytes(n) for n in chosen)
        have = sum(fetched_bytes(n) for n in chosen)
        return len(chosen), total, have

    # consoles
    def usable_consoles(self):
        return console_registry.usable(self.engines)

    def toggle_console(self, name):
        if name in self.consoles:
            self.consoles.discard(name)
        else:
            self.consoles.add(name)

    def to_raw(self):
        engines = {}
        for e in self.engines:
            chosen = self.matrix.get(e, set())
            if chosen == set(inventory.by_tier("core", "core-medium")):
                engines[e] = {"datasets": "core"}
            elif chosen == set(inventory.quick()):
                engines[e] = {"datasets": "quick"}
            elif chosen == set(inventory.names()):
                engines[e] = {"datasets": "all"}
            else:
                engines[e] = {"datasets": inventory.build_order(sorted(chosen))}
        usable = {c.name for c in self.usable_consoles()}
        consoles = [c.name for c in console_registry.CONSOLES if c.name in self.consoles and c.name in usable]
        return {"engines": engines, "consoles": consoles, "ports": self.ports,
                "build": self.build, "downloads": self.downloads}


def human_mb(n):
    return f"{n / 1e6:,.0f} MB" if n < 1e9 else f"{n / 1e9:,.1f} GB"


# --- the full-screen chooser ------------------------------------------------------------------------
def run_curses(sel):
    import curses

    def app(scr):
        curses.curs_set(0)
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_CYAN, -1)     # headings
        curses.init_pair(2, curses.COLOR_GREEN, -1)    # chosen
        curses.init_pair(3, curses.COLOR_YELLOW, -1)   # notes
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)   # cursor
        H, C, N, CUR = (curses.color_pair(i) for i in (1, 2, 3, 4))

        def put(y, x, text, attr=0):
            h, w = scr.getmaxyx()
            if 0 <= y < h and x < w:
                scr.addnstr(y, x, text, max(0, w - x - 1), attr)

        def screen_engines():
            pos = 0
            while True:
                scr.erase()
                put(0, 0, "sql-megasamples — configure   step 1 of 3: engines", H | curses.A_BOLD)
                put(1, 0, "Which database engines to build for. MySQL is the hub: every dataset is converted into")
                put(2, 0, "MySQL first and verified there; the other engines are ported from that corpus.")
                for i, name in enumerate(sel.engine_names):
                    e = engine_registry.get(name)
                    on = name in sel.engines
                    line = f" [{'x' if on else ' '}] {e.title:<12} {e.version:<8} {e.image}" + ("   hub" if e.hub else "")
                    put(4 + i, 0, line, CUR if i == pos else (C if on else 0))
                put(6 + len(sel.engine_names), 0, "↑/↓ move   space toggle   Enter continue   q quit", N)
                k = scr.getch()
                if k in (curses.KEY_UP, ord("k")):
                    pos = max(0, pos - 1)
                elif k in (curses.KEY_DOWN, ord("j")):
                    pos = min(len(sel.engine_names) - 1, pos + 1)
                elif k == ord(" "):
                    sel.toggle_engine(sel.engine_names[pos])
                elif k in (10, 13, curses.KEY_ENTER):
                    return True
                elif k in (ord("q"), 27):
                    return False

        def screen_matrix():
            rows = []                                   # (kind, tier_or_name)
            for tier, names in sel.rows():
                rows.append(("tier", tier))
                rows += [("dataset", n) for n in names]
            engines = sel.engines
            r, c, top = 1, 0, 0
            while True:
                scr.erase()
                h, w = scr.getmaxyx()
                put(0, 0, f"sql-megasamples — configure   step 2 of 3: datasets × engines", H | curses.A_BOLD)
                head = f" {'dataset':<24}{'download':>10}{'have':>6} "
                put(1, 0, head + "".join(f"{engine_registry.get(e).title:^12}" for e in engines), curses.A_BOLD)
                body_h = h - 6
                if r < top:
                    top = r
                if r >= top + body_h:
                    top = r - body_h + 1
                for i in range(top, min(len(rows), top + body_h)):
                    y = 2 + i - top
                    kind, item = rows[i]
                    if kind == "tier":
                        put(y, 0, f" {TIER_LABEL.get(item, item)}", H)
                        continue
                    have = fetched_bytes(item)
                    size = inventory.download_bytes(item)
                    q = " q" if inventory.inventory()[item].get("quick") else ""
                    line = f" {item + q:<24}{human_mb(size):>10}{('yes' if size and have >= size else ('part' if have else '')):>6} "
                    put(y, 0, line, CUR if i == r else 0)
                    x = len(line)
                    for j, e in enumerate(engines):
                        on = sel.has(e, item)
                        cell = f"{'[x]' if on else '[ ]':^12}"
                        attr = CUR if (i == r and j == c) else (C if on else 0)
                        put(y, x, cell, attr)
                        x += 12
                y = h - 4
                totals = "   ".join(
                    f"{engine_registry.get(e).title}: {n} datasets, {human_mb(t)} to download"
                    + (f" ({human_mb(hv)} already here)" if hv else "")
                    for e in engines for n, t, hv in [sel.column_totals(e)])
                put(y, 0, totals, N)
                put(y + 1, 0, "↑/↓ ←/→ move   space toggle   a row on all engines   c core   k quick   n none   A all", N)
                put(y + 2, 0, "for the current engine column: c/k/n/A   Enter continue   b back   q quit", N)
                k = scr.getch()
                if k in (curses.KEY_UP,):
                    r = max(0, r - 1)
                    while r > 0 and rows[r][0] == "tier":
                        r -= 1
                    if rows[r][0] == "tier":
                        r = 1
                elif k in (curses.KEY_DOWN,):
                    r = min(len(rows) - 1, r + 1)
                    while r < len(rows) - 1 and rows[r][0] == "tier":
                        r += 1
                elif k in (curses.KEY_LEFT,):
                    c = max(0, c - 1)
                elif k in (curses.KEY_RIGHT,):
                    c = min(len(engines) - 1, c + 1)
                elif k == curses.KEY_NPAGE:
                    r = min(len(rows) - 1, r + body_h)
                elif k == curses.KEY_PPAGE:
                    r = max(1, r - body_h)
                elif k == ord(" ") and rows[r][0] == "dataset":
                    sel.toggle(engines[c], rows[r][1])
                elif k == ord("a") and rows[r][0] == "dataset":
                    on = not sel.has(engines[c], rows[r][1])
                    for e in engines:
                        if sel.has(e, rows[r][1]) != on:
                            sel.toggle(e, rows[r][1])
                elif k == ord("c"):
                    sel.set_column(engines[c], inventory.by_tier("core", "core-medium"))
                elif k == ord("k"):
                    sel.set_column(engines[c], inventory.quick())
                elif k == ord("n"):
                    sel.set_column(engines[c], [])
                elif k == ord("A"):
                    sel.set_column(engines[c], inventory.names())
                elif k in (10, 13, curses.KEY_ENTER):
                    return "next"
                elif k == ord("b"):
                    return "back"
                elif k in (ord("q"), 27):
                    return "quit"

        def screen_consoles():
            usable = sel.usable_consoles()
            names = [c.name for c in console_registry.CONSOLES]
            pos = 0
            while True:
                scr.erase()
                put(0, 0, "sql-megasamples — configure   step 3 of 3: consoles", H | curses.A_BOLD)
                put(1, 0, "Web UIs that start beside the engines, already connected, read-only account first.")
                for i, name in enumerate(names):
                    con = console_registry.get(name)
                    ok = con in usable
                    on = name in sel.consoles and ok
                    engines = ", ".join(con.engines) or "the index page"
                    line = f" [{'x' if on else ' '}] {con.title:<14} {engines:<28} {con.note}"
                    if not ok:
                        line += "   (needs an engine not selected)"
                    put(3 + i, 0, line, CUR if i == pos else (C if on else (curses.A_DIM if not ok else 0)))
                y = 5 + len(names)
                put(y, 0, "Ports (127.0.0.1 only): " + "  ".join(
                    f"{k} {v}" for k, v in sel.ports.items() if k in sel.engines or k in sel.consoles), N)
                put(y + 2, 0, "↑/↓ move   space toggle   Enter write the file   b back   q quit", N)
                k = scr.getch()
                if k in (curses.KEY_UP, ord("k")):
                    pos = max(0, pos - 1)
                elif k in (curses.KEY_DOWN, ord("j")):
                    pos = min(len(names) - 1, pos + 1)
                elif k == ord(" ") and console_registry.get(names[pos]) in usable:
                    sel.toggle_console(names[pos])
                elif k in (10, 13, curses.KEY_ENTER):
                    return "next"
                elif k == ord("b"):
                    return "back"
                elif k in (ord("q"), 27):
                    return "quit"

        step = 0
        while True:
            if step == 0:
                if not screen_engines():
                    return False
                step = 1
            elif step == 1:
                got = screen_matrix()
                if got == "quit":
                    return False
                step = 0 if got == "back" else 2
            else:
                got = screen_consoles()
                if got == "quit":
                    return False
                if got == "back":
                    step = 1
                else:
                    return True

    return curses.wrapper(app)


# --- the line-based chooser, for terminals curses cannot drive --------------------------------------
def run_prompts(sel):
    def ask(question, default):
        answer = input(f"{question} [{default}]: ").strip()
        return answer or default

    print("sql-megasamples — configure (line mode)\n")
    names = ", ".join(sel.engine_names)
    chosen = ask(f"engines ({names})", ",".join(sel.engines))
    sel.engines = [e.strip() for e in chosen.split(",") if e.strip() in sel.engine_names] or sel.engines
    for e in sel.engines:
        spec = ask(f"datasets for {e}: core | quick | all | names", "core")
        try:
            sel.set_column(e, inventory.select([s.strip() for s in spec.split(",")] if "," in spec else spec))
        except KeyError as exc:
            print(f"  ! {exc}; keeping the previous choice")
    usable = [c.name for c in sel.usable_consoles()]
    chosen = ask(f"consoles ({', '.join(usable)})", ",".join(c for c in usable if c in sel.consoles))
    sel.consoles = {c.strip() for c in chosen.split(",") if c.strip() in usable}
    return True


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=CONFIG)
    ap.add_argument("--defaults", action="store_true", help="write the built-in default without asking")
    ap.add_argument("--engines", help="comma-separated; implies non-interactive")
    ap.add_argument("--datasets", help="selector or comma-separated names, applied to every engine named")
    ap.add_argument("--consoles", help="comma-separated")
    ap.add_argument("--line", action="store_true", help="prompt line by line instead of full screen")
    a = ap.parse_args(argv)

    sel = Selection()
    if a.defaults or a.engines or a.datasets or a.consoles:
        if a.engines:
            sel.engines = [e.strip() for e in a.engines.split(",")]
            unknown = [e for e in sel.engines if e not in sel.engine_names]
            if unknown:
                ap.error(f"unknown engine(s): {', '.join(unknown)}; known: {', '.join(sel.engine_names)}")
        if a.datasets:
            spec = [s.strip() for s in a.datasets.split(",")] if "," in a.datasets else a.datasets
            for e in sel.engines:
                sel.set_column(e, inventory.select(spec))
        if a.consoles:
            sel.consoles = {c.strip() for c in a.consoles.split(",")}
    else:
        interactive = sys.stdin.isatty() and sys.stdout.isatty()
        if not interactive:
            print("no terminal: writing the built-in default (use --engines/--datasets/--consoles to choose)")
        elif a.line:
            if not run_prompts(sel):
                return 1
        else:
            try:
                if not run_curses(sel):
                    print("configure: nothing written")
                    return 1
            except Exception as exc:  # noqa: BLE001 - a terminal curses cannot drive falls back to prompts
                print(f"full-screen mode unavailable ({exc}); prompting line by line\n")
                if not run_prompts(sel):
                    return 1

    raw = sel.to_raw()
    cfg = stack.Config(raw)
    problems = cfg.validate()
    for p in problems:
        print(f"  x {p}")
    if problems:
        return 2
    path = stack.write(raw, a.out)
    print(f"  . wrote {rel(path)}")
    for e, ds in cfg.engines.items():
        n, total, have = len(ds), sum(inventory.download_bytes(d) for d in ds), sum(fetched_bytes(d) for d in ds)
        print(f"      {e}: {n} datasets, {human_mb(total)} of downloads"
              + (f" ({human_mb(have)} already verified here)" if have else ""))
    print(f"      consoles: {', '.join(cfg.consoles) or 'none'}")
    print("  next: make run   (fetch, build, image)   then   make up")
    return 0


if __name__ == "__main__":
    sys.exit(main())
