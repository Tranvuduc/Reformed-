// GET /api/epub?id=<book-id>  (vd: ?id=knox/prayer)
// Tạo EPUB on-demand cho sách đã dịch — KHÔNG thêm file tĩnh vào repo
// (Vercel deployment storage đang đầy). Nội dung lấy từ file translations/*.txt
// đã deploy, parse cấu trúc markdown-lite (#, ##, ###) rồi build EPUB 3
// bằng ZIP writer thuần Node (không cần npm dependency).
import zlib from 'node:zlib';

const ID_OK = /^[a-z0-9_.\-/]+$/i;
const FILE_OK = /^[a-z0-9_.-]+\.txt$/i;
const UA = { 'User-Agent': 'ReformedVietnamEPUB/1.0' };

// ---------- CRC32 ----------
const CRC_T = (() => {
  const t = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = (c & 1) ? (0xedb88320 ^ (c >>> 1)) : (c >>> 1);
    t[n] = c >>> 0;
  }
  return t;
})();
function crc32(buf) {
  let c = 0xffffffff;
  for (let i = 0; i < buf.length; i++) c = CRC_T[(c ^ buf[i]) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}

// ---------- ZIP writer tối thiểu (mimetype STORE đầu tiên, còn lại DEFLATE) ----------
function zipBuild(files) {
  const body = [], central = [];
  let off = 0;
  for (const f of files) {
    const name = Buffer.from(f.name, 'utf8');
    const raw = Buffer.isBuffer(f.data) ? f.data : Buffer.from(f.data, 'utf8');
    const comp = f.store ? raw : zlib.deflateRawSync(raw, { level: 9 });
    const crc = crc32(raw), method = f.store ? 0 : 8;
    const lh = Buffer.alloc(30);
    lh.writeUInt32LE(0x04034b50, 0); lh.writeUInt16LE(20, 4);
    lh.writeUInt16LE(0x0800, 6); lh.writeUInt16LE(method, 8);
    lh.writeUInt32LE(crc, 14);
    lh.writeUInt32LE(comp.length, 18); lh.writeUInt32LE(raw.length, 22);
    lh.writeUInt16LE(name.length, 26);
    body.push(lh, name, comp);
    central.push({ name, crc, cl: comp.length, rl: raw.length, method, off });
    off += 30 + name.length + comp.length;
  }
  const cdOff = off, cd = [];
  for (const c of central) {
    const h = Buffer.alloc(46);
    h.writeUInt32LE(0x02014b50, 0); h.writeUInt16LE(20, 4); h.writeUInt16LE(20, 6);
    h.writeUInt16LE(0x0800, 8); h.writeUInt16LE(c.method, 10);
    h.writeUInt32LE(c.crc, 16); h.writeUInt32LE(c.cl, 20); h.writeUInt32LE(c.rl, 24);
    h.writeUInt16LE(c.name.length, 28); h.writeUInt32LE(c.off, 42);
    cd.push(h, c.name);
  }
  const cdBuf = Buffer.concat(cd), end = Buffer.alloc(22);
  end.writeUInt32LE(0x06054b50, 0);
  end.writeUInt16LE(central.length, 8); end.writeUInt16LE(central.length, 10);
  end.writeUInt32LE(cdBuf.length, 12); end.writeUInt32LE(cdOff, 16);
  return Buffer.concat([...body, cdBuf, end]);
}

// ---------- XML helpers ----------
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const inline = (s) => esc(s)
  .replace(/\*\*([^*\n]+)\*\*/g, '<strong>$1</strong>')
  .replace(/\*([^*\n]+)\*/g, '<em>$1</em>'); // *nghiêng* -> em

// ---------- Parse markdown-lite của translations/*.txt ----------
function parseBook(text) {
  const blocks = []; // {h:0|2|3, t}
  const paras = text.replace(/\r/g, '').split(/\n\s*\n/);
  for (const p of paras) {
    const t = p.trim();
    if (!t) continue;
    const m = t.match(/^(#{1,3})\s+(.*)$/s);
    if (m) {
      const lvl = m[1].length;
      if (lvl === 1) continue; // # tiêu đề sách -> dùng title từ index
      blocks.push({ h: lvl, t: m[2].replace(/\s+/g, ' ').trim() });
    } else {
      blocks.push({ h: 0, t });
    }
  }
  return blocks;
}

function buildEpub({ id, title, author, orig, text }) {
  const blocks = parseBook(text);
  // Gom thành chương theo ## ; fallback: cắt mỗi ~120 blocks
  let chaps = [], cur = null;
  const heads2 = blocks.filter((b) => b.h === 2).length;
  if (heads2 >= 3 && heads2 <= 400) {
    for (const b of blocks) {
      if (b.h === 2) { cur = { t: b.t, blocks: [] }; chaps.push(cur); }
      else { if (!cur) { cur = { t: title, blocks: [] }; chaps.push(cur); } cur.blocks.push(b); }
    }
  } else {
    for (let i = 0; i < blocks.length; i += 120)
      chaps.push({ t: `${title} — phần ${chaps.length + 1}`, blocks: blocks.slice(i, i + 120) });
  }
  // Chương quá dài -> chẻ nhỏ
  const final = [];
  for (const c of chaps) {
    for (let i = 0; i < c.blocks.length; i += 300)
      final.push({ t: i ? `${c.t} (tt)` : c.t, blocks: c.blocks.slice(i, i + 300) });
  }

  const css = 'body{font-family:serif;line-height:1.6;margin:5%}h1{text-align:center}h2{margin-top:1.5em}.nr{color:#777;font-size:.85em}';
  const xhtml = (inner, t) =>
    `<?xml version="1.0" encoding="utf-8"?><html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"><head><title>${esc(t)}</title><link rel="stylesheet" href="style.css" type="text/css"/></head><body>${inner}</body></html>`;
  const blk = (b) =>
    b.h === 3 ? `<h3>${inline(b.t)}</h3>`
      : b.h === 2 ? `<h2>${inline(b.t)}</h2>`
        : `<p>${inline(b.t).replace(/\n/g, '<br/>')}</p>`;

  const files = [{ name: 'mimetype', data: 'application/epub+zip', store: true }];
  // Trang bìa + ghi chú bản dịch
  const cover = `<h1>${esc(title)}</h1><p style="text-align:center">${esc(author || '')}</p>` +
    (orig ? `<p style="text-align:center"><i>${esc(orig)}</i></p>` : '') +
    `<p class="nr">Bản dịch do AI hỗ trợ, chưa được mục sư duyệt giáo lý. Thuật ngữ có thể chưa chính xác; hãy đối chiếu với bản gốc và Kinh Thánh.</p>`;
  files.push({ name: 'OEBPS/style.css', data: css });
  files.push({ name: 'OEBPS/cover.xhtml', data: xhtml(cover, title) });

  let man = '', spine = '<itemref idref="cover"/>', nav = '';
  man += '<item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>';
  nav += `<li><a href="cover.xhtml">${esc(title)}</a></li>`;
  final.forEach((c, n) => {
    const f = `c${n}.xhtml`;
    const body = `<h2>${inline(c.t)}</h2>` + c.blocks.map(blk).join('');
    files.push({ name: 'OEBPS/' + f, data: xhtml(body, c.t) });
    man += `<item id="c${n}" href="${f}" media-type="application/xhtml+xml"/>`;
    spine += `<itemref idref="c${n}"/>`;
    nav += `<li><a href="${f}">${esc(c.t)}</a></li>`;
  });
  files.push({
    name: 'OEBPS/nav.xhtml',
    data: xhtml(`<nav epub:type="toc"><h1>Mục lục</h1><ol>${nav}</ol></nav>`, 'Mục lục'),
  });
  files.push({
    name: 'OEBPS/content.opf',
    data: `<?xml version="1.0" encoding="utf-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="u"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="u">reformed-vietnam-${esc(id)}</dc:identifier><dc:title>${esc(title)}</dc:title><dc:creator>${esc(author || 'Reformed Vietnam')}</dc:creator><dc:language>vi</dc:language><meta property="dcterms:modified">${new Date().toISOString().slice(0, 19)}Z</meta></metadata><manifest><item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/><item id="css" href="style.css" media-type="text/css"/>${man}</manifest><spine>${spine}</spine></package>`,
  });
  files.push({
    name: 'META-INF/container.xml',
    data: '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>',
  });
  return zipBuild(files);
}

export default async function handler(req, res) {
  const id = String(req.query.id || '');
  if (!ID_OK.test(id) || id.length > 120 || id.includes('..'))
    return res.status(400).send('bad id');
  const host = req.headers['x-forwarded-host'] || req.headers.host;
  if (!host) return res.status(400).send('no host');
  const base = `https://${host}`;
  try {
    const ir = await fetch(`${base}/translations/index.json`, { headers: UA });
    if (!ir.ok) return res.status(502).send('index unavailable');
    const idx = await ir.json();
    const book = idx.find((b) => b.id === id && !b.hold && b.file);
    if (!book || !FILE_OK.test(book.file)) return res.status(404).send('book not found');
    const tr = await fetch(`${base}/translations/${book.file}`, { headers: UA });
    if (!tr.ok) return res.status(404).send('text not found');
    const text = await tr.text();
    if (text.length > 8000000) return res.status(413).send('too big');

    const epub = buildEpub({
      id, title: book.title || id, author: book.author || '', orig: book.orig || '', text,
    });
    const slug = book.file.replace(/\.txt$/i, '');
    res.setHeader('Content-Type', 'application/epub+zip');
    res.setHeader('Content-Disposition', `attachment; filename="${slug}.epub"`);
    res.setHeader('Cache-Control', 'public, s-maxage=86400, stale-while-revalidate=604800');
    res.status(200).send(epub);
  } catch (e) {
    res.status(502).send('epub error');
  }
}
