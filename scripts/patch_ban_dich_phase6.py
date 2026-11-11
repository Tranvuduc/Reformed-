#!/usr/bin/env python3
"""Phase 6.2/6.3 — Add the "Hoi sach nay" + Giscus sections to ban-dich pages.

Surgical patch (no full regen: tools/build-pages.py execs the other tools/*
builders, and authors_plus.py crashes on a full run). The section HTML is
the canonical ASK_GISCUS block from tools/build-pages.py, extracted from
that file so there is exactly one source of truth — the template change and
this patch can never drift apart.

- Inserts the two sections before the first <footer> of every
  ban-dich/*.html except ban-dich/index.html (a listing, not a book).
- Idempotent: pages already containing id="binh-luan" are skipped.
- /sach/ pages are NOT patched: they do not share the build-pages.py
  template and no generator owns them (build-pages.py line ~473), so a
  surgical patch there would silently drift from any future regen. They
  stay without the sections until a generator owns them.

Run from the repo root:  python3 scripts/patch_ban_dich_phase6.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

SRC = (ROOT / "tools/build-pages.py").read_text(encoding="utf-8")
m = re.search(r'ASK_GISCUS = """(.*?)"""\n', SRC, re.S)
if not m:
    print("FATAL: ASK_GISCUS block not found in tools/build-pages.py", file=sys.stderr)
    sys.exit(1)
BLOCK = m.group(1)


def main():
    patched, skipped, failed = 0, 0, []
    files = sorted((ROOT / "ban-dich").glob("*.html"))
    for f in files:
        if f.name == "index.html":
            skipped += 1
            continue
        text = f.read_text(encoding="utf-8")
        if 'id="binh-luan"' in text:
            skipped += 1
            continue
        slug = f.stem
        section = BLOCK.replace("{slug}", slug)
        i = text.find("<footer>")
        if i == -1:
            failed.append(str(f))
            continue
        f.write_text(text[:i] + section + text[i:], encoding="utf-8")
        patched += 1
    print(f"patched: {patched} | skipped (already patched / index): {skipped} | failed: {len(failed)}")
    for x in failed:
        print("  FAILED (no <footer>):", x)
    if failed:
        sys.exit(1)
    # Verify: every patched file still ends with </html> and carries both ids.
    bad = []
    for f in files:
        if f.name == "index.html":
            continue
        t = f.read_text(encoding="utf-8")
        if 'id="binh-luan"' not in t or 'id="hoi-sach"' not in t or not t.rstrip().endswith("</html>"):
            bad.append(str(f))
    print(f"verify: {len(files) - 1 - len(bad)}/{len(files) - 1} book pages carry both sections")
    if bad:
        print("  BAD:", *bad[:10], sep="\n  ")
        sys.exit(1)
    print("DONE")


if __name__ == "__main__":
    main()
