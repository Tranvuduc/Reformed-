#!/usr/bin/env python3
"""Shared hub-template helpers for the Phase 2 Learn-module builders.

The pattern is copied verbatim from scripts/build_catechism.py (the
canonical hub-template extractor): font_link / <style> / <header> /
<footer> are pulled from hub.html, '#anchor' hrefs are rebased to '/#…',
and pages are written with head(title, desc, url) + MINI_JS. Keeping it in
one place means the five Phase 2 builders (learning paths, doctrine hubs,
loci index, timeline, confessions) stay small and produce pages that look
like the rest of the hub.

Also provides:
- check_links(html): asserts every internal href in a built page resolves
  to a file in the repo (or to a fragment of a page that exists). External
  http(s) and mailto: links are allowed unchecked. Fails the build loudly
  on a dead link instead of shipping it.
- sitemap_add(urls): appends missing <loc> entries (same pattern as the
  other builders) and returns how many were added.
- write_if_changed(path, content): writes only when different, returns True
  when the file changed.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://reformedvietnam.com"

_hub = (ROOT / "hub.html").read_text(encoding="utf-8")
_font = re.search(r'<link rel="stylesheet" href="data:text/css[^"]*"[^>]*>', _hub).group(0)
_style = re.search(r"<style>.*?</style>", _hub, re.S).group(0)
_header = re.search(r"<header.*?</header>", _hub, re.S).group(0)
_footer = re.search(r"<footer.*?</footer>", _hub, re.S).group(0)
_header = re.sub(r'href="#', 'href="/#', _header)
_footer = re.sub(r'href="#', 'href="/#', _footer)

EXTRA_CSS = """
      .crumb { font-size: 13px; color: var(--ink-soft); margin: 18px 0 0; }
      .crumb a { color: var(--gold-text); }
      .cat-head { text-align: center; max-width: 760px; margin: 18px auto 8px; }
      .cat-head .kicker { color: var(--gold-text); font-weight: 700; letter-spacing: .14em; font-size: 13px; text-transform: uppercase; }
      .cat-head h1 { font-family: "Playfair Display", serif; font-size: clamp(26px, 4.5vw, 38px); margin: 8px 0 10px; line-height: 1.2; }
      .title-band { display: flex; gap: 18px; align-items: center; justify-content: center; margin: 14px auto 18px; max-width: 860px; }
      .medallion { width: 72px; height: 72px; border-radius: 50%; border: 2px solid var(--gold-soft); background: var(--burgundy); color: #fdf6e9; display: flex; flex-direction: column; align-items: center; justify-content: center; flex: 0 0 auto; }
      .medallion .m-big { font-family: "Playfair Display", serif; font-size: 34px; font-weight: 700; line-height: 1; }
      .medallion .m-small { font-size: 9px; letter-spacing: .12em; text-transform: uppercase; opacity: .9; }
      .ai-label { display: inline-block; background: var(--gold-soft); color: #6b4423; font-size: 11.5px; font-weight: 700; padding: 3px 9px; border-radius: 20px; }
      .proof { display: flex; justify-content: space-between; gap: 12px; border-bottom: 1px solid var(--line); padding: 9px 2px; }
      .proof .p-ref { color: var(--gold-text); font-weight: 700; white-space: nowrap; }
      .share-row { display: flex; gap: 10px; align-items: center; justify-content: center; flex-wrap: wrap; margin: 22px 0 8px; }
      .share-row .lbl { color: var(--ink-soft); font-size: 13.5px; }
      .share-row a { color: var(--gold-text); font-weight: 700; }
      .cat-index { max-width: 860px; margin: 20px auto; }
      .band-tint { max-width: 860px; margin: 28px auto 0; padding: 18px 20px; border: 1px solid var(--line); border-radius: 12px; background: rgba(255,255,255,.35); }
      .bt-head { font-family: "Playfair Display", serif; font-size: 22px; margin: 0 0 8px; }
      .cat-band { max-width: 860px; margin: 28px auto 0; }
      .cat-band-head { display: flex; align-items: baseline; gap: 12px; flex-wrap: wrap; border-bottom: 2px solid var(--gold-soft); padding-bottom: 6px; margin-bottom: 12px; }
      .cat-band-head h3 { font-family: "Playfair Display", serif; font-size: 21px; margin: 0; }
      .cat-band-head .rng { color: var(--gold-text); font-weight: 700; font-size: 13px; letter-spacing: .05em; }
      .cat-band p, .cat-band li { color: var(--ink-soft); }
      .cat-band a { color: var(--gold-text); }
      .cat-band ul { margin: 6px 0 0; padding-left: 20px; }
      .cat-band li { margin: 4px 0; }
"""

MINI_JS = """
<script>
(function(){var b=document.querySelector('[data-menu-toggle]'),n=document.querySelector('[data-nav]');if(b&&n)b.addEventListener('click',function(){n.classList.toggle('open')});var t=document.querySelector('[data-to-top]');if(t)t.addEventListener('click',function(e){e.preventDefault();window.scrollTo({top:0,behavior:'smooth'})});})();
</script>
"""

def head(title, desc, url, extra_css=""):
    return f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Reformed Vietnam">
<meta property="og:locale" content="vi_VN">
{_font}
{_style}
<style>{EXTRA_CSS}{extra_css}
</style>
</head>"""

header = _header
footer = _footer

def share_row(url):
    return (f'<div class="share-row"><span class="lbl">Chia sẻ trang này:</span> '
            f'<a href="https://www.facebook.com/sharer/sharer.php?u={url}" target="_blank" rel="noopener">Facebook</a> · '
            f'<a href="https://t.me/share/url?url={url}" target="_blank" rel="noopener">Telegram</a> · '
            f'<a href="mailto:?subject=Reformed%20Vietnam&amp;body={url}">Email</a></div>')

def report_mailto(title):
    from urllib.parse import quote
    subject = quote(f"Báo lỗi nội dung: {title} | Reformed Vietnam")
    return (f'<p style="text-align:center;color:var(--ink-soft);font-size:13px;margin-bottom:34px">'
            f'Thấy lỗi trong nội dung? <a href="mailto:reformedvn@gmail.com?subject={subject}">Báo lỗi nội dung</a>'
            f' — gửi về reformedvn@gmail.com.</p>')

def write_if_changed(path, content):
    path = pathlib.Path(path)
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True

def check_links(html, page):
    """Assert every internal href resolves to a file in the repo.

    Internal = starts with '/' (same site). A link may carry a #fragment;
    the fragment is checked against id="…" anchors in the target file
    when the fragment looks like a verse anchor (v<number>) or a section
    anchor (chu-de-…, …). Links to '/' and to directory URLs must resolve
    to an index.html. External http(s)/mailto links are allowed.
    """
    bad = []
    for href in sorted(set(re.findall(r'href="([^"]+)"', html))):
        if href.startswith(("http", "mailto:", "#", "javascript:", "data:", "tel:")):
            continue
        if href == "/":
            target = ROOT / "index.html"
            if not target.exists():
                bad.append((href, "no index.html"))
            continue
        path_part, _, frag = href.partition("#")
        target = ROOT / path_part.lstrip("/")
        if target.is_dir():
            target = target / "index.html"
        if not target.exists():
            bad.append((href, "missing file"))
            continue
        if frag and (frag.startswith("v") or frag.startswith("chu-de-")):
            text = target.read_text(encoding="utf-8", errors="ignore")
            if f'id="{frag}"' not in text:
                bad.append((href, f"missing anchor #{frag}"))
    if bad:
        print(f"LINK CHECK FAILED in {page}:", file=sys.stderr)
        for href, why in bad:
            print(f"  {href} — {why}", file=sys.stderr)
        sys.exit(1)

def sitemap_add(urls):
    sm_path = ROOT / "sitemap.xml"
    sm = sm_path.read_text(encoding="utf-8")
    added = 0
    for u in urls:
        loc = f"<loc>{BASE}{u}</loc>"
        if loc not in sm:
            sm = sm.replace("</urlset>", f"<url>{loc}</url></urlset>")
            added += 1
    sm_path.write_text(sm, encoding="utf-8")
    return added
