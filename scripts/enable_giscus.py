#!/usr/bin/env python3
"""Enable Giscus comments on the ban-dich book pages (Phase 6.3, step 2).

Step 1 (repo owner, web UI — cannot be done from the CLI) must be done
first: install the Giscus GitHub App on Tranvuduc/Reformed- at
https://github.com/apps/giscus (choose "Only select repositories" and
pick Tranvuduc/Reformed-). GitHub Discussions is already enabled on the
repo, and the "General" discussion category already exists.

This script:
  1. Verifies the app is actually installed, by asking the giscus API for
     a discussion on this repo. If the API answers "giscus is not installed
     on this repository", it refuses to change anything and prints step 1.
  2. Uncomments the Giscus <script> in every ban-dich/*.html page and in
     the tools/build-pages.py template, and updates the visible note in
     the comments section (it no longer says "coming soon").
  3. Prints the files changed. Commit + push afterwards to go live.

Run from the repo root:  python3 scripts/enable_giscus.py
"""
import json
import pathlib
import re
import sys
import urllib.error
import urllib.request
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent

API = ("https://giscus.app/api/discussions?repo=Tranvuduc%2FReformed-"
       "&category=General&mapping=pathname&term=%2Fban-dich%2Ftest.html"
       "&strict=0&reactionsEnabled=1&emitMetadata=0&inputPosition=bottom"
       "&theme=light&lang=vi")

NOTE_OLD = ("Bình luận trên trang sách sẽ mở sau khi tính năng này được bật. "
            "Trong lúc chờ, bạn có thể góp ý qua liên kết “Báo lỗi bản dịch” ở cuối trang. "
            "Bình luận do độc giả viết sẽ hiển thị công khai; "
            "quản trị viên kiểm duyệt và có thể gỡ bình luận không phù hợp.")
NOTE_NEW = ("Bình luận bên dưới dùng tài khoản GitHub của bạn. "
            "Bình luận hiển thị công khai; "
            "quản trị viên kiểm duyệt và có thể gỡ bình luận không phù hợp.")

BLOCK_RE = re.compile(r"<!-- GISCUS-OFF\n(.*?)GISCUS-OFF-END -->\n?", re.S)


def uncomment(text):
    def repl(m):
        lines = [ln for ln in m.group(1).splitlines()
                 if ln.strip().startswith('<script src="https://giscus.app/client.js"')]
        if len(lines) != 1:
            raise ValueError("expected exactly one giscus script line in the commented block")
        return lines[0] + "\n"
    return BLOCK_RE.sub(repl, text)


def main():
    print("Checking whether the Giscus app is installed on Tranvuduc/Reformed- ...")
    req = urllib.request.Request(API, headers={
        "User-Agent": "Mozilla/5.0 (compatible; ReformedVietnam-enable-giscus/1.0)",
        "Accept": "application/json",
    })
    data = None
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        # The giscus API reports "not installed" as HTTP 403 WITH a JSON
        # error body — that is the signal, not a network failure.
        try:
            data = json.loads(e.read().decode("utf-8"))
        except Exception:  # noqa: BLE001 — unreadable body = unverifiable
            data = None
        if not isinstance(data, dict) or "error" not in data:
            print(f"Giscus API returned HTTP {e.code} with no usable error body; refusing to change anything.", file=sys.stderr)
            print("Check your network, or install the app first: https://github.com/apps/giscus", file=sys.stderr)
            sys.exit(1)
    except Exception as e:  # noqa: BLE001 — network failure = cannot verify
        print(f"Could not reach the giscus API ({e}); refusing to change anything.", file=sys.stderr)
        print("Check your network, or install the app first: https://github.com/apps/giscus", file=sys.stderr)
        sys.exit(1)
    if isinstance(data, dict) and "error" in data:
        print(f"Giscus API says: {data['error']}", file=sys.stderr)
        print("The Giscus app is NOT installed yet. Do step 1 first:", file=sys.stderr)
        print("  https://github.com/apps/giscus  -> Install -> Only select repositories -> Tranvuduc/Reformed-", file=sys.stderr)
        print("Then re-run this script.", file=sys.stderr)
        sys.exit(1)
    print("Giscus app is installed. Uncommenting the widget ...")

    targets = [ROOT / "tools/build-pages.py"] + sorted((ROOT / "ban-dich").glob("*.html"))
    changed, already, untouched = 0, 0, 0
    for f in targets:
        text = f.read_text(encoding="utf-8")
        if "GISCUS-OFF" not in text:
            already += 1
            continue
        new = uncomment(text)
        if NOTE_OLD in new:
            new = new.replace(NOTE_OLD, NOTE_NEW)
        f.write_text(new, encoding="utf-8")
        changed += 1
    print(f"uncommented: {changed} | already enabled / no block: {already} | untouched: {untouched}")
    print("DONE — commit and push to go live (one batched push).")


if __name__ == "__main__":
    main()
