// AI "pastor panel" review of Vietnamese wording. Usage: PROVIDER=x MODEL=y node tools/review.mjs
import fs from 'node:fs';
const P = process.env.PROVIDER, MODEL = process.env.MODEL;
const C = {
  gemini: { url: 'https://generativelanguage.googleapis.com/v1beta/openai', key: process.env.GEMINI_API_KEY },
  groq: { url: 'https://api.groq.com/openai/v1', key: process.env.GROQ_API_KEY },
  mistral: { url: 'https://api.mistral.ai/v1', key: process.env.MISTRAL_API_KEY },
  cerebras: { url: 'https://api.cerebras.ai/v1', key: process.env.CEREBRAS_API_KEY },
  nvidia: { url: 'https://integrate.api.nvidia.com/v1', key: process.env.NVIDIA_API_KEY }
}[P];
const txt = f => fs.readFileSync(f, 'utf8').replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>/g, '').replace(/<[^>]+>/g, ' ').replace(/&nbsp;/g, ' ').replace(/\s+/g, ' ').trim();
const vi = JSON.parse(fs.readFileSync('vi.json', 'utf8'));
const titles = Object.entries(vi).map(([k, v]) => k + ' => ' + v);
const SYS = `You are a senior Vietnamese-speaking Reformed pastor and theologian (Tin Lành, Westminster/Three Forms of Unity tradition) with strong Vietnamese language skills, reviewing a free Vietnamese Reformed library website for doctrinal accuracy and natural Protestant Vietnamese. Avoid Catholic vocabulary (Thiên Chúa, Giáo hội, Giêsu, etc.); Protestant norms: Đức Chúa Trời, Hội Thánh, Chúa Giê-xu/Jesus, Cơ Đốc nhân, thuộc linh, Kinh Thánh. Be specific, candid and concise. Output markdown with: (1) a verdict score /10, (2) a table of concrete problems: item | issue | suggested fix, ordered by severity, (3) what is good. Write findings in English, quote Vietnamese exactly. Do not invent problems; say "OK" when fine.`;
const jobs = [];
for (let i = 0; i < titles.length; i += 70) jobs.push(['Vietnamese book titles (id => VN title; original English authors: Calvin, Owen, Edwards, Bunyan, Ryle, Spurgeon, etc.), part ' + (i / 70 + 1), titles.slice(i, i + 70).join('\n')]);
jobs.push(['About page text (site description and doctrinal stance)', txt('about.html').slice(0, 6000)]);
const lo = txt('lo-trinh.html'); jobs.push(['Reading-plan page (stages and book order for new Reformed readers; judge order, pastoral wisdom, wording)', lo.slice(0, 9000)]);
const tp = fs.readFileSync('tools/topics.py', 'utf8').match(/TOPICS\s*=\s*\[[\s\S]*?\n\]/); if (tp) jobs.push(['Topic hubs definition (names, intros, keyword regex; judge whether the topics, names and keywords are doctrinally sound)', tp[0].slice(0, 7000)]);
let lastE = '';
let out = `# ${P} / ${MODEL}\n\n`;
for (const [name, body] of jobs) {
  let res = '';
  for (let a = 0; a < 3 && !res; a++) {
    try {
      const r = await fetch(C.url + '/chat/completions', { method: 'POST', headers: { 'content-type': 'application/json', authorization: 'Bearer ' + C.key }, body: JSON.stringify({ model: MODEL, temperature: 0.2, max_tokens: 3500, messages: [{ role: 'system', content: SYS }, { role: 'user', content: 'Review this: ' + name + '\n\n' + body }] }) });
      const j = await r.json();
      res = j.choices?.[0]?.message?.content || ''; if (!res) { lastE = r.status + ' ' + JSON.stringify(j).slice(0, 300); console.log(P, r.status, JSON.stringify(j).slice(0, 200)); await new Promise(s => setTimeout(s, 20000)); }
    } catch (e) { lastE = e.message; console.log(P, e.message); await new Promise(s => setTimeout(s, 10000)); }
  }
  out += `## ${name}\n\n${res || '(no response) ' + lastE}\n\n`;
  await new Promise(s => setTimeout(s, P === 'groq' ? 25000 : 6000));
}
fs.mkdirSync('review', { recursive: true });
fs.writeFileSync(`review/${P}.md`, out);
