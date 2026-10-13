#!/usr/bin/env python3
"""Clean OCR of J.W. Alexander 'Thoughts on Family Worship' (1847)."""
import re, sys

src = "/tmp/alexander_family_worship.txt"
dst = "/home/hatch/workspace/reformed-site/tools/alexander_fw_clean.txt"

with open(src, encoding="utf-8", errors="replace") as f:
    text = f.read()

# Drop lines that are pure scan-artifact noise (box-drawing / lone symbols)
lines = []
for ln in text.split("\n"):
    s = ln.strip()
    if not s:
        lines.append("")
        continue
    # scan garbage lines: mostly non-alphanumeric
    alnum = sum(1 for c in s if c.isalnum())
    if len(s) > 0 and alnum / len(s) < 0.35:
        continue
    lines.append(ln)

text = "\n".join(lines)

# Remove page headers/footers like "PREFACE. 3", "10 FAMILY-WORSHIP.", "CONTENTS. 7"
text = re.sub(r"(?m)^\d+\s+(PREFACE|FAMILY-WORSHIP|CONTENTS|FAMILY-WOKSHIP)\.?\s*$", "", text)
text = re.sub(r"(?m)^(PREFACE|FAMILY-WORSHIP|CONTENTS|FAMILY-WOKSHIP)\.?\s+\d+\*?\s*$", "", text)
# lone page numbers
text = re.sub(r"(?m)^\d{1,3}\*?\s*$", "", text)

# Remove NYPL/library stamps and barcode lines
text = re.sub(r"(?m)^NYPL.*$", "", text)
text = re.sub(r"(?m)^\d\s+\d{4}\s+\d{8}.*$", "", text)

# Remove copyright/print boilerplate
text = re.sub(r"(?m)^Entered\s+according\s+to\s+the\s+act\s+of\s+Congress.*$", "", text)
text = re.sub(r"(?m)^A\.\s*W\.\s*Mitchell.*$", "", text)
text = re.sub(r"(?m)^In\s+the\s+office\s+of\s+the\s+Clerk.*$", "", text)
text = re.sub(r"(?m)^District\s+of\s+Pennsylvania.*$", "", text)
text = re.sub(r"(?m)^PRINTED\s+BY.*$", "", text)
text = re.sub(r"(?m)^WILLIAM\s+S\.\s*MARTIEN.*$", "", text)
text = re.sub(r"(?m)^PRESBYTERIAN\s+BOARD\s+OF\s+PUBLICATION.*$", "", text)
text = re.sub(r"(?m)^PHILADELPHIA:.*$", "", text)
text = re.sub(r"(?m)^JAMES\s+W\.'?ALEXANDER,.*$", "JAMES W. ALEXANDER,", text)
text = re.sub(r"(?m)^PASTOR\s+OF\s+THE\s+DUANE-STREET.*$", "PASTOR OF THE DUANE-STREET PRESBYTERIAN CHURCH, NEW YORK.", text)

# Collapse multiple spaces to one (OCR double-spacing)
text = re.sub(r"[ \t]{2,}", " ", text)

# Join hyphenated words split across line breaks: "convic-\ntion" -> "conviction"
# (also handles "convic- \n tion" with stray spaces around the newline)
text = re.sub(r"(\w)-[ \t]*\n[ \t]*(\w)", r"\1\2", text)

# Fix systematic OCR misreads: spurious capital T inserted (wTell->well, wTorld->world)
text = re.sub(r"wT([a-z])", lambda m: "w" + m.group(1), text)
text = text.replace("tJa", "Ja")
text = text.replace("rlowTs", "flows")
text = text.replace("tVie", "the")
text = text.replace("growTth", "growth")
text = text.replace("OP FAMILYWORSHIP", "OF FAMILY-WORSHIP")
text = text.replace("OP FAMILY-WORSHIP", "OF FAMILY-WORSHIP")
text = text.replace("Pa<rn", "Part")
text = text.replace("resrard", "regard")
text = text.replace("lie would desire", "he would desire")
text = text.replace("w^e", "we")
text = text.replace("n'ot", "not")
text = text.replace("FAMILY-WOKSHIP", "FAMILY-WORSHIP")
text = text.replace("continualhj", "continually")
text = text.replace("re-apppearing", "reappearing")
text = text.replace("wmich", "which")

# Join lines within paragraphs: a line not ending with sentence punctuation and
# next line not blank and not a heading -> join with space.
paras = []
buf = ""
def flush():
    global buf
    if buf.strip():
        paras.append(buf.strip())
    buf = ""

for ln in text.split("\n"):
    s = ln.strip()
    if not s:
        flush()
        continue
    # headings: CHAPTER I., all-caps title lines, dedication lines in caps
    is_heading = bool(re.match(r"^(CHAPTER\s+[IVXLCDM]+\.?|CONTENTS\.?|PREFACE\.?|THE\s+END\.?)$", s, re.I))
    if is_heading:
        flush()
        paras.append(s)
        continue
    if buf:
        buf += " " + s
    else:
        buf = s
flush()

# Final pass: join any hyphen-space splits surviving inside paragraphs
paras = [re.sub(r"(\w)- (\w)", r"\1\2", p) for p in paras]

with open(dst, "w", encoding="utf-8") as f:
    f.write("\n\n".join(paras) + "\n")

print("cleaned paragraphs:", len(paras))
print("words:", sum(len(p.split()) for p in paras))
