# Reformed Vietnam
Static site + five Vercel functions. Catalog: books.json (CCEL), mg.json (Monergism, 9Marks), vi.json (Vietnamese titles).
- api/sync.js: cross-device progress sync by secret code (Vercel Blob, env BLOB_READ_WRITE_TOKEN). Storage failure answers 503 — never 200 `ok:true` for an unpersisted write; the client (app.js) shows "not synced yet, will retry" + last-sync time and retries with backoff. GET failure also answers 503, never an empty state.
- api/text.js: serves CCEL plain text for reader.html. GET only, 9s upstream timeout, 12MB cap, `id` validated.
- api/tr.js: shared machine-translation cache (Vercel Blob). GET is public (read a cached translation, `?stats` for bot status). POST never accepts client-supplied translation text: the reader sends SOURCE paragraphs only; the server verifies them against the canonical CCEL text and translates them itself (Google gtx, then MyMemory fallback), first-write-wins. Bot/admin writes (status reports, overwriting a poisoned entry) require `Authorization: Bearer <TR_WRITE_TOKEN>` (Vercel env var, never shipped to the browser); if the var is unset those branches answer 503. POST brake: 120/hour per IP, per instance (see note below).
- api/tts.js: Google Translate TTS proxy. GET only, 8s upstream timeout, `q` ≤ 200 chars, same per-instance brake (120/hour per IP).
- api/chat.js: AI chat (Groq first, Gemini fallback; no key → 503 `not_ready`). Per-instance per-IP brake: 10/hour, 50/day. That brake is honest about its limits: serverless runs many instances with separate memory, so it is a spam brake, not a global quota — the providers' own 429 quotas are the real $0 guard. A Groq timeout deliberately does NOT fall back to Gemini (a timeout usually means the other provider is timing out too; retrying only makes the user wait longer).
- Security headers (vercel.json): CSP + HSTS + X-Frame-Options DENY + Permissions-Policy. The CSP allowlist is derived from the site's real loads (Google Fonts, jsDelivr for Piper TTS, cdnjs for JSZip, giscus.app, YouTube-nocookie embed, getBible/MyMemory/Google-translate APIs). `script-src` keeps `'unsafe-inline'` because the site has many inline scripts — so the CSP constrains external loads, connect targets, framing and objects, but is NOT a full XSS barrier; the real XSS defence is escaping (esc() in reader.html/app.js escapes `&<>"'`) plus the closed tr.js write path above.
- about.html: set CONTACT to show a takedown email
Deploy: push to a Git-connected Vercel project, or use the Vercel CLI.
Env vars (Vercel dashboard, never in the repo): BLOB_READ_WRITE_TOKEN, GROQ_API_KEY, GEMINI_API_KEY, TR_WRITE_TOKEN.

## Handoff brief
Static site "Reformed Vietnam" (free Reformed ebook library), live at https://reformedvietnam.com (Vercel Hobby).
- index.html / style.css / app.js: catalog UI, EN/VI, saved + progress (localStorage), sync, TTS.
- reader.html: in-site reader. about.html: About + takedown (set `CONTACT` for an email).
- books.json, mg.json, vi.json (Vietnamese titles keyed "author/slug"), desc.json (descriptions + start list).
- api/text.js proxies CCEL plain text (`ccel.org/ccel/{letter}/{author}/{slug}/cache/{slug}.txt`); api/sync.js syncs by secret code via private Vercel Blob.
Open items: contact email, more books, real audio, licensing check, type-label fixes.
Deploy: connect this repo in Vercel (Settings -> Git) so each push deploys.

_Auto-deploy test: 2026-09-30_

## Our own Vietnamese translations
EPUBs live in `sach/<slug>.epub`. `python3 tools/build-vn-books.py` builds the reading page `doc/<slug>.html`, extracts the cover `sach/<slug>.jpg`, and adds an `rv-<slug>` entry to the top of `mg.json` → `vn`. Then run `python3 tools/build-pages.py` to refresh `tieng-viet.html`, topic pages and `sitemap.xml`. To add a book: drop the EPUB in `sach/` and add one line to `BOOKS` in the script.
