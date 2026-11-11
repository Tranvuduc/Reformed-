#!/usr/bin/env python3
"""Phase 2 (author pages) — build /a/ pages for Johann Gerhard, Jeremiah
Burroughs and Franciscus Gomarus WITHOUT a full tools/build-pages.py run.

Why a dedicated script: a full build-pages.py run wipes and regenerates
a/ and b/ (3,000+ files) and re-runs authors_plus.py; it is the risky
operation (see AGENTS.md cautions). This script mirrors the patched
author-page loop in build-pages.py (vn merge + vn cards + intro variants)
exactly, so the next full run regenerates these three pages byte-identically.

It does, for the three authors only:
  1. builds a/<slug>.html with the same page()/bcard()/bkgrid() helpers
     (execs build-pages.py lines 1-123, stopping before the a//b/ wipe),
  2. adds the .bio block from tools/author_bios_more.json for the two NEW
     pages (Gerhard, Gomarus) by running authors_plus.py's bio loop
     filtered to those two slugs (Burroughs already has his bio),
  3. links the author name on the 4 affected /ban-dich/ pages
     (Gerhard 1, Gomarus 3) to the new /a/ pages (Burroughs' 12 pages
     are already linked).

Run from the repo root: python3 tools/build_vn_authors.py
"""
import json, os, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
os.chdir(ROOT)
sys.path.insert(0, str(ROOT / "scripts"))

AUTHORS = {
    "johann-gerhard": {
        "name": "Johann Gerhard",
        "sig": ("Johann Gerhard (1582–1637), nhà thần học Lutheran người Đức, được xem là "
                "nhà thần học Tin Lành còn sống vĩ đại nhất thời ông — tác giả 'Suy Ngẫm Thánh' "
                "(Meditationes Sacræ) và bộ 'Loci Theologici'."),
    },
    "jeremiah-burroughs": {
        "name": "Jeremiah Burroughs",
        "sig": ("Jeremiah Burroughs (1599–1646) để lại kiệt tác về sự thỏa lòng trong Đấng Christ — "
                "'món báu vật hiếm có' cho mọi tín hữu."),
    },
    "franciscus-gomarus": {
        "name": "Franciscus Gomarus",
        "sig": ("Franciscus Gomarus (1563–1641), nhà thần học Cải Chánh người Hà Lan, giáo sư tại "
                "Leiden và Groningen — đối thủ chính của Arminius trong cuộc tranh luận về tiền định."),
    },
}
# catalogue author strings per slug (author-slug-map.json is the source)
CATALOGUE_AUTHORS = {
    "johann-gerhard": ["Johann Gerhard"],
    "jeremiah-burroughs": ["Jeremiah Burroughs", "Burroughs"],
    "franciscus-gomarus": ["Franciscus Gomarus"],
}


def load_build_pages_helpers():
    """Exec build-pages.py lines 1-123 (helpers only, before the a//b/ wipe)."""
    src = pathlib.Path("tools/build-pages.py").read_text(encoding="utf-8").splitlines(keepends=True)
    assert src[123].startswith('for d in ("a", "b"):'), src[123]
    g = {"__name__": "__main__"}
    exec("".join(src[:123]), g)
    g["urls"] = ["", "about.html", "tac-gia.html", "tieng-viet.html"]
    return g


def build_pages(g):
    page, bcard, bkgrid, E = g["page"], g["bcard"], g["bkgrid"], g["E"]
    SITE = g["SITE"]
    ia = json.load(open("ia.json", encoding="utf-8")) if os.path.exists("ia.json") else {"a": [], "b": []}
    idx = json.load(open("translations/index.json", encoding="utf-8"))
    for slug_key, meta in AUTHORS.items():
        name = meta["name"]
        items = []
        # IA items (Burroughs only: 15)
        for i, nm in enumerate(ia["a"]):
            if nm == name:
                for r in ia["b"]:
                    if r[0] == i:
                        items.append(bcard(r[1], name, f"https://archive.org/details/{r[2]}",
                                            kicker="Internet Archive", ext=True, desc_=r[3] or None))
        # vn items, catalogue order. Ban-dich slug = translation FILENAME
        # (vi_books.py _normfile), NOT the catalogue id: e.g. id
        # 'ai1-275-excellency-gracious-spirit-burroughs' lives at
        # /ban-dich/burroughs-excellency-gracious-spirit.html.
        vn_items = []
        for e in idx:
            if (e.get("author") or "").strip() in CATALOGUE_AUTHORS[slug_key]:
                _f = (e.get("file") or "")
                if _f.startswith("translations/"):
                    _f = _f[len("translations/"):]
                _vs = os.path.splitext(_f)[0] if _f else None
                assert _vs and os.path.exists(f"translations/{_vs}.txt"), f"no translation file for {e['id']}"
                assert os.path.exists(f"ban-dich/{_vs}.html"), f"no ban-dich page for {e['id']} (slug {_vs})"
                vn_items.append(bcard(e.get("short") or e.get("title") or e["id"], name,
                                      f"/ban-dich/{_vs}.html", kicker="Bản dịch"))
        n_en, n_vn = len(items), len(vn_items)
        n = n_en + n_vn
        assert n >= 1, f"no items for {slug_key}"
        _ips = [p for p in name.replace(".", " ").split() if p and p[0].isalpha()]
        _ini = ((_ips[0][0] + (_ips[-1][0] if len(_ips) > 1 else "")) or "?").upper()
        _mono = (f'<svg class="au-pic" viewBox="0 0 96 96" aria-hidden="true"><circle cx="48" cy="48" r="44" fill="none" stroke="currentColor" stroke-width="2.5"/><circle cx="48" cy="48" r="37" fill="none" stroke="currentColor" stroke-width="1" opacity=".35"/><text x="48" y="61" text-anchor="middle" font-size="30" fill="currentColor" font-family="Georgia,serif">{E(_ini)}</text></svg>')
        if n_vn and n_en:
            _intro = (f"Trang này tập hợp {n_en} tác phẩm của {name} thuộc phạm vi công cộng và {n_vn} bản dịch "
                      "tiếng Việt (bản dịch AI, chưa duyệt). Tất cả đều có thể đọc trực tuyến, nghe đọc thành tiếng "
                      "hoặc tải EPUB/PDF miễn phí trong thư viện Reformed Vietnam.")
        elif n_vn:
            _intro = (f"Trang này tập hợp {n_vn} bản dịch tiếng Việt của {name} (bản dịch AI, chưa duyệt). "
                      "Tất cả đều có thể đọc trực tuyến, nghe đọc thành tiếng hoặc tải EPUB/PDF miễn phí trong "
                      "thư viện Reformed Vietnam.")
        else:
            _intro = (f"Trang này tập hợp {n} tác phẩm của {name} thuộc phạm vi công cộng: sách thần học, bài giảng, "
                      "luận thuyết và tài liệu linh tu của truyền thống Cải Chánh và Thanh giáo. Tất cả đều có thể "
                      "đọc trực tuyến, nghe đọc thành tiếng hoặc tải EPUB/PDF miễn phí trong thư viện Reformed Vietnam.")
        intro = (meta["sig"] + " ") + _intro
        _vn_grid = ('<h2>Bản dịch tiếng Việt</h2>' + bkgrid("".join(vn_items))) if vn_items else ""
        body = (f'<div class="au-head">{_mono}<h1>{E(name)} – sách miễn phí</h1></div>'
                f'<p style="clear:both">{E(intro)}</p>'
                f'<p><a class="btn primary" href="/?q={E(name.split()[-1])}">Mở trong thư viện</a></p>'
                + bkgrid("".join(items)) + _vn_grid)
        ld = {"@context": "https://schema.org", "@type": "CollectionPage",
              "name": f"{name} – sách miễn phí", "inLanguage": "vi",
              "url": f"{SITE}/a/{slug_key}.html"}
        path = f"a/{slug_key}.html"
        old = pathlib.Path(path).read_text(encoding="utf-8") if pathlib.Path(path).exists() else None
        new = page(f"{name} – sách miễn phí, đọc và tải | Reformed Vietnam", intro, path, body, ld)
        pathlib.Path(path).write_text(new, encoding="utf-8")
        print(f"  /a/{slug_key}.html — {n_en} EN + {n_vn} vn, {'written' if new != old else 'unchanged'}")
        # NOTE: the rebuild drops the .bio block (authors_plus adds it);
        # add_bios() below re-adds it for all three pages.


def add_bios():
    """Run authors_plus.py's bio loop filtered to the three slugs only.

    The full loop would also touch 33 bio-less pages (mostly alias
    redirects); filtering keeps this run scoped to these three authors.
    Burroughs' bio is re-added here too, because the rebuild above drops
    the .bio block that authors_plus had added to his page.
    """
    from html import escape as E
    src = pathlib.Path("tools/authors_plus.py").read_text(encoding="utf-8").splitlines(keepends=True)
    assert src[63].startswith("for _sl, _nm"), src[63]
    assert src[77].startswith("# sermon compilation"), src[77]
    g = {"__name__": "__main__", "E": E, "_VT": {}}
    exec("".join(src[:38]), g)          # _AB + bios_more merge
    exec("".join(src[43:63]), g)        # _min/_initials/_monogram/_rel/_apage (skips the _VT build: _vn is [] here)
    # Filter ONLY the loop's iteration: _rel() must still see the FULL _AB
    # list, otherwise the 'related authors' line comes out empty (the
    # filtered list contains only these three authors, self excluded).
    g["_AB_FILTERED"] = [x for x in g["_AB"]
                         if x[0] in (["johann-gerhard"], ["franciscus-gomarus"], ["jeremiah-burroughs"])]
    assert len(g["_AB_FILTERED"]) == 3, f"expected 3 bio entries, got {len(g['_AB_FILTERED'])}"
    _loop = "".join(src[63:77]).replace("in _AB:", "in _AB_FILTERED:", 1)
    exec(_loop, g)                      # bio loop only
    for slug_key in ("johann-gerhard", "franciscus-gomarus", "jeremiah-burroughs"):
        assert 'class="bio"' in pathlib.Path(f"a/{slug_key}.html").read_text(encoding="utf-8"), f"no bio on {slug_key}"
    print("  bios present on all three author pages")


def link_ban_dich_names():
    """Link the author name on the 4 affected /ban-dich/ pages."""
    pairs = [
        ("ban-dich/arch-gerhard-sacred-meditations.html", "Johann Gerhard", "johann-gerhard"),
        ("ban-dich/arch-gomarus-on-the-sacraments.html", "Franciscus Gomarus", "franciscus-gomarus"),
        ("ban-dich/mg1-1114-providence-gomarus.html", "Franciscus Gomarus", "franciscus-gomarus"),
        ("ban-dich/mg1-1225-theses-predestination-gomarus.html", "Franciscus Gomarus", "franciscus-gomarus"),
    ]
    for path, name, slug_key in pairs:
        p = pathlib.Path(path)
        h = p.read_text(encoding="utf-8")
        if f"/a/{slug_key}.html" in h and f">{name}</a>" in h:
            print(f"  already linked on {path}")
            continue
        old = f"<p>{name} · "
        assert h.count(old) == 1, f"{path}: expected 1 author line, found {h.count(old)}"
        p.write_text(h.replace(old, f'<p><a href="/a/{slug_key}.html">{name}</a> · ', 1), encoding="utf-8")
        print(f"  linked author on {path}")


def check_author_pages():
    """Every internal link on the three author pages must resolve.

    A target resolves if it exists on disk OR is tracked in git (the
    sparse checkout does not materialize every directory, e.g. bai-viet/).
    """
    import subprocess
    tracked = set(subprocess.check_output(["git", "ls-files"], text=True).splitlines())
    for slug_key in AUTHORS:
        h = pathlib.Path(f"a/{slug_key}.html").read_text(encoding="utf-8")
        for href in sorted(set(re.findall(r'href="([^"]+)"', h))):
            if href.startswith(("http", "mailto:", "#", "javascript:", "data:", "tel:")):
                continue
            if href.startswith("/?"):
                continue  # site search link, resolves to the library
            rel = href.lstrip("/").split("#")[0].split("?")[0]
            if rel.endswith("/"):
                rel += "index.html"
            ok = (ROOT / rel).exists() or rel in tracked
            assert ok, f"{slug_key}: missing link target {href}"
    print("all author-page links verified")


def main():
    g = load_build_pages_helpers()
    build_pages(g)
    add_bios()
    link_ban_dich_names()
    check_author_pages()
    print("DONE")


if __name__ == "__main__":
    main()
