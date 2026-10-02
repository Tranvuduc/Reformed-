# Developer Guide

This project is a static, client-side library for Reformed books and reading material. The app is intentionally lightweight and hosted on Vercel, but it is still a fairly large single-page app.

## Project structure

- `index.html` — landing page, filter bar, book grid, hero UI
- `style.css` — all site styling
- `app.js` — core catalog logic, rendering, filtering, sync, and interaction behavior
- `reader.html` — in-page reader for public-domain or linked content
- `about.html` — project/about page and contact info
- `books.json` — main library catalog
- `mg.json` — Monergism / free ebook entries
- `vi.json` — Vietnamese catalog entries
- `desc.json` — descriptions and curated shelf metadata
- `api/sync.js` — secret-code sync across devices via Vercel Blob
- `api/text.js` — CCEL text proxy for the reading experience
- `tools/` — data-generation and translation utilities

## Primary data model

The app relies on a few recurring structures:

- `BOOKS`: array of book objects used by the library UI
- `DESC[id]`: optional description lookup for a given book ID
- `st`: app state object, including filters, selected language, saved books, and reading progress
- `prog[id]`: reading progress and status for each book
- `localStorage`: persistence for language, saved books, progress, and sync code

Most of the logic lives in `app.js`, and the biggest source of maintenance risk is that it mixes UI rendering, catalog expansion, filters, sync logic, and app state in one place.

## When making changes

### Editing catalog data
- Update `books.json`, `mg.json`, `vi.json`, or `desc.json` when adding or adjusting library entries.
- Keep keys consistent (`author/slug` style for many records, as the code expects them in several places).
- If a title is a public-domain or externally linked resource, ensure the metadata still matches the actual external link and permissions.

### Editing UI behavior
- `index.html` contains the main structure for the landing page.
- `style.css` controls layout and responsiveness.
- `app.js` is where filters, sorting, “start here” recommendations, saved books, and sync are handled.

### Adding a new page or section
- Keep the page static and lightweight.
- Reuse the same design conventions from existing pages.
- Keep relative links consistent to avoid broken navigation.

## Good maintenance habits

- Do small, reviewable changes.
- Prefer function-level edits over large in-place rewrites.
- If you touch data conventions, update the matching logic in `app.js` too.
- For UI changes, test both mobile and desktop widths because the site is heavily responsive.
- Because the app stores user state in `localStorage`, be careful not to break backwards compatibility during updates.

## Local validation

A simple local validation flow is enough for this project:

1. Open the site in a browser locally.
2. Check the home page loads and filters work.
3. Test search, language toggle, saved books, and reading progress.
4. Confirm the data files still parse (`books.json`, `desc.json`, etc.).
5. For sync features, verify the Vercel environment and credentials are set correctly before testing on deployed builds.

## Planned cleanup

This repo is currently a fast-moving static app. The next stage of maintenance should be a cleanup pass to split `app.js` into smaller modules and centralize the state and constants. That will make the UI easier to modify safely without causing regressions.
