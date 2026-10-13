# Executed from build-pages.py after nang_cap2.py.
# Data-driven features: tra-kinh-thanh (+kt/*.json), giao-ly-hang-ngay, nhom-nho (+nhom-nho/*.html), ke-hoach-doc.
# Content features live in tools/nang_cap3b.py (exec'd at the end).
import json as _j3, re as _r3, os as _o3, collections as _c3, urllib.parse as _up3, math as _m3

_NC3 = _NC + '<style>.sel{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0}.sel select,.sel input{padding:8px;border-radius:8px;border:1px solid #8885;background:inherit;color:inherit;font:inherit;min-width:0}.rs a{font-weight:600}.rs li{margin:.5em 0}.ct{display:inline-block;margin:2px 3px;padding:3px 9px;border-radius:99px;background:#8882;font-size:.88rem;cursor:pointer;border:0;color:inherit}.ct.on{background:var(--acc,#8b5a2b);color:#fff}.q{margin:.3em 0}.print-only{display:none}@media print{nav,footer,.noprint,button{display:none!important}.print-only{display:block}}</style>'
_idx3 = _j3.load(open("translations/index.json", encoding="utf-8"))
_pub3 = [b for b in _idx3 if not b.get("hold") and _o3.path.exists("txt/" + b["file"])]
_bkv3 = _j3.loads(_r3.search(r'var BKV=(\{.*?\}),BKVRE', open("reader.html", encoding="utf-8").read(), _r3.S).group(1))
_bkre3 = _r3.compile(r"(?<![\w])(" + "|".join(_r3.escape(x) for x in sorted(_bkv3, key=len, reverse=True)) + r")\s(\d{1,3}):(\d{1,3})(?:[-–](\d{1,3}))?", _r3.I | _r3.U)
_VN66 = [x[0] for x in _BK]  # Vietnamese names in canonical order (from nang_cap2)

def _stem3(b): return _o3.path.splitext(b["file"])[0]
def _blocks3(text):
    """Mirror the reader's paragraph build: blocks split on blank lines, joined by space. Returns [(text, offset)]"""
    out, pos = [], 0
    for m in _r3.finditer(r"(?:[^\n]*\S[^\n]*(?:\n(?![ \t]*\n)[^\n]*)*)", text):
        t = " ".join(x.strip() for x in m.group(0).split("\n") if x.strip())
        t = _r3.sub(r"\s{2,}", " ", t)
        if len(t) >= 2: out.append((t, m.start()))
    return out
def _anchor3(t):
    a = t[:46]
    if len(t) > 46 and " " in a: a = a[:a.rstrip().rfind(" ")] if a[-1] != " " else a
    return a.strip()
def _hdr_end3(text):
    # reader strips everything before the first '# ' title line region ('*** START' style); our txt has a header block, keep all, mirror not needed for anchors
    return 0

_B3 = {}   # stem -> dict(title, author, blocks, chars)
for _b in _pub3:
    _t = open("txt/" + _b["file"], encoding="utf-8").read()
    _bl = _blocks3(_t)
    _B3[_stem3(_b)] = {"title": _b.get("title", ""), "author": _b.get("author", ""), "blocks": _bl, "chars": sum(len(x[0]) for x in _bl)}

# ---------- 1. Tra cuu theo Kinh Thanh ----------
_kt = {}   # book -> chapter -> stem -> [count, set(verses), anchor]
for _s, _d in _B3.items():
    for _t, _off in _d["blocks"]:
        for _m in _bkre3.finditer(_t):
            _bk = _bkv3[_m.group(1).lower()]; _ch = int(_m.group(2)); _vs = _m.group(3) + (("–" + _m.group(4)) if _m.group(4) else "")
            _e = _kt.setdefault(_bk, {}).setdefault(_ch, {}).setdefault(_s, [0, [], _anchor3(_t)])
            _e[0] += 1
            if _vs not in _e[1] and len(_e[1]) < 60: _e[1].append(_vs)
_o3.makedirs("kt", exist_ok=True)
_stems3 = sorted(_B3, key=lambda s: (_B3[s]["author"], _B3[s]["title"]))
_six3 = {s: i for i, s in enumerate(_stems3)}
for _bk, _chs in _kt.items():
    _o = {str(ch): sorted([[_six3[s], v[0], v[1], v[2]] for s, v in d.items()], key=lambda r: -r[1])[:40] for ch, d in _chs.items()}
    open(f"kt/{_bk}.json", "w", encoding="utf-8").write(_j3.dumps(_o, ensure_ascii=False, separators=(",", ":")))
_tbl3 = [[_s, _B3[_s]["title"], _B3[_s]["author"]] for _s in _stems3]
_cnts3 = {bk: sorted([[ch, sum(v[0] for v in d.values())] for ch, d in chs.items()]) for bk, chs in _kt.items()}
_bk_opts = "".join(f'<option value="{i+1}">{E(n)}{" (" + str(sum(c for _, c in _cnts3.get(i+1, []))) + ")" if i+1 in _cnts3 else ""}</option>' for i, n in enumerate(_VN66))
_b1 = _NC3 + f'''<h1>Tra cứu theo Kinh Thánh</h1>
<p>Chọn một sách và một chương Kinh Thánh để thấy những sách Cải Chánh trong thư viện đã trích dẫn hoặc giảng giải đoạn đó. Nhấn vào kết quả để mở đúng chỗ trong trình đọc.</p>
<div class="sel noprint"><select id="bk" aria-label="Sách Kinh Thánh">{_bk_opts}</select><select id="ch" aria-label="Chương"></select></div>
<p class="m" id="st"></p><ul class="rs" id="rs"></ul>
<p class="m">Chỉ tính các trích dẫn dạng “Sách chương:câu” trong {len(_stems3)} bản dịch tiếng Việt. Bản dịch do AI hỗ trợ, chưa được mục sư duyệt; hãy đối chiếu Kinh Thánh. Số trong ngoặc là số lần được trích dẫn.</p>
<script>(function(){{var T={_j3.dumps(_tbl3, ensure_ascii=False, separators=(",", ":"))},C={_j3.dumps(_cnts3, separators=(",", ":"))};
var bk=document.getElementById("bk"),ch=document.getElementById("ch"),rs=document.getElementById("rs"),st=document.getElementById("st"),cache={{}};
function fillCh(){{var n=bk.value,l=C[n]||[];ch.innerHTML=l.length?l.map(function(x){{return'<option value="'+x[0]+'">Chương '+x[0]+' ('+x[1]+')</option>'}}).join(""):'<option value="">Chưa có chương nào</option>';show()}}
function E(s){{return String(s).replace(/[&<>"]/g,function(c){{return{{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}}[c]}})}}
function show(){{var n=bk.value,c=ch.value;rs.innerHTML="";if(!c){{st.textContent="Chưa có sách nào trong thư viện trích dẫn sách này.";return}}st.textContent="Đang tải…";
(cache[n]?Promise.resolve(cache[n]):fetch("/kt/"+n+".json").then(function(r){{return r.json()}}).then(function(j){{return cache[n]=j}})).then(function(j){{var l=j[c]||[];st.textContent=l.length+" sách trích dẫn "+bk.options[bk.selectedIndex].text.replace(/ \\(\\d+\\)$/,"")+" "+c+".";
rs.innerHTML=l.map(function(r){{var t=T[r[0]];return'<li><a href="/reader.html?id=vn/'+t[0]+'&at='+encodeURIComponent(r[3])+'">'+E(t[1])+'</a> · '+E(t[2])+' <span class="m">('+r[1]+' lần: '+r[2].map(function(v){{return c+':'+v}}).join(", ")+')</span></li>'}}).join("")}}).catch(function(){{st.textContent="Không tải được dữ liệu. Hãy thử lại."}})}}
bk.onchange=fillCh;ch.onchange=show;var h=location.hash.match(/#(\\d+)-(\\d+)/);if(h){{bk.value=h[1];fillCh();ch.value=h[2];show()}}else{{bk.value=45;fillCh()}}}})()</script>'''
open("tra-kinh-thanh.html", "w", encoding="utf-8").write(page("Tra cứu theo Kinh Thánh: ai giảng giải đoạn này? | Reformed Vietnam", "Chọn sách và chương Kinh Thánh để thấy những sách Cải Chánh tiếng Việt đã trích dẫn và giảng giải đoạn đó.", "tra-kinh-thanh.html", _b1)); urls.append("tra-kinh-thanh.html")

# ---------- 2. Giao ly hang ngay ----------
def _qa3(path, rx, kind):
    t = open(path, encoding="utf-8").read(); out = []
    if kind == "hd":
        for m in _r3.finditer(r"\*\*Hỏi (\d+)\.\*\*\s*\n(.+?)\n\s*\n\*\*Đáp\.\*\*\s*\n(.+?)(?=\n\s*\n)", t, _r3.S):
            out.append([int(m.group(1)), m.group(2).strip(), _r3.sub(r"\s*\([a-z]{1,2}\)", "", m.group(3)).strip()])
    else:
        for m in _r3.finditer(r"\*\*Câu (\d+)\. (.+?)\*\*\s*\n\s*\n(?:Đáp\.\s*)?(.+?)(?=\n\s*\n)", t, _r3.S):
            out.append([int(m.group(1)), m.group(2).strip(), _r3.sub(r"\[[a-z]{1,2}\]", "", m.group(3)).strip()])
    return out
_hd3 = _qa3("translations/heidelberg.txt", None, "hd"); _wsc3 = _qa3("translations/westminster-shorter.txt", None, "wsc")
_b2 = _NC3 + f'''<h1>Giáo lý mỗi ngày</h1><p class="m" id="dt"></p>
<p>Mỗi ngày một câu hỏi từ hai bản giáo lý vấn đáp của truyền thống Cải Chánh. Đọc chậm, đối chiếu Kinh Thánh, rồi nói chuyện với người thân hoặc nhóm nhỏ. Dùng nút để xem câu khác.</p>
<section class="nc"><h2>Giáo lý Heidelberg <span class="stt" id="hn"></span></h2><p><b id="hq"></b></p><p id="ha"></p><p><button class="btn s" id="hp" type="button">← Trước</button> <button class="btn s" id="hx" type="button">Sau →</button> <a class="btn s" id="hl" href="#">Mở trong trình đọc</a></p></section>
<section class="nc"><h2>Giáo lý Vắn tắt Westminster <span class="stt" id="wn"></span></h2><p><b id="wq"></b></p><p id="wa"></p><p><button class="btn s" id="wp" type="button">← Trước</button> <button class="btn s" id="wx" type="button">Sau →</button> <a class="btn s" id="wl" href="#">Mở trong trình đọc</a></p></section>
<section class="nc"><h2>Ba câu hỏi để suy nghĩ</h2><ol><li>Câu trả lời này nói gì về Đức Chúa Trời?</li><li>Nó nói gì về tôi, và về điều tôi cần?</li><li>Hôm nay tôi sẽ tin hoặc vâng giữ điều gì cụ thể?</li></ol></section>
<p class="m">Các bản dịch giáo lý này do AI hỗ trợ và chưa được mục sư duyệt. Các câu Kinh Thánh chứng minh có trong bản đầy đủ ở trình đọc. <a href="/hom-nay.html">Xem thêm trang Hôm nay</a>.</p>
<script>(function(){{var H={_j3.dumps(_hd3, ensure_ascii=False, separators=(",", ":"))},W={_j3.dumps(_wsc3, ensure_ascii=False, separators=(",", ":"))};
var d=new Date(),doy=Math.floor((d-new Date(d.getFullYear(),0,0))/864e5);document.getElementById("dt").textContent="Ngày "+d.getDate()+"/"+(d.getMonth()+1)+"/"+d.getFullYear();
function E(s){{return String(s).replace(/[&<>]/g,function(c){{return{{"&":"&amp;","<":"&lt;",">":"&gt;"}}[c]}})}}
function wire(L,p,id,rd,lab,init){{var i=init;function r(){{var x=L[i];document.getElementById(p+"n").textContent=lab+x[0]+"/"+L.length;document.getElementById(p+"q").textContent=x[1];document.getElementById(p+"a").innerHTML=E(x[2]);
document.getElementById(p+"l").href="/reader.html?id=vn/"+rd+"&at="+encodeURIComponent(({{h:"**Hỏi "+x[0]+".**",w:"**Câu "+x[0]+"."}})[p=="h"?"h":"w"])}}
document.getElementById(p+"p").onclick=function(){{i=(i-1+L.length)%L.length;r()}};document.getElementById(p+"x").onclick=function(){{i=(i+1)%L.length;r()}};r()}}
wire(H,"h","hd","heidelberg","Hỏi ",(doy-1)%H.length);wire(W,"w","wsc","westminster-shorter","Câu ",(doy-1)%W.length)}})()</script>'''
open("giao-ly-hang-ngay.html", "w", encoding="utf-8").write(page("Giáo lý mỗi ngày: Heidelberg và Westminster | Reformed Vietnam", "Mỗi ngày một câu hỏi giáo lý Heidelberg và Westminster bằng tiếng Việt, kèm ba câu hỏi suy nghĩ.", "giao-ly-hang-ngay.html", _b2)); urls.append("giao-ly-hang-ngay.html")

# ---------- 3. Nhom nho (per book) ----------
_Q3 = ["Đoạn này nói điều gì về Đức Chúa Trời, hoặc về Đấng Christ?", "Có điều nào khó hiểu hoặc làm bạn băn khoăn? Kinh Thánh nói gì về điều đó?", "Điều gì trong phần đọc này bạn cần tin hoặc vâng giữ trong tuần tới, và ai có thể nhắc bạn?"]
_o3.makedirs("nhom-nho", exist_ok=True)
_isHead3 = lambda t: len(t) <= 90 and (t.startswith("#") or (t.isupper() and len(t) > 4) or bool(_r3.match(r"(chương|phần|bài|ngày|hỏi|mục|lời tựa|kết luận|sermon|chapter)\b", t, _r3.I)))
_gl = []
for _s in _stems3:
    _d = _B3[_s]; _bl = _d["blocks"]; _tot = _d["chars"]
    if _tot < 6000: continue
    _n = max(3, min(12, _m3.ceil(_tot / 14000)))
    _cut = [0]; _acc = 0; _target = _tot / _n; _k = 1
    for _i, (_t, _off) in enumerate(_bl):
        _acc += len(_t)
        if _acc >= _target * _k and _k < _n and _i + 1 < len(_bl):
            _cut.append(_i + 1); _k += 1
    _cut.append(len(_bl))
    _rows = ""
    for _j in range(len(_cut) - 1):
        _seg = _bl[_cut[_j]:_cut[_j + 1]]
        if not _seg: continue
        _hs = [x[0].lstrip("# ").strip("* ") for x in _seg if _isHead3(x[0])]
        _lab = (_hs[0] if _hs else _seg[0][0][:70] + "…") + ((" … " + _hs[-1]) if len(_hs) > 1 else "")
        _cc = _c3.Counter()
        for _t, _ in _seg:
            for _m in _bkre3.finditer(_t): _cc[f"{_VN66[_bkv3[_m.group(1).lower()] - 1]} {_m.group(2)}"] += 1
        _scr = ", ".join(x for x, _ in _cc.most_common(3))
        _link = f'/reader.html?id=vn/{_s}&at={_up3.quote(_anchor3(_seg[0][0]))}'
        _rows += f'<section class="nc"><h2>Buổi {_j + 1}</h2><p><b>Đọc:</b> <a href="{E(_link)}">{E(_lab)}</a> <span class="stt">(khoảng {max(5, round(sum(len(x[0]) for x in _seg) / 900))} phút)</span></p>' + (f'<p><b>Kinh Thánh cùng đọc:</b> {E(_scr)}</p>' if _scr else "") + '<ol>' + "".join(f'<li class="q">{E(q)}</li>' for q in _Q3) + '</ol></section>'
    _bd = _NC3 + f'<h1>Nhóm nhỏ: {E(_d["title"])}</h1><p>{E(_d["author"])} · {_n} buổi, mỗi buổi khoảng 15–25 phút đọc. Người dẫn nhóm mở đầu bằng cầu nguyện, mọi người đọc phần của buổi đó trước, rồi thảo luận ba câu hỏi. <button class="btn s noprint" type="button" onclick="print()">In</button></p>' + _rows + '<p class="m">Các câu hỏi là khung chung, không thay thế sự hướng dẫn của mục sư. Bản dịch do AI hỗ trợ, chưa được mục sư duyệt. <a href="/nhom-nho.html">Các sách khác</a>.</p>'
    open(f"nhom-nho/{_s}.html", "w", encoding="utf-8").write(page(f"Nhóm nhỏ: {_d['title']} | Reformed Vietnam", f"Kế hoạch đọc và thảo luận {_n} buổi cho nhóm nhỏ: {_d['title']} ({_d['author']}).", f"nhom-nho/{_s}.html", _bd)); urls.append(f"nhom-nho/{_s}.html")
    _gl.append((_s, _d["title"], _d["author"], _n))
_li = "".join(f'<li><a href="/nhom-nho/{s}.html">{E(t)}</a> · {E(a)} <span class="stt">({n} buổi)</span></li>' for s, t, a, n in sorted(_gl, key=lambda x: (x[3], x[2], x[1])))
_b3 = _NC3 + f'<h1>Sách cho nhóm nhỏ</h1><p>Mỗi sách được chia thành các buổi học ngắn, có phần đọc, Kinh Thánh cùng đọc và ba câu hỏi thảo luận. Phù hợp cho nhóm 3–10 người ở nhà nhóm hoặc trực tuyến. Sách ngắn nằm trên cùng. Có thể in từng kế hoạch. Muốn bắt đầu nhanh? Xem <a href="/doc-chung.html">kế hoạch 4 tuần</a>.</p><ul class="rs">{_li}</ul><p class="m">Bản dịch do AI hỗ trợ, chưa được mục sư duyệt.</p>'
open("nhom-nho.html", "w", encoding="utf-8").write(page("Sách cho nhóm nhỏ: kế hoạch đọc và thảo luận | Reformed Vietnam", "Kế hoạch học nhóm nhỏ cho từng sách Cải Chánh tiếng Việt: phần đọc, Kinh Thánh cùng đọc và câu hỏi thảo luận.", "nhom-nho.html", _b3)); urls.append("nhom-nho.html")

# ---------- 7. Ke hoach doc ca nhan ----------
_opt = "".join(f'<option value="{s}">{E(_B3[s]["title"])} · {E(_B3[s]["author"])} ({round(_B3[s]["chars"] / 900)} phút)</option>' for s in sorted(_B3, key=lambda s: _B3[s]["chars"]))
_b7 = _NC3 + f'''<h1>Kế hoạch đọc cá nhân</h1><p>Chọn một sách và số ngày. Trang chia sách thành các phần đều nhau, mỗi phần có một liên kết mở đúng chỗ trong trình đọc. Tiến độ lưu trong điện thoại của bạn, không gửi đi đâu.</p>
<div class="sel noprint"><select id="bk" aria-label="Sách">{_opt}</select><select id="dy" aria-label="Số ngày"><option>7</option><option selected>14</option><option>30</option><option>60</option><option>90</option></select></div>
<p class="m" id="st"></p><ol id="pl"></ol><p class="m">Khoảng 15 phút đọc mỗi ngày là đủ cho phần lớn sách. Bản dịch do AI hỗ trợ, chưa được mục sư duyệt.</p>
<script>(function(){{var $=function(i){{return document.getElementById(i)}};function E(s){{return String(s).replace(/[&<>"]/g,function(c){{return{{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}}[c]}})}}
function ls(k,v){{try{{if(v===undefined)return JSON.parse(localStorage.getItem(k)||"[]");localStorage.setItem(k,JSON.stringify(v))}}catch(e){{return[]}}}}
function blocks(t){{var o=[];t.split(/\\n[ \\t]*\\n/).forEach(function(r){{var s=r.split("\\n").map(function(x){{return x.trim()}}).filter(Boolean).join(" ").replace(/\\s{{2,}}/g," ");if(s.length>1)o.push(s)}});return o}}
function an(t){{var a=t.slice(0,46);if(t.length>46&&a.indexOf(" ")>0&&a.slice(-1)!==" ")a=a.slice(0,a.lastIndexOf(" "));return a.trim()}}
function go(){{var s=$("bk").value,n=+$("dy").value;$("st").textContent="Đang tạo kế hoạch…";$("pl").innerHTML="";
fetch("/txt/"+s+".txt").then(function(r){{return r.text()}}).then(function(t){{var B=blocks(t),tot=B.reduce(function(a,x){{return a+x.length}},0),pos=[],acc=0;B.forEach(function(x,i){{pos.push(acc);acc+=x.length}});
var done=ls("rv.kh."+s+"."+n),h="",bi=0;for(var d=0;d<n;d++){{var tg=tot*d/n;while(bi<B.length-1&&pos[bi+1]<=tg)bi++;
var mins=Math.max(1,Math.round(tot/n/900));h+='<li><label><input type="checkbox" data-d="'+d+'"'+(done.indexOf(d)>=0?" checked":"")+'> Ngày '+(d+1)+'</label> · <a href="/reader.html?id=vn/'+s+'&at='+encodeURIComponent(an(B[bi]))+'">Mở phần này</a> <span class="m">(~'+mins+' phút)</span></li>'}}
$("pl").innerHTML=h;$("st").textContent=n+" ngày, đã đọc "+done.length+"/"+n+".";
$("pl").onchange=function(e){{var d=+e.target.dataset.d,a=ls("rv.kh."+s+"."+n),i=a.indexOf(d);if(e.target.checked&&i<0)a.push(d);if(!e.target.checked&&i>=0)a.splice(i,1);ls("rv.kh."+s+"."+n,a);$("st").textContent=n+" ngày, đã đọc "+a.length+"/"+n+"."}}}}).catch(function(){{$("st").textContent="Không tải được sách. Hãy thử lại."}})}}
$("bk").onchange=go;$("dy").onchange=go;var q=location.hash.slice(1);if(q&&$("bk").querySelector('[value="'+q+'"]'))$("bk").value=q;go()}})()</script>'''
open("ke-hoach-doc.html", "w", encoding="utf-8").write(page("Kế hoạch đọc cá nhân: chia sách theo ngày | Reformed Vietnam", "Chọn một sách Cải Chánh tiếng Việt và số ngày; nhận kế hoạch đọc từng ngày, lưu tiến độ trong điện thoại.", "ke-hoach-doc.html", _b7)); urls.append("ke-hoach-doc.html")

exec(open("tools/nang_cap3b.py", encoding="utf-8").read()) if _o3.path.exists("tools/nang_cap3b.py") else None
