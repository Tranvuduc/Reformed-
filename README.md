# Reformed Vietnam
Static site + two Vercel functions. Catalog: books.json (CCEL), mg.json (Monergism, 9Marks), vi.json (Vietnamese titles).
- api/sync.js: cross-device progress sync by secret code (Vercel Blob, env BLOB_READ_WRITE_TOKEN)
- api/text.js: serves CCEL plain text for reader.html
- about.html: set CONTACT to show a takedown email
Deploy: push to a Git-connected Vercel project, or use the Vercel CLI.

## Handoff brief
Static site "Reformed Vietnam" (free Reformed ebook library), live at https://reformed-vietnam.vercel.app (Vercel Hobby).
- index.html / style.css / app.js: catalog UI, EN/VI, saved + progress (localStorage), sync, TTS.
- reader.html: in-site reader. about.html: About + takedown (set `CONTACT` for an email).
- books.json, mg.json, vi.json (Vietnamese titles keyed "author/slug"), desc.json (descriptions + start list).
- api/text.js proxies CCEL plain text (`ccel.org/ccel/{letter}/{author}/{slug}/cache/{slug}.txt`); api/sync.js syncs by secret code via private Vercel Blob.
Open items: contact email, more books, real audio, licensing check, type-label fixes.
Deploy: connect this repo in Vercel (Settings -> Git) so each push deploys.

_Auto-deploy test: 2026-09-30_
