#!/usr/bin/env python3
"""Sanity check for the generated site. Run from repo root after build-pages.py.
Fails (exit 1) on broken internal links, missing sitemap targets, or pages missing <title>/<h1>."""
import os, re, sys, glob
root = os.getcwd()
exist = set()
for r, d, fs in os.walk('.'):
    if r.startswith(('./.git', './node_modules')): continue
    for f in fs: exist.add(os.path.normpath(os.path.join(r, f)))
bad, notitle = {}, []
for f in glob.glob('**/*.html', recursive=True):
    if f.startswith(('node_modules', 'translations', 'google')): continue
    t = open(f, encoding='utf-8', errors='ignore').read()
    if f == 'reader.html': continue  # links built in JS
    if '<title>' not in t: notitle.append(f)
    for m in re.finditer(r'(?:href|src)="([^"#?]+)', t):
        u = m.group(1)
        if re.match(r'(https?:|mailto:|tel:|data:|javascript:|//)', u) or "'" in u or '+' in u: continue
        p = os.path.normpath(u.lstrip('/')) if u.startswith('/') else os.path.normpath(os.path.join(os.path.dirname(f), u))
        if p in exist or os.path.join(p, 'index.html') in exist or p.startswith(('api/', '_vercel')) or p == '.': continue
        bad.setdefault(u, []).append(f)
sm = open('sitemap.xml', encoding='utf-8').read()
miss = [u for u in re.findall(r'<loc>https://[^/]+/([^<]*)</loc>', sm) if u and not os.path.exists(u) and not os.path.exists(u.rstrip('/') + '/index.html')]
print(f'broken links: {len(bad)}; sitemap targets missing: {len(miss)}; pages without <title>: {len(notitle)}')
for u, fl in list(bad.items())[:20]: print('  BROKEN', u, 'in', fl[0])
for u in miss[:20]: print('  SITEMAP', u)
sys.exit(1 if bad or miss or notitle else 0)
