#!/usr/bin/env python3
"""Check the Academy figures baked into hoc-vien/index.html and index.html
against the real lesson data (QR 1.0, RV-012). The pages are hand-maintained,
so this guard — not a human memory — keeps the numbers honest. Run from the
repo root: python3 scripts/check-academy-figures.py. Exit 1 on any mismatch.

Sources of truth:
- data/thirdmill-companions.json["companions"]: one entry per Thirdmill lesson
  with Vietnamese companion material (terms + study questions) -> 122.
- data/thirdmill-summaries.json["summaries"]: detailed Vietnamese summaries -> 7.
- data/academy.json["courses"][*]["lessons"]: local companion-track lessons -> 28.
- hoc-vien/khoa/*: one directory per Thirdmill course -> 14.
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def load(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8"))


companions = len(load("data/thirdmill-companions.json")["companions"])
summaries = len(load("data/thirdmill-summaries.json")["summaries"])
academy = load("data/academy.json")
lessons = sum(len(c.get("lessons", [])) for c in academy["courses"])
courses = len([d for d in (ROOT / "hoc-vien/khoa").iterdir() if d.is_dir()])
print(f"companions={companions} summaries={summaries} academy_lessons={lessons} courses={courses}")

errors = []


def expect(path, needle, what):
    txt = (ROOT / path).read_text(encoding="utf-8")
    if needle not in txt:
        errors.append(f"{path}: missing {what}: {needle!r}")


expect("hoc-vien/index.html",
       f"Cả {companions} bài của ba chứng chỉ đều có tài liệu đồng hành tiếng Việt",
       "companions sentence")
expect("hoc-vien/index.html",
       f"{summaries} bài (khóa FC1) có thêm bản tóm tắt chi tiết tiếng Việt",
       "summaries sentence")
expect("hoc-vien/index.html",
       f"3 khóa đồng hành địa phương của Reformed Vietnam có {lessons} bài học tiếng Việt",
       "academy lessons sentence")
expect("index.html",
       f"cả {companions} bài đều có thuật ngữ và câu hỏi học tập; {summaries} bài có bản tóm tắt chi tiết; 3 khóa đồng hành địa phương có {lessons} bài học",
       "homepage sentence")
expect("hoc-vien/index.html", f"14 khóa, {companions} bài học", "courses/lessons total")
# Guard against the old, wrong figure coming back:
for path in ("hoc-vien/index.html", "index.html"):
    txt = (ROOT / path).read_text(encoding="utf-8")
    if "28 bài tóm tắt" in txt or "28 trong 122 bài" in txt:
        errors.append(f"{path}: old wrong figure '28 bài tóm tắt' is back")

if errors:
    print("MISMATCH:")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("OK: baked Academy figures match the lesson data.")
