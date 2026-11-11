#!/usr/bin/env python3
"""Phase 3.6 — "Sach moi them" (recently added books).

Derives the newest Vietnamese translations from git history: the date a
book's ban-dich/<slug>.html page FIRST appeared in the repo is the date it
entered the library. No catalogue dates are invented — the catalogue
(translations/index.json) carries no added-date field.

Honesty guard: this repo is a SHALLOW clone whose earliest commit is
2026-11-05, and 2,932 ban-dich pages first appear in that boundary commit
(the bulk import). Those are NOT true addition dates, so every file whose
first appearance is on the boundary date is EXCLUDED. Only books added
after the boundary (2026-11-06 onward) are listed, newest first.

Outputs (all committed):
  1. tools/recent-books.json — top 30, machine-readable, reused by
     tools/vi_books.py for the "Moi them gan day" block on ban-dich/.
  2. A "Sach moi them" section (top 12) injected into index.html and
     hub.html, right before the giao-ly section, between
     <!-- RV-RECENT-START --> / <!-- RV-RECENT-END --> markers
     (re-running replaces the block in place). index.html is also copied
     to ~/workspace/your_files/reformed-vietnam-phase-a/index.html,
     the standing Phase-A mirror.

Re-run after each translation round lands to refresh the list.
Run from the repo root:  python3 scripts/build_recent.py
"""
import json, os, re, shutil, subprocess
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
TODAY = date.today().isoformat()
TOP_JSON = 30
TOP_HOME = 12


def _normfile(f):
    if not f:
        return None
    if f.startswith("translations/"):
        f = f[len("translations/"):]
    return os.path.splitext(f)[0]


def _titlecase_vi(t):
    """Same display rule as tools/vi_books.py (M7): titlecase only when the
    whole title is uppercase; acronyms/numerals stay verbatim. Kept local
    so this script stays standalone."""
    if not t or not t.isupper():
        return t
    _out = []
    for _w in t.split(" "):
        _core = _w.strip(".,;:!?()\"'«»—–-")
        if _core in {"WSC", "KJV", "NKJV", "ESV", "NASB", "NIV", "BDM", "CCEL",
                     "EPUB", "PDF", "MP3", "URL", "HTML", "AI", "DVD", "CD",
                     "BD", "NT", "OT"} or (re.match(r"^[IVXLCDM]+$", _core or "") and len(_core) <= 5):
            _out.append(_w)
        else:
            _out.append(_w.capitalize())
    return " ".join(_out)


def git_first_seen():
    """slug -> first-appearance date (YYYY-MM-DD) for ban-dich pages."""
    out = subprocess.run(
        ["git", "log", "--diff-filter=A", "--name-only",
         "--format=COMMIT %ad", "--date=short", "--", "ban-dich/"],
        capture_output=True, text=True, check=True).stdout
    cur, seen = None, {}
    for line in out.splitlines():
        if line.startswith("COMMIT "):
            cur = line[7:].strip()
        elif line.strip():
            f = line.strip()
            if f.endswith(".html") and f not in seen:
                seen[f] = cur
    return seen


def boundary_date():
    out = subprocess.run(
        ["git", "log", "--format=%ad", "--date=short"],
        capture_output=True, text=True, check=True).stdout
    dates = [l.strip() for l in out.splitlines() if l.strip()]
    return dates[-1] if dates else None


def catalogue():
    idx = json.load(open("translations/index.json", encoding="utf-8"))
    cat = {}
    for r in idx:
        s = _normfile(r.get("file"))
        if not s:
            continue
        t = r.get("title") or r.get("short") or (r.get("vi") or {}).get("t") or ""
        a = r.get("author") or r.get("a") or ""
        cat[s] = (_titlecase_vi(t), a)
    return cat


def vn_date(iso):
    y, m, d = iso.split("-")
    return f"{int(d)}/{int(m)}/{y}"


def section_html(books):
    items = "".join(
        f'<li><a href="/ban-dich/{b["slug"]}.html">{b["title"]}</a>'
        f'<span class="rv-ra">{b["author"]}</span>'
        f'<span class="rv-rd">thêm ngày {vn_date(b["date"])}</span></li>\n            '
        for b in books)
    return (
        '      <!-- RV-RECENT-START -->\n'
        '      <style>.rv-recent{list-style:none;margin:18px 0 0;padding:0;border-top:1px solid var(--line)}'
        '.rv-recent li{display:flex;flex-wrap:wrap;gap:4px 10px;align-items:baseline;padding:10px 2px;border-bottom:1px solid var(--line)}'
        '.rv-recent li a{font-weight:600;text-decoration:none}.rv-recent li a:hover{text-decoration:underline}'
        '.rv-recent .rv-ra{color:var(--muted);font-size:.88rem}'
        '.rv-recent .rv-rd{margin-left:auto;color:var(--muted);font-size:.85rem;white-space:nowrap}</style>\n'
        '      <section class="section" id="moi-them">\n'
        '        <div class="wrap">\n'
        '          <div class="section-head">\n'
        '            <div class="rule"></div>\n'
        '            <h2>Sách mới thêm</h2>\n'
        '            <p>Những bản dịch mới nhất vừa vào thư viện — mới nhất ở trên cùng.</p>\n'
        '          </div>\n'
        '          <ul class="rv-recent">\n'
        f'            {items}'
        '          </ul>\n'
        '          <div style="text-align:center;margin-top:20px"><a class="btn solid" href="/ban-dich/">Xem tất cả bản dịch →</a></div>\n'
        '        </div>\n'
        '      </section>\n'
        '      <!-- RV-RECENT-END -->\n')


def inject(path, block):
    text = open(path, encoding="utf-8").read()
    pat = re.compile(r"      <!-- RV-RECENT-START -->.*?      <!-- RV-RECENT-END -->\n",
                     re.S)
    if pat.search(text):
        text = pat.sub(block, text, count=1)
        changed = "replaced"
    else:
        anchor = '      <section class="section" id="giao-ly">'
        if anchor not in text:
            raise SystemExit(f"{path}: anchor giao-ly section not found")
        text = text.replace(anchor, block + anchor, 1)
        changed = "inserted"
    open(path, "w", encoding="utf-8").write(text)
    return changed


def main():
    bound = boundary_date()
    seen = git_first_seen()
    cat = catalogue()
    books = []
    for f, d in seen.items():
        if d == bound:
            continue  # shallow-clone boundary bulk import: not a real date
        slug = os.path.splitext(os.path.basename(f))[0]
        if not os.path.exists(f"ban-dich/{slug}.html"):
            continue
        if slug not in cat:
            continue
        title, author = cat[slug]
        books.append({"slug": slug, "title": title, "author": author,
                      "date": d})
    books.sort(key=lambda b: (b["date"], b["slug"]), reverse=True)
    top = books[:TOP_JSON]
    payload = {
        "generated": TODAY,
        "boundary_excluded": bound,
        "note": ("Ngay them = ngay trang ban-dich/ cua sach xuat hien lan dau "
                 "trong git (sau ngay gioi han shallow clone). Khong co ngay "
                 "nao duoc tu suy ra cho sach cu hon."),
        "books": top,
    }
    with open("tools/recent-books.json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    block = section_html(top[:TOP_HOME])
    for path in ("index.html", "hub.html"):
        print(path, inject(path, block))
    mirror = os.path.expanduser(
        "~/workspace/your_files/reformed-vietnam-phase-a/index.html")
    if os.path.exists(mirror):
        shutil.copyfile("index.html", mirror)
        print("phase-a mirror updated")
    print(f"recent: {len(books)} books with real post-boundary dates "
          f"(boundary {bound} excluded); newest: "
          + ", ".join(f'{b["slug"]} ({b["date"]})' for b in top[:3]))


if __name__ == "__main__":
    main()
