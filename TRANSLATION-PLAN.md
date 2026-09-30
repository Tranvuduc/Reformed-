# Plan: 1,000 Vietnamese books

**Reality check.** Free, legally reusable Vietnamese Reformed books number in the low hundreds at most (Tiên Phong, 9Marks, scattered ministry sites). They cannot reach 1,000 by linking. The realistic route is translating public-domain English works, which is legal because the originals are public domain (CCEL, Gutenberg, Archive).

## Pipeline (built)
- `tools/translate.mjs <author/slug>`: pulls CCEL text, splits into ~1,800-char chunks, translates each with Claude using `tools/glossary.json` (fixed Reformed terms), saves `vi/<id>/NNNN.txt`. Resumable.
- `.github/workflows/translate.yml`: run from GitHub Actions ("Translate book", input the id). Needs repo secret `ANTHROPIC_API_KEY`.
- `tools/priority.json`: tier 1 = 40 best-known titles (start here), tier 2 = remaining described titles.

## Scale
One 100,000-word book is about 130k tokens in and about 260k tokens out (Vietnamese uses more tokens). So: 10 books = 4M tokens, 100 books = 40M, 1,000 books = 400M. Start with tier 1 and check cost before scaling.

## Phases
1. **Pilot (this week):** add the API secret, translate 3 short works (Pilgrim's Progress, a Spurgeon sermon set, Westminster Shorter Catechism). Have a Vietnamese pastor review 10 pages.
2. **Reader support:** VI/EN toggle in `reader.html` reading `vi/<id>/` chunks; show "Bản dịch máy, chưa hiệu đính" on every translated book.
3. **Tier 1 (40 books):** translate, publish, announce on the Facebook page.
4. **Review loop:** reader "Báo lỗi dịch" link opens a prefilled GitHub issue or email to reformedvn@gmail.com.
5. **Scale to 100, then 300** by demand (saved/read counts). 1,000 only if review capacity exists.

## Quality and legal
- Label all machine translation as such; do not call it authoritative.
- Bible quotes: use the 1934 Vietnamese Bible style (public domain).
- Translate only public-domain originals; never modern copyrighted books without permission.
- Keep the original author credit and source on every page.

## Ways to get real Vietnamese books faster
- Ask Tiên Phong, 9Marks Vietnamese, Thư Viện Tin Lành, and Vietnamese seminaries for permission to host or link (draft in the promo doc).
- Paste any Vietnamese book links you find; I add them to `mg.json` (`vn`).
