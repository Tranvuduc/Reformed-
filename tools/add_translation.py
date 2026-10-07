#!/usr/bin/env python3
"""Add a completed translation to translations/index.json for the build pipeline.
Usage: python3 tools/add_translation.py <id> <file> <title> <orig> <author> [by]
Example: python3 tools/add_translation.py spurgeon/grace spurgeon-grace.txt "Tất Cả Bởi Ân Điển" "All of Grace" "C. H. Spurgeon"
"""
import json, os, sys

if len(sys.argv) < 6:
    print(__doc__); sys.exit(1)

bid, bfile, title, orig, author = sys.argv[1:6]
by = sys.argv[6] if len(sys.argv) > 6 else "Muse"

idx_path = "translations/index.json"
idx = json.load(open(idx_path, encoding="utf-8"))

# check file exists
if not os.path.exists(f"translations/{bfile}"):
    print(f"ERROR: translations/{bfile} not found"); sys.exit(1)

# check not already present
for e in idx:
    if e["id"] == bid:
        print(f"Already in index: {bid}"); sys.exit(0)

entry = {
    "id": bid,
    "file": bfile,
    "title": title,
    "orig": orig,
    "author": author,
    "by": by,
    "reviewed": False
}
idx.append(entry)
json.dump(idx, open(idx_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"Added: {bid} -> {bfile}")
print(f"Next: python3 tools/build-pages.py (rebuilds ban-dich/ + txt/ + vi-books.json)")
