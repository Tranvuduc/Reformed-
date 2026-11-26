#!/usr/bin/env python3
"""Check the frozen unified-shell constants in tools/build-pages.py and
tools/build-vn-books.py match hub.html's <header class="site"> /
<footer class="site"> (as extracted by scripts/hub_page.py).

Why frozen constants exist at all: the round pipeline's gen4.py extracts
page() from build-pages.py by AST closure and only pulls in top-level
def/assign nodes — a live `from hub_page import ...` would be silently
absent and staging would fail with NameError. So the shell markup lives as
string constants in the builders, and THIS script is the drift guard: run
it whenever hub.html's header/footer changes (and before merging any
template change). Exit 0 = in sync; exit 1 = drift, with the differing
constant named.

Run from the repo root: python3 scripts/check_shell_sync.py
"""
import pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hub_page import header as HUB_HEADER, footer as HUB_FOOTER

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _const(src, name):
    m = re.search(rf'^{name} = """(.*?)"""$', src, re.M | re.S)
    if not m:
        print(f"FAIL: {name} not found as a triple-quoted constant", file=sys.stderr)
        sys.exit(1)
    return m.group(1)


def main():
    bad = []
    for rel, names in (("tools/build-pages.py", ("_SHELL_HEADER", "_SHELL_FOOTER")),
                       ("tools/build-vn-books.py", ("SHELL_HEADER", "SHELL_FOOTER"))):
        src = (ROOT / rel).read_text(encoding="utf-8")
        for name, want in ((names[0], HUB_HEADER), (names[1], HUB_FOOTER)):
            got = _const(src, name)
            if got != want:
                bad.append(f"{rel}:{name} differs from hub.html ({len(got)}B vs {len(want)}B)")
    if bad:
        print("SHELL SYNC FAIL:", file=sys.stderr)
        for b in bad:
            print("  " + b, file=sys.stderr)
        print("Update the constants from hub.html (via scripts/hub_page.py extraction), then re-run.", file=sys.stderr)
        sys.exit(1)
    print(f"shell sync OK: header {len(HUB_HEADER)}B, footer {len(HUB_FOOTER)}B match hub.html in both builders")


if __name__ == "__main__":
    main()
