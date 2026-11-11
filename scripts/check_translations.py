#!/usr/bin/env python3
"""Phase 5.2 — Translation quality checker (Kiểm tra chất lượng bản dịch).

Reads every file in translations/*.txt once and checks for common defects:

  * missing first-line "AI, chưa duyệt" header (new-round convention;
    most bulk-imported files predate it — reported, not auto-fixed)
  * missing TRANSLATION STATUS / TERMINOLOGY ISSUES footer
  * [NEEDS REVIEW] markers (counted, not defects by themselves)
  * markdown artefacts in plain text (backticks, markdown links,
    blockquotes, raw HTML tags)
  * untranslated English passages (heuristic: long mostly-ASCII lines
    containing common English words; meta lines, source lines and
    NEEDS REVIEW notes are excluded)
  * locked-term violations in the site's own voice: "công bình",
    "Kinh Lạy Cha", "Kinh Tin Kính", "nước Đức Chúa Trời".
    NOTE: "công bình" and "nước Đức Chúa Trời" are legitimate INSIDE
    quoted 1934 verse text, so those counts need manual review — the
    checker reports them, it does not judge them.
  * structural: empty/tiny files, files with no title line
  * catalogue cross-check: index entries whose file is missing, and
    txt files with no index entry

Output:
  * data/quality-report.json — machine-readable summary (the public
    tracker page reads this at build time)
  * scripts/quality-report-YYYY-MM-DD.md — full findings with per-file
    lists (top 20 per category)

This script NEVER edits translations. Anything it finds is a report;
fixes happen by human decision in later rounds.
"""
import datetime
import glob
import json
import os
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
TODAY = datetime.date.today().isoformat()

ENGLISH_WORDS = set("""the and of to in is you that it he was for on are as with his they at be this
have from or one had by word but not what all were we when your can said there use an each which she do how
their if will up other about out many then them these so some her would make like him into time has look two
more write go see number no way could people my than first water been call who oil its now find long down day
did get come made may part over new sound take only little work know place year live me back give most very
after thing our just name good sentence man think say great where help through much before line right too mean
old any same tell boy follow came want show also around form three small set put end does another well large
must big even such because turn here why ask went men read need land different home us move try kind hand
picture again change off play spell air away animal house point page letter mother answer found study still
learn should world high every near add food between own below country plant last school father keep tree never
start city earth eye light thought head under story saw left few while along might close something seem next
hard open example begin life always those both paper together got group often run""".split())

MD_LINK_RE = re.compile(r"\[[^\]]+\]\(https?://[^)]+\)")
HTML_TAG_RE = re.compile(r"<[a-zA-Z/][^>]{0,60}>")


def is_english_line(line):
    """A body line that looks like untranslated English."""
    s = line.strip()
    if len(s) < 20:
        return False
    words = re.findall(r"[A-Za-z]+", s)
    if len(words) < 4:
        return False
    letters = [c for c in s if c.isalpha()]
    if not letters:
        return False
    ascii_ratio = sum(1 for c in letters if ord(c) < 128) / len(letters)
    if ascii_ratio < 0.85:
        return False
    hits = sum(1 for w in words if w.lower() in ENGLISH_WORDS)
    return hits >= 2


def norm_file(f):
    """Index 'file' values may carry a leading space and/or a
    'translations/' prefix — compare basenames."""
    return (f or "").strip().rsplit("/", 1)[-1]


def slug_words(name):
    """Content words of a txt basename, minus numeric/catalogue prefixes
    ('003-', 'mg1-1094-', '1000-418-' ...). Used only for the
    likely-same-work heuristic for unindexed files."""
    base = name[:-4] if name.endswith(".txt") else name
    parts = [p for p in re.split(r"[-_]", base) if p and not p.isdigit()
             and not re.match(r"^(mg|ai|rv|w|arch|bim|d8bk)\d*$", p)]
    return set(parts)


def check_file(path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    chars = len(text)
    first = next((ln.strip() for ln in lines if ln.strip()), "")
    r = {
        "file": path.name, "chars": chars, "lines": len(lines),
        "header": first == "AI, chưa duyệt",
        "footer_status": "TRANSLATION STATUS" in text,
        "footer_terms": "TERMINOLOGY ISSUES" in text,
        "needs_review": text.count("[NEEDS REVIEW"),
        "english_lines": 0, "english_sample": [],
        "cong_binh": 0, "kinh_lay_cha": 0, "kinh_tin_kinh": 0,
        "nuoc_dct": 0, "backtick": 0, "md_link": 0, "blockquote": 0,
        "html_tag": 0, "has_title": False, "tiny": chars < 200,
    }
    # Title: a "# ..." heading, or (new format) the line after the
    # "AI, chưa duyệt" header; old files put the title on line 1.
    for ln in lines[:6]:
        if ln.startswith("# ") and len(ln.strip()) > 3:
            r["has_title"] = True
    if first == "AI, chưa duyệt":
        for ln in lines[1:5]:
            if ln.strip() and not ln.startswith("#"):
                r["has_title"] = True
    if not r["has_title"] and first and not first.startswith("AI,"):
        r["has_title"] = True  # old files: plain title on line 1

    in_footer = False
    for ln in lines:
        if "TRANSLATION STATUS:" in ln:
            in_footer = True
        if in_footer:
            continue
        low = ln.lower()
        if "công bình" in low:
            r["cong_binh"] += low.count("công bình")
        if "kinh lạy cha" in low:
            r["kinh_lay_cha"] += low.count("kinh lạy cha")
        if "kinh tin kính" in low:
            r["kinh_tin_kinh"] += low.count("kinh tin kính")
        if "nước đức chúa trời" in low:
            r["nuoc_dct"] += low.count("nước đức chúa trời")
        if "`" in ln:
            r["backtick"] += ln.count("`")
        if MD_LINK_RE.search(ln):
            r["md_link"] += 1
        if ln.lstrip().startswith(">"):
            r["blockquote"] += 1
        if HTML_TAG_RE.search(ln):
            r["html_tag"] += 1
        # English-passage heuristic: skip meta lines and review notes.
        s = ln.strip()
        if (s.startswith(("**Nguyên tác:**", "**Nguồn:**", "Nguồn:", "Nguyên tác:"))
                or "NEEDS REVIEW" in s or s.startswith("http")):
            continue
        if is_english_line(ln):
            r["english_lines"] += 1
            if len(r["english_sample"]) < 2:
                r["english_sample"].append(s[:160])
    return r


def main():
    idx = json.loads((ROOT / "translations/index.json").read_text(encoding="utf-8"))
    idx_by_file = {norm_file(e.get("file")): e for e in idx if norm_file(e.get("file"))}
    # Hidden files (.src-*) are ENGLISH SOURCE texts kept beside the
    # translations — they are not translations and must not be checked.
    files = sorted(p for p in pathlib.Path(ROOT / "translations").glob("*.txt")
                   if not p.name.startswith("."))
    rows = [check_file(p) for p in files]

    def count(key):
        return sum(1 for r in rows if r[key])

    def total(key):
        return sum(r[key] for r in rows)

    def top(key, n=20):
        return [{"file": r["file"], key: r[key]} for r in
                sorted(rows, key=lambda r: -r[key])[:n] if r[key]]

    eng_flagged = [r for r in rows
                   if r["english_lines"] > 10 and r["english_lines"] / max(1, r["lines"]) > 0.02]
    have_names = {p.name for p in files}
    missing_file = [e for e in idx if norm_file(e.get("file"))
                    and norm_file(e.get("file")) not in have_names]
    not_in_index = [r for r in rows if r["file"] not in idx_by_file]
    # Likely-same-work heuristic for unindexed files: an indexed file
    # whose slug shares most content words (e.g. 003-marrow-... vs
    # mg1-1094-marrow-... — different translations of one work).
    idx_wordsets = [(e_file, slug_words(e_file)) for e_file in idx_by_file]
    same_work, no_match = [], []
    for r in not_in_index:
        w = slug_words(r["file"])
        best = 0.0
        for _f, iw in idx_wordsets:
            if not w or not iw:
                continue
            ov = len(w & iw) / max(len(w), len(iw))
            if ov > best:
                best = ov
        (same_work if best >= 0.6 else no_match).append(r["file"])
    unindexed_examples = not_in_index[:10]

    summary = {
        "date": TODAY,
        "files_total": len(rows),
        "index_total": len(idx),
        "header_ai_chua_duyet": count("header"),
        "header_missing": len(rows) - count("header"),
        "footer_status_missing": len(rows) - count("footer_status"),
        "footer_terms_missing": len(rows) - count("footer_terms"),
        "needs_review_files": sum(1 for r in rows if r["needs_review"]),
        "needs_review_total": total("needs_review"),
        "english_flagged_files": len(eng_flagged),
        "english_lines_total": total("english_lines"),
        "cong_binh_lines": total("cong_binh"),
        "cong_binh_files": sum(1 for r in rows if r["cong_binh"]),
        "kinh_lay_cha": total("kinh_lay_cha"),
        "kinh_lay_cha_files": sum(1 for r in rows if r["kinh_lay_cha"]),
        "kinh_tin_kinh": total("kinh_tin_kinh"),
        "kinh_tin_kinh_files": sum(1 for r in rows if r["kinh_tin_kinh"]),
        "nuoc_dct_lines": total("nuoc_dct"),
        "nuoc_dct_files": sum(1 for r in rows if r["nuoc_dct"]),
        "backtick_files": sum(1 for r in rows if r["backtick"]),
        "md_link_files": sum(1 for r in rows if r["md_link"]),
        "blockquote_files": sum(1 for r in rows if r["blockquote"]),
        "html_tag_files": sum(1 for r in rows if r["html_tag"]),
        "tiny_files": count("tiny"),
        "no_title_files": len(rows) - count("has_title"),
        "index_entries_missing_file": len(missing_file),
        "txt_files_not_in_index": len(not_in_index),
        "unindexed_likely_same_work": len(same_work),
        "unindexed_no_match": len(no_match),
        "top_english": [{"file": r["file"], "english_lines": r["english_lines"],
                          "sample": r["english_sample"][:1]} for r in
                         sorted(eng_flagged, key=lambda r: -r["english_lines"])[:20]],
        "top_needs_review": top("needs_review"),
        "top_cong_binh": top("cong_binh"),
    }
    (ROOT / "data/quality-report.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")

    md = []
    md.append(f"# Báo cáo kiểm tra chất lượng bản dịch — {TODAY}\n")
    md.append("Kiểm tra bằng `scripts/check_translations.py` trên toàn bộ "
              f"`translations/*.txt` ({summary['files_total']:,} tệp) và "
              f"chỉ mục ({summary['index_total']:,} mục). Script này KHÔNG sửa "
              "bản dịch — mọi mục dưới đây đều cần quyết định của người duyệt "
              "trước khi sửa.\n")
    md.append("## Tổng quan\n")
    md.append(f"- Dòng đầu \"AI, chưa duyệt\": {summary['header_ai_chua_duyet']:,} có / "
              f"{summary['header_missing']:,} thiếu (hầu hết là tệp nhập hàng loạt cũ; "
              "nhãn \"Bản dịch AI, chưa duyệt\" vẫn hiện trên mọi trang sách qua huy hiệu duyệt).")
    md.append(f"- Thiếu chân trang TRANSLATION STATUS: {summary['footer_status_missing']:,} tệp; "
              f"thiếu TERMINOLOGY ISSUES: {summary['footer_terms_missing']:,} tệp.")
    md.append(f"- Dấu [NEEDS REVIEW]: {summary['needs_review_total']:,} dấu trong "
              f"{summary['needs_review_files']:,} tệp (ghi chú phục dựng OCR / chỗ chưa chắc — "
              "không tự nó là lỗi).")
    md.append(f"- Đoạn tiếng Anh chưa dịch (ngưỡng: >10 dòng và >2% số dòng): "
              f"{summary['english_flagged_files']} tệp, tổng {summary['english_lines_total']:,} dòng.")
    md.append(f"- \"công bình\": {summary['cong_binh_lines']:,} lượt trong {summary['cong_binh_files']:,} tệp — "
              "PHẦN LỚN là trích dẫn Kinh Thánh 1934 nguyên văn (ví dụ Ê-sai 64:5: “Chúa đón kẻ vui mừng làm sự công bình”), "
              "nơi từ này là đúng. Chỉ sai khi là giọng văn của chính bản dịch — cần rà soát thủ công từng chỗ, không sửa hàng loạt.")
    md.append(f"- \"Kinh Lạy Cha\": {summary['kinh_lay_cha']:,} lượt ({summary['kinh_lay_cha_files']:,} tệp) và "
              f"\"Kinh Tin Kính\": {summary['kinh_tin_kinh']:,} lượt ({summary['kinh_tin_kinh_files']:,} tệp) — "
              "đối chiếu mẫu cho thấy phần lớn là tên gọi quen thuộc của bài cầu nguyện / tín điều BÊN TRONG văn bản được dịch "
              "(“đọc kinh Lạy Cha”, “đã học thuộc Kinh Tin Kính”), không phải giọng văn riêng của trang. "
              "Thuật ngữ khóa “Bài Cầu Nguyện Chung” / “Tín Điều Các Sứ Đồ” áp dụng cho giọng văn của trang; "
              "có sửa các chỗ trong bản dịch hay không là quyết định duyệt theo ngữ cảnh, không sửa hàng loạt.")
    md.append(f"- \"nước Đức Chúa Trời\": {summary['nuoc_dct_lines']:,} lượt trong {summary['nuoc_dct_files']:,} tệp — "
              "như \"công bình\": đúng trong trích dẫn 1934, giọng văn riêng dùng "
              "\"Vương quốc Đức Chúa Trời\". Cần rà soát thủ công.")
    md.append(f"- Dấu hiệu markdown trong văn bản thuần: backtick {summary['backtick_files']:,} tệp, "
              f"liên kết markdown {summary['md_link_files']:,} tệp, trích dẫn `>` "
              f"{summary['blockquote_files']:,} tệp, thẻ HTML {summary['html_tag_files']:,} tệp.")
    md.append(f"- Tệp rất ngắn (<200 ký tự): {summary['tiny_files']:,} tệp; "
              f"không có dòng tựa: {summary['no_title_files']:,} tệp.")
    md.append(f"- Chỉ mục thiếu tệp: {summary['index_entries_missing_file']:,} mục; "
              f"tệp txt chưa có trong chỉ mục: {summary['txt_files_not_in_index']:,} tệp — "
              f"trong đó {summary['unindexed_likely_same_work']:,} tệp có khả năng là bản dịch khác của tác phẩm đã có "
              f"(đối chiếu tên tệp; ví dụ 003-marrow-modern-divinity-fisher.txt và mg1-1094-marrow-divinity-fisher.txt "
              f"là hai bản dịch khác nhau của cùng một tác phẩm Fisher), còn {summary['unindexed_no_match']:,} tệp "
              f"không khớp tác phẩm nào trong chỉ mục. Cần đối chiếu từng tệp trước khi quyết định giữ, liệt kê hay dọn.")
    md.append("\n## Tệp có nhiều đoạn tiếng Anh nhất\n")
    for e in summary["top_english"]:
        md.append(f"- `{e['file']}` — {e['english_lines']} dòng"
                  + (f" — ví dụ: _{e['sample'][0]}_" if e["sample"] else ""))
    md.append("\n## Tệp có nhiều dấu [NEEDS REVIEW] nhất\n")
    for e in summary["top_needs_review"]:
        md.append(f"- `{e['file']}` — {e['needs_review']} dấu")
    md.append("\n## Tệp có nhiều \"công bình\" nhất (cần rà soát thủ công)\n")
    for e in summary["top_cong_binh"]:
        md.append(f"- `{e['file']}` — {e['cong_binh']} lượt")
    if not_in_index:
        md.append("\n## Tệp txt chưa có trong chỉ mục (10 ví dụ đầu)\n")
        for r in unindexed_examples:
            md.append(f"- `{r['file']}` ({r['chars']:,} ký tự)")
    md.append("\n## Không tự sửa\n")
    md.append("Không có mục nào ở trên được sửa tự động trong đợt này: thêm dòng "
              "đầu \"AI, chưa duyệt\" cho ~3.000 tệp cũ là thao tác hàng loạt, cần "
              "tái tạo cả `txt/` và trang đọc; thêm chân trang TRANSLATION STATUS "
              "đồng nghĩa khẳng định trạng thái mà script không biết. Các mục này "
              "chờ quyết định duyệt theo từng đợt.\n")
    out = "\n".join(md)
    report_path = ROOT / f"scripts/quality-report-{TODAY}.md"
    report_path.write_text(out, encoding="utf-8")
    print(out)
    print(f"\nwrote data/quality-report.json + {report_path.name}")


if __name__ == "__main__":
    main()
