// Translate a CCEL book to Vietnamese with Claude, resumable, chunk by chunk.
// Usage: ANTHROPIC_API_KEY=... node tools/translate.mjs author/slug [maxChunks]
// Output: vi/<author>/<slug>/0001.txt ... + vi/<author>/<slug>/meta.json
import fs from "node:fs";
import path from "node:path";
const id = process.argv[2], max = +process.argv[3] || 1e9;
if (!/^[a-z0-9_-]+\/[a-z0-9_.-]+$/i.test(id || "")) { console.error("usage: node tools/translate.mjs author/slug [maxChunks]"); process.exit(1); }
const KEY = process.env.ANTHROPIC_API_KEY, MODEL = process.env.MODEL || "claude-sonnet-5-5";
if (!KEY) { console.error("ANTHROPIC_API_KEY missing"); process.exit(1); }
const gl = JSON.parse(fs.readFileSync("tools/glossary.json", "utf8"));
const SITE = process.env.SITE || "https://reformed-vietnam.vercel.app";
const dir = path.join("vi", id); fs.mkdirSync(dir, { recursive: true });
const text = await (await fetch(`${SITE}/api/text?id=${encodeURIComponent(id)}`)).text();
if (text.length < 500) throw new Error("no source text");
// chunk at paragraph boundaries, ~1800 chars
const chunks = []; let cur = "";
for (const p of text.split(/\n\s*\n/)) { if (cur.length + p.length > 1800 && cur) { chunks.push(cur); cur = ""; } cur += (cur ? "\n\n" : "") + p.trim(); }
if (cur) chunks.push(cur);
const sys = `You translate public-domain Reformed Christian literature from English into natural, reverent Vietnamese for Vietnamese Protestant readers. Rules: faithful to the author, no additions or commentary, keep paragraph breaks, keep Scripture references, quote Scripture in the Vietnamese Bible style (Kinh Thánh Tiếng Việt 1934 wording where possible). Use this glossary: ${JSON.stringify(gl)}. Output only the translation.`;
let done = 0;
for (let i = 0; i < chunks.length && done < max; i++) {
  const f = path.join(dir, String(i + 1).padStart(4, "0") + ".txt");
  if (fs.existsSync(f)) continue;
  for (let t = 0; t < 4; t++) {
    const r = await fetch("https://api.anthropic.com/v1/messages", { method: "POST", headers: { "x-api-key": KEY, "anthropic-version": "2023-06-01", "content-type": "application/json" }, body: JSON.stringify({ model: MODEL, max_tokens: 4096, system: sys, messages: [{ role: "user", content: chunks[i] }] }) });
    if (r.ok) { const j = await r.json(); fs.writeFileSync(f, j.content.map((c) => c.text || "").join("")); done++; break; }
    await new Promise((s) => setTimeout(s, 5000 * (t + 1)));
  }
  if (!fs.existsSync(f)) throw new Error("chunk " + (i + 1) + " failed");
}
fs.writeFileSync(path.join(dir, "meta.json"), JSON.stringify({ id, chunks: chunks.length, model: MODEL, machine: true, updated: new Date().toISOString().slice(0, 10) }));
console.log(id, done, "new chunks of", chunks.length);
