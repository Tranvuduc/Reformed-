# Reformed Vietnam – guide for any coding tool

Free Vietnamese Reformed ebook/audio library. Static site on Vercel (+ `api/*.js` serverless, GitHub Actions bots). Site: https://reformed-vietnam.vercel.app

## Rules (read first)
- Work on a **branch**, never directly on `main`. Review the diff before merging.
- Do NOT refactor or split `app.js` / `style.css`. A past automated refactor broke the app.
- Copyright: external Vietnamese books are **link-out only**; never host them. Hosted: public-domain works and our own AI translations (labelled "AI, chưa duyệt").
- Vietnamese copy must be natural church Vietnamese (Hội Thánh, Phúc Âm, Đức Chúa Trời, nhà nhóm). Scripture = Vietnamese 1934 (getBible "vietnamese").
- Author/credit pen name for books: "David".

## Build & check
- `python3 tools/build-pages.py` generates all HTML pages (exec's the other `tools/*.py`). Generated files are committed.
- `node --check app.js` after editing; check `reader.html` inline scripts too.
- Push to `main` -> Vercel deploys. Users must reload twice (service worker `sw.js`, network-first).

## Where things are
- `index.html`, `app.js`, `style.css`: homepage and library (4-step faith journey in `renderTiles`).
- `reader.html`: in-site reader (paging, TTS, translation, Scripture popups). `?id=vn/<slug>` reads `txt/<slug>.txt`; params `pid`, `at`.
- `translations/*.txt`: source of AI Vietnamese translations -> `ban-dich/*.html` and `txt/*.txt` via `tools/vi_books.py`, `tools/static_txt.py`. Keep line count, headings, numbers when polishing.
- `tools/moi_tin.py`: 30-day new-believer path. `tools/reformed101.py`: "Cải Chánh là gì?", pastor page.
- Data: `books.json`, `mg.json`, `vi-books.json`, `audio.json`. API: `api/text.js`, `sync.js`, `tr.js`, `tts.js`.

## Open work
- Pastor review of translations (`translations/review/`); Bible-first lessons; Android test; verify `api/tts`; EPUB (`rv-`) Vietnamese polish. See `translations/PLAN-COMPLETE.md`.
