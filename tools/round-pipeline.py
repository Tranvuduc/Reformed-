#!/usr/bin/env python3
"""Unified pipeline for one translation round: staging -> index -> pages -> live-verify.

Replaces the four separate agents (staging, commit-by-hand, page-step, live-poll)
plus Molly's manual checks at each step. The script does every mechanical step,
stops before `git commit`, and prints the exact commit/push commands for Molly.

Usage:
    python3 tools/round-pipeline.py --round 96            # stages (a)-(d), then STOP, print commit cmds
    python3 tools/round-pipeline.py --round 96 --live      # stage (e) only, AFTER Molly commits + pushes
    python3 tools/round-pipeline.py --round 96 --dry-run   # read-only checks + simulated writes
    python3 tools/round-pipeline.py --round 96 --level 2 --by Molly

Rules (all learned the hard way, rounds 78-95):
  * NEVER commit or push. No `git commit` / `git push` call exists in this file.
  * Packet §6 may be wrong (R88 lesson) -- the .txt title block is authoritative
    for title/short/orig; the live index is authoritative for counts.
  * books-lookup.json uses DEFAULT separators (", " + ": "), NOT compact.
    Verified by machine BEFORE writing; parse-check IMMEDIATELY after writing
    (R91 staging lesson, R94 comma lesson).
  * index files are single-line, compact separators, sort_keys, NO trailing
    newline. books-lookup is "[\\n" + one entry per line + "\\n]\\n".
  * gen4 title-cases Roman numerals >= 6 chars wrong ("XXXIII" -> "Xxxiii",
    R95). Fixed output-only AFTER gen4, BEFORE og regen; scan "Xx" every round.
  * gen4 og images carry Dore art. Regenerate art-free from a clean dir with
    NO img/; verify pixel (1000,300) == (243,239,228).
  * .sig = md5("v4|" + "ban-dich/<slug>.html" + "|" + og:title + "|" +
    og:description)[:12], path WITHOUT leading slash, title/desc HTML-UNESCAPED.
  * Page word counts use "." thousand separators: regex (\\d[\\d.]*) từ.
    gen4's count reads systematically HIGHER than the .txt body (R89
    adjudication) -- NOT a defect; the .txt footer is authoritative. A page
    count LOWER than the .txt body IS a defect (content lost) -> FAIL.
  * Flag counts use the prefix "[NEEDS REVIEW" (no closing bracket).
  * Sitemap is valid XML since KT-06 (2026-11-18), exactly the build-pages.py
    format: <?xml ...?>\n<urlset xmlns="http://www.sitemaps.org/schemas/
    sitemap/0.9"> + fragments + </urlset>\n. Appenders insert new entries
    BEFORE </urlset> (legacy fragment files without a wrapper fall back to
    EOF append). build_search.py rewrites tim-kiem/index.html from its
    template on every run -> revert it to HEAD afterwards (known drift).
  * Live poll: Vercel deploy lag is 4-25 min; an all-404 first try is normal,
    retry before reporting failure. Poll totals are computed from the check
    list, never hand-counted (R92 "18/18" was really 19).
  * /tmp is wiped on VM reboot: all workdirs live under ~/workspace.
  * GITHUB_TOKEN comes transiently from `gh auth token`; it is NEVER written
    to a file or printed (gen4 needs it -- unauthenticated GitHub API = 403).
  * The coordinator's "ĐẠT" is NEVER trusted: this pipeline only stages
    deliveries that already passed Molly's INDEPENDENT verification. It does
    NOT re-verify translation quality (quotes vs hub 1934, gaps, footnotes) --
    that stays a separate human-supervised step (rNN-verify-independent.py).
    What it verifies is the PACKAGING: packet vs .txt, index formats,
    generated pages, sitemap/search, live state.

Exit codes: 0 = all stages PASS; 1 = a stage FAILED (exception report printed,
run stops at the first FAIL); 2 = usage error.
"""
import argparse
import hashlib
import html
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

HOME = Path.home()
REPO = HOME / "workspace/repos/reformed-vietnam"
SELF = Path(__file__).resolve()
SELF_REL = str(SELF.relative_to(REPO))  # tools/round-pipeline.py
SELF_PYC_DIR = REPO / "tools/__pycache__"
GEN4 = HOME / "workspace/your_files/helper-deliveries/ken-gen4/gen4.py"
GEN4_DIR = GEN4.parent
COWORK = HOME / "workspace/your_files/coworking"
DELIV_ROOT = HOME / "workspace/your_files/helper-deliveries"
BASE = "https://reformedvietnam.com"
OG_BG = (243, 239, 228)
ROMAN = re.compile(r"^[IVXLCDM]+$")
TITLECASE_CORRUPT = re.compile(r"\bXx[a-z]+\b")  # tripwire: "Xxxiii", "Xxxvii", ...
WORD_COUNT_RE = re.compile(r"(\d[\d.]*) từ")
FLAG_RE = re.compile(r"\[NEEDS REVIEW: [^\]]*\]")  # FULL chunk incl. prefix + "]"
FLAG_BTN = '<button type="button" class="nr-flag"'
BADGE = '<span class="rv-badge'
NR_TEXT_RE = re.compile(r'<span class="nr-text"[^>]*>(.*?)</span>', re.S)
OG_TITLE_RE = re.compile(r'<meta property="og:title" content="(.*?)">')
OG_DESC_RE = re.compile(r'<meta property="og:description" content="(.*?)">')


class Fail(Exception):
    """A stage failed. Message goes verbatim into the exception report."""


def log(msg=""):
    print(msg, flush=True)


def stage_head(name):
    log(f"\n===== {name} =====")


def run(cmd, cwd=None, env=None, check=True, capture=True):
    """Run a command. Returns CompletedProcess. Raises Fail on nonzero exit."""
    r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=capture, text=True)
    if check and r.returncode != 0:
        raise Fail(f"command failed ({r.returncode}): {' '.join(str(c) for c in cmd)}\n"
                    f"stdout tail:\n{r.stdout[-2000:]}\nstderr tail:\n{r.stderr[-2000:]}")
    return r


def git(*args):
    return run(["git", "-C", str(REPO), *args]).stdout


def git_status():
    out = git("status", "--porcelain")
    return out.rstrip("\n").splitlines() if out.strip() else []


def git_status_ignoring_self():
    """Working-tree status minus this script itself (uncommitted until Molly
    commits it in its own commit) and its regenerable __pycache__ bytecode.
    Stale self .pyc files are deleted -- running the script as __main__ never
    creates one; only py_compile/import does. The TRACKED tts_gen pyc in the
    same dir is never touched."""
    if SELF_PYC_DIR.is_dir():
        for p in SELF_PYC_DIR.glob("round-pipeline.*.pyc"):
            p.unlink()
            log(f"  (removed stale self bytecode {p.name})")
    kept = []
    for ln in git_status():
        path = ln[3:]
        if path == SELF_REL or path.startswith("tools/__pycache__/round-pipeline."):
            continue
        kept.append(ln)
    return kept


# ---------------------------------------------------------------- packet ----
def parse_packet(round_no):
    """Parse VONG-NN packet §6 table + §6.1/§6.2 topic counts + header label.

    Table shape varies by round: R95/R96 have (id, title, short, orig, length);
    R89 has (id, title, short, length, topics) and no orig column. Columns are
    mapped by header name; orig/topics may come from the table or fall back to
    the .txt (orig) / the §6.1 bullets (shared topics).
    Returns dict: {label, rows: [{slug,title,short,orig,length,topics|None}],
                   topics: {name: (before, after)}, index_before, index_after}
    """
    path = COWORK / f"VONG-{round_no}-PARALLEL.md"
    if not path.exists():
        raise Fail(f"packet not found: {path}")
    pkt = path.read_text(encoding="utf-8")
    m = re.search(r"# VÒNG \d+ — PARALLEL: (.+?)\s*\(", pkt)
    label = re.sub(r"[*`,]", "", m.group(1)).strip() if m else f"Vòng {round_no}"
    # NOTE: split on line-anchored headers. A plain split("## §6") also splits
    # "### §6.1" (it contains "## §6" at index 1) and would cut §6.1 off.
    sec = re.split(r"^## §6\b", pkt, flags=re.M)[1]
    sec = re.split(r"^## §7\b", sec, flags=re.M)[0]

    header = None
    rows = []
    for ln in sec.splitlines():
        s = ln.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells):
            continue  # separator row
        if header is None and any("title" in c.lower() for c in cells) \
                and any("short" in c.lower() for c in cells):
            header = [c.lower() for c in cells]
            continue
        if header is not None and re.match(r"R\d+-", cells[0]):
            rows.append(cells)
    if header is None or not rows:
        raise Fail(f"packet §6 table not parsed (header={header}, rows={len(rows)})")

    def col(*names):
        for i, h in enumerate(header):
            if any(n in h for n in names):
                return i
        return None

    ci = {"slug": col("id", "slug"), "title": col("title"), "short": col("short"),
          "orig": col("orig"), "length": col("length"), "topics": col("topics")}
    if ci["slug"] is None or ci["title"] is None or ci["short"] is None \
            or ci["length"] is None:
        raise Fail(f"packet §6 missing required columns: header={header}")
    out_rows = []
    for cells in rows:
        if len(cells) != len(header):
            raise Fail(f"§6 row has {len(cells)} cols, header has {len(header)}: "
                       f"{cells[0] if cells else '?'}")
        slug = cells[ci["slug"]].strip("`")
        topics = None
        if ci["topics"] is not None and cells[ci["topics"]].strip():
            topics = [t.strip() for t in cells[ci["topics"]].split(",") if t.strip()]
        out_rows.append({
            "slug": slug,
            "title": cells[ci["title"]],
            "short": cells[ci["short"]],
            "orig": cells[ci["orig"]] if ci["orig"] is not None else None,
            "length": cells[ci["length"]],
            "topics": topics,
        })

    topics = {}
    index_before = index_after = None
    for ln in sec.splitlines():
        mm = re.match(r"-\s*(.+?):\s*([\d.]+)\s*→\s*\*\*([\d.]+)\*\*", ln.strip())
        if not mm:
            continue
        name, before, after = mm.group(1).strip(), int(mm.group(2).replace(".", "")), \
            int(mm.group(3).replace(".", ""))
        if name.lower().startswith("index"):
            index_before, index_after = before, after
        else:
            topics[name] = (before, after)
    return {"label": label, "rows": out_rows, "topics": topics,
            "index_before": index_before, "index_after": index_after}


def author_from_l3(l3):
    return re.sub(r"\s*\([^)]*\)\s*$", "", l3).strip()


def derive_short(packet_short, l7, l8):
    """Expected short from the .txt title block.
    Chapter books: <series> — Chương <RN>: <L8>. Other books: short == L8."""
    if l7.startswith("CHƯƠNG "):
        rn = l7[len("CHƯƠNG "):].strip()
        prefix = packet_short.split(" — Chương ")[0]
        return f"{prefix} — Chương {rn}: {l8}"
    return l8


def body_of(text):
    return text.split("TRANSLATION STATUS")[0]


def derive_length(body):
    bc, bw = len(body), len(body.split())
    return ("dai" if (bw >= 6300 or bc >= 28000) else "vừa"), bc, bw


# ------------------------------------------------------------- manifest -----
def load_items(round_no, txt_source):
    """Parse packet §6 + .txt title blocks into per-slug items (no live-index
    comparison). Used by staging-verify AND by the dry-run regression check,
    which re-verifies ALREADY-COMMITTED pages (their slugs are in the index
    by design, so novelty/count checks must not run there)."""
    pkt = parse_packet(round_no)
    items = []
    diffs = []
    for row in pkt["rows"]:
        slug = row["slug"]
        p = Path(txt_source) / slug / f"{slug}.txt"
        if not p.exists():
            raise Fail(f"delivery .txt missing: {p}")
        text = p.read_text(encoding="utf-8")
        lines = text.split("\n")
        if len(lines) < 10:
            raise Fail(f"{slug}: title block has only {len(lines)} lines")
        L = {i: lines[i] for i in range(10)}
        if L[0] != "AI, chưa duyệt":
            diffs.append(f"{slug}: L0={L[0]!r}")
        if L[1] != "" or L[6] != "" or L[9] != "":
            diffs.append(f"{slug}: blank lines L1/L6/L9 not empty")
        if L[2] != row["title"]:
            diffs.append(f"{slug}: title L2 mismatch\n  txt: {L[2]}\n  pkt: {row['title']}")
        author = author_from_l3(L[3])
        if not author:
            diffs.append(f"{slug}: author L3 unparsable: {L[3]!r}")
        orig = row["orig"]
        if not L[4].startswith("Nguyên tác: "):
            diffs.append(f"{slug}: L4 does not start with 'Nguyên tác: ': {L[4][:60]!r}")
        elif orig is not None and L[4][len("Nguyên tác: "):] != orig:
            diffs.append(f"{slug}: orig mismatch\n  txt: {L[4]}\n  pkt: {orig}")
        else:
            orig = L[4][len("Nguyên tác: "):]  # .txt is authoritative
        if not L[5].startswith("Nguồn: "):
            diffs.append(f"{slug}: L5 does not start with 'Nguồn: ': {L[5][:60]!r}")
        exp_short = derive_short(row["short"], L[7], L[8])
        if exp_short != row["short"]:
            diffs.append(f"{slug}: short mismatch\n  txt-derived: {exp_short}\n  pkt: {row['short']}")
        body = body_of(text)
        length, bc, bw = derive_length(body)
        if length != row["length"]:
            diffs.append(f"{slug}: length {length} != packet {row['length']} "
                         f"(body {bc}/{bw})")
        topics = row["topics"]
        if topics is None:
            topics = list(pkt["topics"].keys())
        if not topics:
            diffs.append(f"{slug}: no topics (no topics column, no §6.1 bullets)")
        items.append({
            "slug": slug, "title": row["title"], "short": row["short"],
            "orig": orig, "length": length, "topics": topics, "author": author,
            "body_chars": bc, "body_words": bw,
            "flags": body.count("[NEEDS REVIEW"),
            "flag_texts": FLAG_RE.findall(body),
            "txt_path": str(p),
        })
        log(f"  {slug[:64]}... title/short/orig OK body {bc}/{bw} -> {length} "
            f"flags={items[-1]['flags']} topics={topics}")
    if diffs:
        raise Fail("packet §6 vs .txt diffs (%d):\n" % len(diffs) + "\n".join(diffs))
    return pkt, items


def build_manifest(round_no, txt_source):
    """Stage (a): verify packet §6 vs .txt title blocks + counts, by machine.

    txt_source: directory holding <slug>/<slug>.txt deliveries (roundNN dir).
    Adds the live-index checks on top of load_items: slug novelty, topic
    before-counts and index totals (live index authoritative; packet may lie).
    Returns manifest dict (also used by stages b/c/d).
    """
    pkt, items = load_items(round_no, txt_source)
    idx = json.loads((REPO / "translations/index.json").read_text(encoding="utf-8"))
    ids = {e.get("id") for e in idx}
    files = {e.get("file") for e in idx}
    topic_counts = Counter()
    for e in idx:
        for t in e.get("topics", []):
            topic_counts[t] += 1
    diffs = []
    for it in items:
        if it["slug"] in ids:
            diffs.append(f"{it['slug']}: slug already in index.json (id hit)")
        if (it["slug"] + ".txt") in files:
            diffs.append(f"{it['slug']}: file already in index.json (file hit)")
    # topic + index counts (live index is authoritative; packet may be wrong)
    for name, (before, after) in pkt["topics"].items():
        have = topic_counts.get(name, 0)
        n_with = sum(1 for it in items if name in it["topics"])
        if have != before:
            diffs.append(f"topic {name}: index has {have}, packet §6.1 says {before}")
        if after != before + n_with:
            diffs.append(f"topic {name}: packet after {after} != {before}+{n_with}")
        log(f"  topic {name}: {have} -> {have + n_with} (packet {before} -> {after})")
    if pkt["index_before"] is not None and len(idx) != pkt["index_before"]:
        diffs.append(f"index total: live {len(idx)}, packet §6.1 says "
                     f"{pkt['index_before']}")
    if pkt["index_after"] is not None and pkt["index_after"] != len(idx) + len(items):
        diffs.append(f"index after: packet says {pkt['index_after']}, "
                     f"live+new = {len(idx) + len(items)}")
    log(f"  index: {len(idx)} -> {len(idx) + len(items)}")
    if diffs:
        raise Fail("STAGING-VERIFY diffs (%d):\n" % len(diffs) + "\n".join(diffs))
    return {"round": round_no, "label": pkt["label"], "items": items,
            "index_before": len(idx), "index_after": len(idx) + len(items),
            "topics_before": {t: topic_counts.get(t, 0) for t in pkt["topics"]}}

# -------------------------------------------------------- stage (b) index --
def full_entry(it, level, by):
    return {"author": it["author"], "by": by, "file": it["slug"] + ".txt",
            "id": it["slug"], "length": it["length"], "level": level,
            "orig": it["orig"], "review_status": "ai-draft", "reviewed": False,
            "short": it["short"], "title": it["title"], "topics": it["topics"]}


def lite_entry(it, level):
    return {"author": it["author"], "id": it["slug"], "length": it["length"],
            "level": level, "review_status": "ai-draft", "short": it["short"],
            "slug": it["slug"], "topics": it["topics"]}


def update_single_line(path, entries):
    """Single-line compact sort_keys, no trailing newline. Immediate parse-check."""
    raw = Path(path).read_text(encoding="utf-8")
    # lesson: .rstrip("\\n") not .strip() -- the file is one long line
    assert "\n" not in raw.rstrip("\n") and not raw.endswith("\n"), \
        f"{path}: not single-line / has trailing newline"
    data = json.loads(raw)
    before = len(data)
    data.extend(entries)
    out = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    assert "\n" not in out and not out.endswith("\n")
    Path(path).write_text(out, encoding="utf-8")
    chk = json.loads(Path(path).read_text(encoding="utf-8"))
    assert len(chk) == before + len(entries), \
        f"{path}: count {len(chk)} != {before + len(entries)}"
    for e in entries:
        assert any(x.get("id") == e["id"] for x in chk), f"{path}: missing {e['id']}"
    log(f"  {path.name}: {before} -> {len(chk)}  parse-check PASS")
    return before, len(chk)


def update_books_lookup(path, items):
    """books-lookup.json: '[\\n' + one entry/line + '\\n]\\n', DEFAULT separators.
    Separators verified by machine BEFORE writing; parse-check IMMEDIATELY after
    (R94 lesson: a forgotten trailing comma breaks the whole file)."""
    raw = Path(path).read_text(encoding="utf-8")
    assert raw.startswith("[\n") and raw.endswith("]\n"), \
        "books-lookup wrapper wrong (want '[\\n' ... '\\n]\\n')"
    lines = raw.splitlines()
    entries_before = len(lines) - 2
    assert not lines[-2].endswith(","), "last old entry already has a comma?!"
    new_lines = []
    for i, it in enumerate(items):
        ent = {"a": it["author"], "s": it["slug"], "t": it["short"]}
        line = json.dumps(ent, ensure_ascii=False)  # DEFAULT separators
        assert '": "' in line and '", "' in line and '":"' not in line, \
            f"default-sep fail: {line[:80]}"
        if i < len(items) - 1:
            line += ","
        new_lines.append(line)
    out_lines = lines[:-1]  # drop "]"
    out_lines[-1] = out_lines[-1] + ","  # comma on last old entry
    out_lines.extend(new_lines)
    out_lines.append("]")
    Path(path).write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    chk = json.loads(Path(path).read_text(encoding="utf-8"))
    assert len(chk) == entries_before + len(items), \
        f"books-lookup count {len(chk)} != {entries_before + len(items)}"
    for it in items:
        assert any(x.get("s") == it["slug"] for x in chk), \
            f"books-lookup missing {it['slug']}"
    # old lines unchanged except the comma on the old last line
    after = Path(path).read_text(encoding="utf-8").splitlines()
    assert after[1:entries_before] == lines[1:entries_before], \
        "books-lookup: old lines changed!"
    assert after[entries_before] == lines[entries_before] + ",", \
        "books-lookup: old last line not comma'd as expected"
    log(f"  books-lookup.json: {entries_before} -> {len(chk)}  parse-check PASS")
    return entries_before, len(chk)


def stage_b_index_write(manifest, level, by, dry_run):
    stage_head("(b) INDEX-WRITE")
    items = manifest["items"]
    if dry_run:
        log("  DRY-RUN: no files written. Planned entries:")
        for it in items:
            log("   full: " + json.dumps(full_entry(it, level, by), ensure_ascii=False))
            log("   lite: " + json.dumps(lite_entry(it, level), ensure_ascii=False))
            log(f"   lookup: {json.dumps({'a': it['author'], 's': it['slug'], 't': it['short']}, ensure_ascii=False)}")
        log(f"  would copy {len(items)} .txt files to translations/ (byte-identical)")
        log(f"  index {manifest['index_before']} -> {manifest['index_after']} (simulated)")
        return
    update_single_line(REPO / "translations/index.json",
                       [full_entry(it, level, by) for it in items])
    update_single_line(REPO / "translations/index-lite.json",
                       [lite_entry(it, level) for it in items])
    update_single_line(REPO / "translations/index.min.json",
                       [lite_entry(it, level) for it in items])
    update_books_lookup(REPO / "api/data/books-lookup.json", items)
    for it in items:
        src = Path(it["txt_path"])
        dst = REPO / "translations" / (it["slug"] + ".txt")
        shutil.copyfile(src, dst)
        assert src.read_bytes() == dst.read_bytes(), f"copy mismatch {it['slug']}"
        log(f"  copied translations/{it['slug']}.txt (byte-identical)")
    st = git_status_ignoring_self()
    expect_mod = {"translations/index.json", "translations/index-lite.json",
                  "translations/index.min.json", "api/data/books-lookup.json"}
    expect_new = {f"translations/{it['slug']}.txt" for it in items}
    got_mod = {l[3:] for l in st if l.startswith(" M ")}
    got_new = {l[3:] for l in st if l.startswith("?? ")}
    if got_mod != expect_mod or got_new != expect_new:
        raise Fail(f"git status after stage (b) is not exactly the expected set:\n"
                   f"  modified: {sorted(got_mod)} (want {sorted(expect_mod)})\n"
                   f"  untracked: {sorted(got_new)} (want {sorted(expect_new)})")
    log(f"  git status: exactly {len(expect_mod)} modified + {len(expect_new)} new, "
        "nothing else")
    log("  (b) PASS")


# ----------------------------------------------------------- stage (c) pages -
def gh_token():
    r = run(["gh", "auth", "token"], check=True)
    tok = r.stdout.strip()
    if not tok:
        raise Fail("`gh auth token` returned empty (env GITHUB_TOKEN is empty too; "
                   "unauthenticated GitHub API = 403 for gen4)")
    return tok  # NEVER printed or written to a file


def og_meta(html_text):
    """og:title / og:description from built HTML, HTML-UNESCAPED."""
    mt = OG_TITLE_RE.search(html_text)
    md = OG_DESC_RE.search(html_text)
    if not mt or not md:
        raise Fail("og:title / og:description meta not found in built HTML")
    return html.unescape(mt.group(1)), html.unescape(md.group(1))


def compute_sig(slug, title, desc):
    return hashlib.md5(
        f"v4|ban-dich/{slug}.html|{title}|{desc}".encode("utf-8")).hexdigest()[:12]


def roman_corruptions(title):
    """(correct, corrupted) pairs for Roman-numeral tokens gen4 mangles.

    _keep_caps() in tools/vi_books.py keeps Roman numerals only up to length 5;
    longer ones get .capitalize(): XXXIII -> Xxxiii, XXXVII -> Xxxvii,
    XXXVIII -> Xxxviii. (XXXVI is 5 chars: safe.)
    """
    out = []
    for tok in re.findall(r"[IVXLCDM]{2,}", title):
        if len(tok) >= 6 and ROMAN.match(tok):
            out.append((tok, tok.capitalize()))
    return out


def fix_titlecase(html_text, slug, title):
    """Output-only fix of gen4's Roman-numeral title-casing. Returns new text."""
    fixed = html_text
    for correct, corrupt in roman_corruptions(title):
        n_before = fixed.count(corrupt)
        if n_before:
            fixed = fixed.replace(corrupt, correct)
            log(f"  {slug[:40]}: title-case fix {corrupt} -> {correct} "
                f"({n_before} places)")
        else:
            log(f"  {slug[:40]}: no {corrupt} corruption found (already correct?)")
        if corrupt in fixed:
            raise Fail(f"{slug}: {corrupt} still present after title-case fix")
    # tripwire: any other Xx... token left in title/h1 (a numeral we did not expect)
    m = re.search(r"<title>(.*?)</title>", fixed, re.S)
    hay = (m.group(1) if m else "") + " " + " ".join(
        re.findall(r"<h1[^>]*>(.*?)</h1>", fixed, re.S))
    bad = TITLECASE_CORRUPT.findall(html.unescape(hay))
    if bad:
        raise Fail(f"{slug}: unexpected title-case corruption in title/h1: {bad}")
    # tripwire: standalone "AI" in title/h1 is ALWAYS the Vietnamese pronoun
    # "ai" (or "Ai Ca" = Lamentations), never the acronym -- 9 live pages
    # had this misfire before "AI" was removed from _ACRONYMS (vi_books.py,
    # 2026-11-16, fix ccfe5b35/4f15baa3). The legit "AI" only lives in the
    # fixed label "Bản dịch AI, chưa duyệt", never in a title.
    if re.search(r"\bAI\b", html.unescape(hay)):
        raise Fail(f"{slug}: standalone 'AI' in title/h1 -- "
                   f"the Vietnamese pronoun 'ai' must be 'Ai' (fix output-only, "
                   f"then recompute .sig)")
    return fixed


def regen_og_artfree(workdir, items):
    """Regenerate og images art-free from a clean dir with NO img/.

    tools/og_images.py pastes Dore art iff img/dore-sermon.jpg exists relative
    to the CWD, so the regen runs with cwd=<clean dir>. Imported with
    sys.dont_write_bytecode so no tools/__pycache__ is created (tts_gen pyc
    in there is TRACKED -- never touch it).
    Returns {slug: (jpg_path_in_repo, sig)}.
    """
    ogdir = Path(workdir) / "og-clean"
    if ogdir.exists():
        shutil.rmtree(ogdir)
    ogdir.mkdir(parents=True)
    assert not (ogdir / "img").exists(), "og-clean dir must not contain img/"
    spec = importlib.util.spec_from_file_location(
        "og_images_local", REPO / "tools/og_images.py")
    mod = importlib.util.module_from_spec(spec)
    old_dwb = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    old_cwd = os.getcwd()
    try:
        spec.loader.exec_module(mod)
        os.chdir(ogdir)
        out = {}
        for it in items:
            slug = it["slug"]
            html_text = (REPO / "ban-dich" / f"{slug}.html").read_text(encoding="utf-8")
            title, desc = og_meta(html_text)
            got = mod.og_image(f"ban-dich/{slug}.html", title, desc)
            jpg = ogdir / got
            sigf = ogdir / (got + ".sig")
            if not jpg.exists() or not sigf.exists():
                raise Fail(f"og regen produced nothing for {slug}")
            shutil.copyfile(jpg, REPO / "og" / jpg.name)
            shutil.copyfile(sigf, REPO / "og" / sigf.name)
            out[slug] = (str(REPO / "og" / jpg.name), sigf.read_text().strip())
            log(f"  og {slug[:40]}: {jpg.name} + .sig {out[slug][1]}")
        return out
    finally:
        os.chdir(old_cwd)
        sys.dont_write_bytecode = old_dwb


def check_built_page(item, html_path):
    """Machine checks on one built ban-dich page. Returns list of findings
    (empty = PASS). `item` is a manifest entry (slug/title/short/flags/...)."""
    slug = item["slug"]
    problems = []
    h = Path(html_path).read_text(encoding="utf-8")
    nb = h.count(BADGE)
    if nb != 1:
        problems.append(f"badge count {nb} != 1")
    nf = h.count(FLAG_BTN)
    if nf != item["flags"]:
        problems.append(f"flag buttons {nf} != .txt flags {item['flags']}")
    html_flags = [html.unescape(x) for x in NR_TEXT_RE.findall(h)]
    # R100: the renderer (vi_books.py emphasis-stripper) drops "__" pairs,
    # so "___" in a .txt flag renders as "_" in HTML. That is a rendering
    # quirk, not flag drift -- compare flag texts with underscore runs
    # collapsed so the check still catches real changes (missing/added/
    # rewritten flags) without failing on this cosmetic difference.
    def _norm_flags(texts):
        return [re.sub(r"_+", "_", t) for t in texts]
    if _norm_flags(html_flags) != _norm_flags(item["flag_texts"]):
        first_diff = next(((a, b) for a, b in zip(html_flags, item["flag_texts"])
                           if a != b), None)
        problems.append(f"flag texts differ (html {len(html_flags)} vs "
                        f"txt {len(item['flag_texts'])}; first diff: {first_diff})")
    if "TRANSLATION STATUS" in h:
        problems.append("TRANSLATION STATUS rendered into HTML")
    m = WORD_COUNT_RE.search(h)
    if not m:
        problems.append("no '<n> từ' word count found in HTML")
    else:
        page_words = int(m.group(1).replace(".", "").replace(",", ""))
        if page_words < item["body_words"]:
            problems.append(f"page words {page_words} < .txt body words "
                            f"{item['body_words']} (content lost?)")
        log(f"  {slug[:40]}: page words {page_words} vs .txt body "
            f"{item['body_words']} (delta {page_words - item['body_words']:+d}, "
            "gen4 reads high by design)")
    # .sig recompute
    title, desc = og_meta(h)
    sig = compute_sig(slug, title, desc)
    sigf = REPO / "og" / f"ban-dich-{slug}.jpg.sig"
    if sigf.exists():
        if sigf.read_text().strip() != sig:
            problems.append(f".sig mismatch: file {sigf.read_text().strip()} "
                            f"!= recomputed {sig}")
    else:
        problems.append(".sig file missing")
    return problems


def check_og_pixel(slug):
    from PIL import Image
    p = REPO / "og" / f"ban-dich-{slug}.jpg"
    if not p.exists():
        return f"og jpg missing: {p.name}"
    px = Image.open(p).convert("RGB").getpixel((1000, 300))
    if px != OG_BG:
        return f"og pixel (1000,300) = {px}, want art-free {OG_BG} (Dore art?)"
    return None


def stray_scan():
    """Corpus-wide stray-header scan (both known forms). Returns total count."""
    total = 0
    d = REPO / "ban-dich"
    for fn in d.glob("*.html"):
        t = fn.read_text(encoding="utf-8", errors="ignore")
        total += t.count("<p>AI, chưa duyệt</p>") + t.count("AI, chưa duyệt<br>")
    return total


def stage_c_pages(manifest, workdir, dry_run):
    stage_head("(c) PAGES (gen4 + og art-free + page checks)")
    items = manifest["items"]
    if dry_run:
        # Regression-test the page-check logic on the PREVIOUS round's committed
        # pages (no gen4 run, no writes). Round NN-1's packet + deliveries exist.
        prev = manifest["round"] - 1
        log(f"  DRY-RUN: checking committed round-{prev} pages with the same "
            "code the real run uses (no gen4, no writes)")
        # load_items only: no novelty/count checks -- round NN-1 is committed,
        # so its slugs ARE in the index and its counts have moved on.
        _pkt, prev_items = load_items(prev, DELIV_ROOT / f"round{prev}")
        n_bad = 0
        for it in prev_items:
            slug = it["slug"]
            hp = REPO / "ban-dich" / f"{slug}.html"
            if not hp.exists():
                raise Fail(f"dry-run: committed page missing: {hp}")
            h = hp.read_text(encoding="utf-8")
            probs = check_built_page(it, hp)
            # title-case: committed pages must carry the CORRECT numerals
            for correct, corrupt in roman_corruptions(it["title"]):
                if corrupt in h:
                    probs.append(f"corrupted numeral {corrupt} still in HTML")
                if correct not in h:
                    probs.append(f"correct numeral {correct} missing from HTML")
            px = check_og_pixel(slug)
            if px:
                probs.append(px)
            if probs:
                n_bad += 1
                log(f"  FAIL {slug[:64]}: " + "; ".join(probs))
            else:
                log(f"  PASS {slug[:64]} (.sig/og/badge/flags/words OK)")
        n_stray = stray_scan()
        log(f"  stray headers corpus-wide: {n_stray} (want 0)")
        if n_stray:
            raise Fail(f"stray headers present corpus-wide: {n_stray}")
        if n_bad:
            raise Fail(f"dry-run page checks: {n_bad}/{len(items)} pages FAIL")
        log("  (c) DRY-RUN PASS")
        return
    # ---- real run ----
    workdir = Path(workdir)
    txtdir = workdir / "txt"
    txtdir.mkdir(parents=True, exist_ok=True)
    for it in items:
        shutil.copyfile(REPO / "translations" / (it["slug"] + ".txt"),
                        txtdir / (it["slug"] + ".txt"))
    # clear stale gen4 outputs for these slugs (out/ is cumulative)
    for it in items:
        for p in (GEN4_DIR / "out/ban-dich" / (it["slug"] + ".html"),
                  GEN4_DIR / "out/txt" / (it["slug"] + ".txt"),
                  GEN4_DIR / "out/og" / (f"ban-dich-{it['slug']}.jpg"),
                  GEN4_DIR / "out/og" / (f"ban-dich-{it['slug']}.jpg.sig")):
            if p.exists():
                p.unlink()
    env = dict(os.environ)
    env["GITHUB_TOKEN"] = gh_token()  # transient only; never printed/written
    cmd = [sys.executable, str(GEN4), *[it["slug"] for it in items],
           "--index", str(REPO / "translations/index.json"),
           "--txt-dir", str(txtdir)]
    log("  running gen4 (GITHUB_TOKEN transient, not logged)...")
    r = run(cmd, cwd=str(GEN4_DIR), env=env, check=False)
    log("  gen4 output tail:\n" + "\n".join(r.stdout.splitlines()[-15:]))
    if r.returncode != 0:
        raise Fail(f"gen4 failed ({r.returncode}):\n{r.stderr[-2000:]}")
    for it in items:
        src_h = GEN4_DIR / "out/ban-dich" / (it["slug"] + ".html")
        src_t = GEN4_DIR / "out/txt" / (it["slug"] + ".txt")
        if not src_h.exists() or not src_t.exists():
            raise Fail(f"gen4 did not build {it['slug']} (missing out/ files)")
        shutil.copyfile(src_h, REPO / "ban-dich" / (it["slug"] + ".html"))
        shutil.copyfile(src_t, REPO / "txt" / (it["slug"] + ".txt"))
        log(f"  built ban-dich/{it['slug'][:40]}.html + txt/")
    # title-case fix (output-only) BEFORE og regen (og:title changes with it)
    for it in items:
        hp = REPO / "ban-dich" / (it["slug"] + ".html")
        fixed = fix_titlecase(hp.read_text(encoding="utf-8"), it["slug"], it["title"])
        hp.write_text(fixed, encoding="utf-8")
    # og art-free (gen4's og has Dore art -- never used)
    regen_og_artfree(workdir, items)
    # machine checks on the fresh pages
    problems = []
    for it in items:
        probs = check_built_page(it, REPO / "ban-dich" / (it["slug"] + ".html"))
        px = check_og_pixel(it["slug"])
        if px:
            probs.append(px)
        if probs:
            problems.append(f"{it['slug']}: " + "; ".join(probs))
        else:
            log(f"  PASS {it['slug'][:64]} (.sig/og/badge/flags/words OK)")
    n_stray = stray_scan()
    log(f"  stray headers corpus-wide: {n_stray} (want 0)")
    if n_stray:
        problems.append(f"stray headers corpus-wide: {n_stray}")
    if problems:
        raise Fail("(c) page checks FAIL:\n" + "\n".join(problems))
    log("  (c) PASS")

# ---------------------------------------------- stage (d) search + sitemap --
def stage_d_search_sitemap(manifest, dry_run):
    stage_head("(d) SEARCH + SITEMAP")
    items = manifest["items"]
    sm_path = REPO / "sitemap.xml"
    raw = sm_path.read_text(encoding="utf-8")
    locs_before = raw.count("<loc>")
    # bot-regression tripwires (catalog-bot 60a0be78 lesson)
    for bad in ("nhom-nho/nhom-nho/", "sach/sach/"):
        if bad in raw:
            raise Fail(f"sitemap contains double-path {bad} (bot regression?)")
    for it in items:
        if f"/ban-dich/{it['slug']}.html" in raw:
            raise Fail(f"sitemap already contains {it['slug']} (double-append?)")
    entries = "".join(
        f"<url><loc>{BASE}/ban-dich/{it['slug']}.html</loc></url>" for it in items)
    if dry_run:
        log("  DRY-RUN: no files written. Would append to sitemap.xml:")
        log(f"   {entries[:200]}{'...' if len(entries) > 200 else ''}")
        log(f"  sitemap locs {locs_before} -> {locs_before + len(items)} (simulated)")
        log("  would run: python3 scripts/build_search.py (not run in dry-run)")
        log(f"  search count would go to "
            f"{json.loads((REPO / 'data/search-index.json').read_text(encoding='utf-8'))['count'] + len(items)} (simulated)")
        log("  would revert tim-kiem/index.html to HEAD if build_search.py "
            "rewrites it (known drift)")
        log("  (d) DRY-RUN PASS (simulation only)")
        return {"sitemap_before": locs_before,
                "sitemap_after": locs_before + len(items),
                "search_before": None, "search_after": None}
    if "</urlset>" in raw:
        assert raw.count("</urlset>") == 1, "sitemap has != 1 </urlset>"
        new = raw.replace("</urlset>", entries + "</urlset>", 1)
    else:
        # Legacy fragment format (pre-KT-06, no wrapper): append at EOF.
        log("  NOTE: sitemap.xml has no </urlset> (legacy fragment format) -- "
            "appending at EOF")
        new = raw.rstrip("\n") + entries
    sm_path.write_text(new, encoding="utf-8")
    after = sm_path.read_text(encoding="utf-8")
    assert after.count("<loc>") == locs_before + len(items), \
        "sitemap loc count after append wrong"
    _check = re.sub(r"^<\?xml[^?]*\?>\s*", "", after)
    if "<urlset" not in _check:
        _check = "<root>" + _check + "</root>"
    try:
        ET.fromstring(_check)
    except ET.ParseError as e:
        raise Fail(f"sitemap not well-formed XML after append: {e}")
    log(f"  sitemap locs {locs_before} -> {locs_before + len(items)}")
    search_path = REPO / "data/search-index.json"
    search_before = json.loads(search_path.read_text(encoding="utf-8"))["count"]
    r = run([sys.executable, "scripts/build_search.py"], cwd=str(REPO), check=False)
    log("  build_search.py output tail:\n" + "\n".join(r.stdout.splitlines()[-6:]))
    if r.returncode != 0:
        raise Fail(f"build_search.py failed ({r.returncode}):\n{r.stderr[-2000:]}")
    sdata = json.loads(search_path.read_text(encoding="utf-8"))
    if sdata["count"] != search_before + len(items) \
            or len(sdata["items"]) != sdata["count"]:
        raise Fail(f"search count {sdata['count']} (want "
                   f"{search_before + len(items)}); items {len(sdata['items'])}")
    us = {it.get("u", "").lstrip("/") for it in sdata["items"]}
    missing = [it["slug"] for it in items
               if f"ban-dich/{it['slug']}.html" not in us]
    if missing:
        raise Fail(f"search-index missing slugs: {missing} "
                   "(note: key 'u' carries a leading slash)")
    log(f"  search {search_before} -> {sdata['count']} (all {len(items)} slugs present)")
    # sitemap must be unchanged by build_search (it only reads the sitemap;
    # if it changed, something else moved)
    locs_now = sm_path.read_text(encoding="utf-8").count("<loc>")
    if locs_now != locs_before + len(items):
        raise Fail(f"sitemap locs changed by build_search.py: "
                   f"{locs_before + len(items)} -> {locs_now}")
    # tim-kiem/index.html drift: build_search rewrites it from its template
    diffed = git("diff", "--name-only").split()
    if "tim-kiem/index.html" in diffed:
        run(["git", "-C", str(REPO), "checkout", "HEAD", "--", "tim-kiem/index.html"])
        diffed = git("diff", "--name-only").split()
        assert "tim-kiem/index.html" not in diffed, "tim-kiem revert failed"
        log("  tim-kiem/index.html reverted to HEAD (known build_search drift)")
    log("  (d) PASS")
    return {"sitemap_before": locs_before, "sitemap_after": locs_before + len(items),
            "search_before": search_before, "search_after": sdata["count"]}


def print_commit_commands(manifest, counts):
    n = manifest["round"]
    label = manifest["label"]
    idx_files = ["translations/index.json", "translations/index-lite.json",
                 "translations/index.min.json", "api/data/books-lookup.json"]
    txt_files = [f"translations/{it['slug']}.txt" for it in manifest["items"]]
    page_files = []
    for it in manifest["items"]:
        page_files += [f"ban-dich/{it['slug']}.html", f"txt/{it['slug']}.txt",
                       f"og/ban-dich-{it['slug']}.jpg",
                       f"og/ban-dich-{it['slug']}.jpg.sig"]
    page_files += ["sitemap.xml", "data/search-index.json"]
    log("\n===== COMMIT COMMANDS (Molly runs these; the script never commits) =====")
    log("  # 1. index commit")
    log("  git -C " + str(REPO) + " add " + " ".join(idx_files + txt_files))
    log(f"  git -C {REPO} commit -m \"Vòng {n}: index {label} "
        f"({manifest['index_before']} → {manifest['index_after']})\"")
    log("  git -C " + str(REPO) + " push")
    log("  # 2. pages commit (after verifying the index commit landed)")
    log("  git -C " + str(REPO) + " add " + " ".join(page_files))
    log(f"  git -C {REPO} commit -m \"Vòng {n}: pages {label} "
        f"(sitemap {counts['sitemap_after']}, search {counts['search_after']})\"")
    log("  git -C " + str(REPO) + " push")
    log(f"  # 3. then: python3 tools/round-pipeline.py --round {n} --live")
    log("  # (live-poll needs the push deployed; Vercel lag is 4-25 min)")


def write_state(manifest, counts):
    state = {
        "round": manifest["round"], "label": manifest["label"],
        "slugs": [it["slug"] for it in manifest["items"]],
        "flags": {it["slug"]: it["flags"] for it in manifest["items"]},
        "check_string": {it["slug"]: check_string(it) for it in manifest["items"]},
        "index_lite_after": manifest["index_after"],
        "sitemap_after": counts["sitemap_after"],
        "search_after": counts["search_after"],
    }
    p = COWORK / f"r{manifest['round']}-pipeline-state.json"
    p.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
    log(f"  state file for --live: {p}")
    return p


def check_string(item):
    """Substring the live page must contain (case-insensitive).
    Chapter books: 'Chương <RN>'; other books: first 40 chars of short."""
    m = re.search(r"CHƯƠNG\s+([IVXLCDM0-9]+)", item["title"])
    if m:
        return "Chương " + m.group(1)
    return item["short"][:40]


# ------------------------------------------------------- stage (e) live-poll -
def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "round-pipeline/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()


def stage_e_live_poll(round_no):
    stage_head("(e) LIVE-POLL (runs AFTER Molly commits + pushes)")
    sp = COWORK / f"r{round_no}-pipeline-state.json"
    if not sp.exists():
        raise Fail(f"state file missing: {sp}\nRun stages (a)-(d) first, "
                   "then commit + push, then --live.")
    st = json.loads(sp.read_text(encoding="utf-8"))
    slugs = st["slugs"]
    log_path = HOME / f"workspace/r{round_no}-live-poll.log"
    checks = []
    for s in slugs:
        checks += [(f"page {s[:24]} 200", "page", s),
                   (f"page {s[:24]} title", "title", s),
                   (f"page {s[:24]} badge", "badge", s),
                   (f"page {s[:24]} flags", "flags", s)]
    checks += [("index-lite", "lite", None), ("sitemap", "sitemap", None),
               ("search", "search", None)]
    for s in slugs:
        checks.append((f"og {s[:24]}", "og", s))
    checks.append(("homepage", "home", None))
    total = len(checks)
    log(f"  {total} checks (computed from the check list, never hand-counted): "
        f"{len(slugs)} pages x (200+title+badge+flags) + lite + sitemap + "
        f"search + {len(slugs)} og + homepage")
    deadline = time.time() + 25 * 60
    attempt = 0
    with open(log_path, "a", encoding="utf-8") as lf:
        while time.time() < deadline:
            attempt += 1
            ok = 0
            fails = []
            lf.write(f"=== try {attempt} {time.strftime('%H:%M:%S')} ===\n")
            for name, kind, s in checks:
                good, detail = run_one_live_check(kind, s, st)
                lf.write(("PASS " if good else "FAIL ") + name +
                         ("" if good else f" ({detail})") + "\n")
                if good:
                    ok += 1
                else:
                    fails.append(f"{name}: {detail}")
            msg = f"try {attempt}: {ok}/{total}"
            log(f"  {msg}")
            lf.write(msg + "\n")
            if ok == total:
                log(f"  ALL {total}/{total} PASS -- live-verified")
                lf.write(f"ALL {total}/{total} PASS {time.strftime('%H:%M:%S')}\n")
                return
            if time.time() + 120 > deadline:
                break
            log("  (Vercel lag 4-25 min; an all-404 first try is normal -- retrying "
                "in 120s)")
            time.sleep(120)
    raise Fail(f"live-poll did NOT reach full pass within 25 min "
               f"(last try fails: {fails}). Log: {log_path}\n"
               "Do NOT report failure yet -- re-run --live; deploys lag.")


def run_one_live_check(kind, slug, st):
    try:
        if kind == "page":
            code, _ = fetch(f"{BASE}/ban-dich/{slug}.html")
            return (code == 200, f"code={code}")
        if kind in ("title", "badge", "flags"):
            code, body = fetch(f"{BASE}/ban-dich/{slug}.html")
            if code != 200:
                return False, f"code={code}"
            text = body.decode("utf-8", errors="ignore")
            if kind == "title":
                want = st["check_string"][slug]
                return (want.lower() in text.lower(), f"missing {want!r}")
            if kind == "badge":
                nb = text.count(BADGE)
                return (nb == 1, f"badge={nb}")
            nf = text.count(FLAG_BTN)
            want = st["flags"][slug]
            return (nf == want, f"flags={nf} want={want}")
        if kind == "lite":
            code, body = fetch(f"{BASE}/translations/index-lite.json")
            d = json.loads(body)
            ids = {e["id"] for e in d}
            missing = [s for s in st["slugs"] if s not in ids]
            return (code == 200 and len(d) == st["index_lite_after"] and not missing,
                    f"count={len(d)} want={st['index_lite_after']} missing={missing}")
        if kind == "sitemap":
            code, body = fetch(f"{BASE}/sitemap.xml")
            t = body.decode("utf-8", errors="ignore")
            n = t.count("<loc>")
            missing = [s for s in st["slugs"] if s not in t]
            return (code == 200 and n == st["sitemap_after"] and not missing,
                    f"locs={n} want={st['sitemap_after']} missing={missing}")
        if kind == "search":
            code, body = fetch(f"{BASE}/data/search-index.json")
            d = json.loads(body)
            us = {it.get("u", "").lstrip("/") for it in d["items"]}
            missing = [s for s in st["slugs"]
                       if f"ban-dich/{s}.html" not in us]
            return (code == 200 and d["count"] == st["search_after"] and not missing,
                    f"count={d['count']} want={st['search_after']} missing={missing}")
        if kind == "og":
            code, _ = fetch(f"{BASE}/og/ban-dich-{slug}.jpg")
            return (code == 200, f"code={code}")
        if kind == "home":
            code, body = fetch(f"{BASE}/")
            t = body.decode("utf-8", errors="ignore")
            return (code == 200 and "3.000+" in t, f"code={code}")
    except Exception as e:  # network blip: a failed check, not a crash
        return False, f"error: {e}"
    return False, "unknown check kind"


# ------------------------------------------------------------------- main ---
def preflight(round_no, allow_dirty=False):
    stage_head("PREFLIGHT")
    if not (COWORK / f"VONG-{round_no}-PARALLEL.md").exists():
        raise Fail(f"packet missing: VONG-{round_no}-PARALLEL.md")
    d = DELIV_ROOT / f"round{round_no}"
    if not d.is_dir():
        raise Fail(f"delivery dir missing: {d}")
    st = git_status_ignoring_self()
    if st and not allow_dirty:
        raise Fail("working tree is NOT clean -- commit or stash first:\n" +
                   "\n".join(st[:20]))
    if st:
        log("  --allow-dirty: tree dirty, proceeding anyway (testing only)")
    else:
        log("  working tree clean")
    if not GEN4.exists():
        raise Fail(f"gen4 not found: {GEN4}")
    try:
        import PIL  # noqa: F401
    except ImportError:
        raise Fail("PIL (Pillow) not importable -- needed for the og pixel check")
    tok = gh_token()
    log(f"  gh auth token OK ({len(tok)} chars, not shown)")
    log("  PREFLIGHT PASS")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--round", type=int, required=True, help="round number, e.g. 96")
    ap.add_argument("--dry-run", action="store_true",
                    help="read-only checks + simulated writes (no file is written)")
    ap.add_argument("--live", action="store_true",
                    help="stage (e) live-poll only; run after commit + push")
    ap.add_argument("--level", type=int, default=2,
                    help="index level for new entries (default 2; packets do not state it)")
    ap.add_argument("--by", default="Molly", help="index 'by' field (default Molly)")
    ap.add_argument("--workdir", default=None,
                    help="scratch dir (default ~/workspace/your_files/coworking/round-pipeline-tmp/rNN)")
    ap.add_argument("--allow-dirty", action="store_true",
                    help="skip the clean-tree preflight check (testing only: "
                         "dry-run writes nothing, and stage (b) still asserts "
                         "the exact expected file set in real runs)")
    args = ap.parse_args()
    if args.live and args.dry_run:
        ap.error("--live and --dry-run cannot be combined")
    nn = args.round
    try:
        if args.live:
            stage_e_live_poll(nn)
            log("\nALL STAGES PASS (live)")
            return 0
        preflight(nn, args.allow_dirty)
        workdir = Path(args.workdir) if args.workdir else \
            COWORK / "round-pipeline-tmp" / f"r{nn}"
        workdir.mkdir(parents=True, exist_ok=True)
        stage_head("(a) STAGING-VERIFY")
        manifest = build_manifest(nn, DELIV_ROOT / f"round{nn}")
        log(f"  packet §6 vs .txt: {4 * len(manifest['items'])}/"
            f"{4 * len(manifest['items'])} fields OK "
            f"(title/short/orig/length x {len(manifest['items'])})")
        log("  (a) PASS")
        stage_b_index_write(manifest, args.level, args.by, args.dry_run)
        if not args.dry_run:
            log("  (b) PASS")
        stage_c_pages(manifest, workdir, args.dry_run)
        counts = stage_d_search_sitemap(manifest, args.dry_run)
        if args.dry_run:
            log("\nDRY-RUN COMPLETE: no files were written. "
                "Re-run without --dry-run to execute (after Molly's independent "
                "verification passes and she confirms the go-ahead).")
            return 0
        write_state(manifest, counts)
        print_commit_commands(manifest, counts)
        log("\nSTAGES (a)-(d) PASS. The script stops here by design: it never "
            "commits or pushes. Molly reviews the exception report above (empty "
            "= clean), runs the two commit commands, waits for the Vercel "
            "deploy, then runs --live.")
        return 0
    except Fail as e:
        log(f"\n*** FAIL ***\n{e}")
        log("Run stopped at the first FAIL. Fix the cause (usually a packet "
            "error, a delivery defect, or a bot regression), then re-run. "
            "Nothing was committed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
