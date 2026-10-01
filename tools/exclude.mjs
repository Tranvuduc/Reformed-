// Shared Reformed-only filter (rules in tools/exclude.json). rows: [authorIdx, title, ...]
import fs from "node:fs";
const ex = JSON.parse(fs.readFileSync(new URL("./exclude.json", import.meta.url), "utf8"));
const DA = new RegExp(ex.deny_au, "i"), DT = new RegExp(ex.deny_ti, "i"), AL = new Set(ex.allow_ia), ALR = new RegExp(ex.allow_ia_re, "i");
export function reformedOnly(names, rows, allowOnly) {
  const keep = rows.filter((r) => { const nm = names[r[0]] || ""; if (DA.test(nm) || DT.test(r[1])) return false; return !allowOnly || AL.has(nm) || ALR.test(nm); });
  const used = [...new Set(keep.map((r) => r[0]))].sort((a, b) => a - b), m = new Map(used.map((o, i) => [o, i]));
  console.log("reformedOnly", rows.length, "->", keep.length);
  return { a: used.map((o) => names[o]), b: keep.map((r) => { const c = r.slice(); c[0] = m.get(r[0]); return c; }) };
}
