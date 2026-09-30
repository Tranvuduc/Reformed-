# Reformed Vietnam
Static site + two Vercel functions. Catalog: books.json (CCEL), mg.json (Monergism, 9Marks), vi.json (Vietnamese titles).
- api/sync.js: cross-device progress sync by secret code (Vercel Blob, env BLOB_READ_WRITE_TOKEN)
- api/text.js: serves CCEL plain text for reader.html
- about.html: set CONTACT to show a takedown email
Deploy: push to a Git-connected Vercel project, or use the Vercel CLI.
