# Executed from build-pages.py. Builds trich-dan.html: daily quote with downloadable/shareable image card.
import json as _j
_Q = [
 ("Lòng người luôn là một xưởng sản xuất thần tượng không ngừng nghỉ.", "The human heart is a perpetual factory of idols.", "John Calvin", "Cơ Đốc Giáo Cương Yếu 1.11.8"),
 ("Sự khôn ngoan thật của chúng ta gồm hầu như chỉ hai phần: biết Đức Chúa Trời và biết chính mình.", "Our wisdom consists almost entirely of two parts: the knowledge of God and of ourselves.", "John Calvin", "Cơ Đốc Giáo Cương Yếu 1.1.1"),
 ("Hãy giết tội lỗi, nếu không nó sẽ giết bạn.", "Be killing sin or it will be killing you.", "John Owen", "Về sự làm chết tội lỗi"),
 ("Tôi đã học hôn lên con sóng đã quăng tôi vào Vầng Đá Muôn Đời.", "I have learned to kiss the wave that throws me against the Rock of Ages.", "C. H. Spurgeon", ""),
 ("Hãy thăm nhiều sách hay, nhưng hãy sống trong Kinh Thánh.", "Visit many good books, but live in the Bible.", "C. H. Spurgeon", ""),
 ("Nhờ kiên trì, con ốc sên đã vào được tàu.", "By perseverance the snail reached the ark.", "C. H. Spurgeon", ""),
 ("Nơi Đấng Christ có nhiều thương xót hơn tội lỗi trong chúng ta.", "There is more mercy in Christ than sin in us.", "Richard Sibbes", ""),
 ("Quyết định sống hết sức mình khi tôi còn sống.", "Resolved: to live with all my might while I do live.", "Jonathan Edwards", "Các quyết tâm"),
 ("Cầu nguyện sẽ khiến con người thôi phạm tội, hoặc tội lỗi sẽ khiến con người thôi cầu nguyện.", "Prayer will make a man cease from sin, or sin will entice a man to cease from prayer.", "John Bunyan", ""),
 ("Chúa đã dựng nên chúng con cho chính Ngài, và lòng chúng con còn bất an cho đến khi yên nghỉ trong Ngài.", "You have made us for yourself, and our heart is restless until it rests in you.", "Augustine", "Tự Thú"),
 ("Mục đích chính của con người là làm vinh hiển Đức Chúa Trời và vui hưởng Ngài đời đời.", "Man's chief end is to glorify God, and to enjoy him for ever.", "Giáo lý Vắn tắt Westminster", "Câu hỏi 1"),
 ("Tôi không thuộc về chính mình, nhưng cả thân thể lẫn linh hồn, lúc sống cũng như lúc chết, đều thuộc về Cứu Chúa thành tín của tôi là Chúa Jesus Christ.", "That I am not my own, but belong, body and soul, in life and in death, to my faithful Savior Jesus Christ.", "Giáo lý Heidelberg", "Câu hỏi 1"),
]
_data = _j.dumps([{"v": v, "e": e, "a": a, "s": s} for v, e, a, s in _Q], ensure_ascii=False)
_css = '<style>.qc{margin:18px 0;padding:22px;border:1px solid #8884;border-radius:14px;background:#9a34120a}.qv{font:600 1.35rem/1.5 Georgia,serif;margin:0 0 10px}.qe{opacity:.7;font-style:italic;margin:0 0 10px}.qa{font-weight:700}.qb{display:flex;gap:10px;flex-wrap:wrap;margin:12px 0}.qb button{padding:9px 16px;border:1px solid #8886;border-radius:999px;background:none;color:inherit;font:inherit;cursor:pointer}.qb button.p{background:#9a3412;color:#fff;border-color:#9a3412}canvas{display:none}</style>'
_body = f'''{_css}<h1>Trích dẫn hôm nay</h1>
<p>Một câu ngắn từ các tác giả Cải Chánh, kèm ảnh để tải về và chia sẻ trên Facebook, Zalo hay nhóm của bạn.</p>
<div class="qc"><p class="qv" id="qv"></p><p class="qe" id="qe"></p><p class="qa" id="qa"></p></div>
<div class="qb"><button class="p" id="dl" type="button">⬇ Tải ảnh</button><button id="sh" type="button">↗ Chia sẻ</button><button id="cp" type="button">Sao chép</button><button id="nx" type="button">Câu khác</button></div>
<p><small>Bản dịch tiếng Việt là dịch của Reformed Vietnam, chưa có mục sư duyệt. Đối chiếu bản gốc khi trích dẫn công khai.</small></p>
<canvas id="cv" width="1080" height="1080"></canvas>
<script>(function(){{var Q={_data},i=Math.floor(Date.now()/864e5)%Q.length,$=function(x){{return document.getElementById(x)}};
function show(){{var q=Q[i];$("qv").textContent="“"+q.v+"”";$("qe").textContent=q.e;$("qa").textContent="— "+q.a+(q.s?", "+q.s:"")}}
function wrap(c,t,x,y,w,lh){{var ws=t.split(" "),l="",ys=y;ws.forEach(function(s){{var n=l?l+" "+s:s;if(c.measureText(n).width>w&&l){{c.fillText(l,x,ys);ys+=lh;l=s}}else l=n}});c.fillText(l,x,ys);return ys+lh}}
function draw(){{var q=Q[i],cv=$("cv"),c=cv.getContext("2d");c.fillStyle="#f3ecd9";c.fillRect(0,0,1080,1080);c.fillStyle="#9a3412";c.fillRect(90,110,120,8);
c.fillStyle="#2a2118";c.textBaseline="alphabetic";var fs=q.v.length>110?52:60;c.font="600 "+fs+"px Georgia,'Times New Roman',serif";var y=wrap(c,"“"+q.v+"”",90,230,900,fs*1.35);
c.font="italic 34px Georgia,serif";c.fillStyle="#6b5d4a";y=wrap(c,q.e,90,y+30,900,46);
c.font="700 40px Georgia,serif";c.fillStyle="#9a3412";c.fillText("— "+q.a,90,Math.min(y+50,930));if(q.s){{c.font="30px Georgia,serif";c.fillStyle="#6b5d4a";c.fillText(q.s,90,Math.min(y+95,975))}}
c.font="600 30px system-ui,sans-serif";c.fillStyle="#2a2118";c.fillText("Reformed Vietnam",90,1030);c.font="26px system-ui,sans-serif";c.fillStyle="#6b5d4a";c.textAlign="right";c.fillText("reformed-vietnam.vercel.app",990,1030);c.textAlign="left"}}
function blob(cb){{draw();$("cv").toBlob(cb,"image/png")}}
$("dl").onclick=function(){{blob(function(b){{var a=document.createElement("a");a.href=URL.createObjectURL(b);a.download="reformed-vietnam-trich-dan.png";a.click()}})}};
$("sh").onclick=function(){{var q=Q[i],t="“"+q.v+"” — "+q.a+"\\nreformed-vietnam.vercel.app";blob(function(b){{var f=new File([b],"trich-dan.png",{{type:"image/png"}});if(navigator.canShare&&navigator.canShare({{files:[f]}}))navigator.share({{files:[f],text:t}}).catch(function(){{}});else if(navigator.share)navigator.share({{text:t,url:location.href}}).catch(function(){{}});else{{navigator.clipboard&&navigator.clipboard.writeText(t);$("sh").textContent="Đã sao chép"}}}})}};
$("cp").onclick=function(){{var q=Q[i];navigator.clipboard&&navigator.clipboard.writeText("“"+q.v+"” — "+q.a+(q.s?", "+q.s:"")+"\\nreformed-vietnam.vercel.app");$("cp").textContent="Đã sao chép";setTimeout(function(){{$("cp").textContent="Sao chép"}},1500)}};
$("nx").onclick=function(){{i=(i+1)%Q.length;show()}};show()}})()</script>'''
open("trich-dan.html", "w", encoding="utf-8").write(page("Trích dẫn Cải Chánh hôm nay – ảnh để chia sẻ | Reformed Vietnam", "Một câu ngắn từ Calvin, Spurgeon, Owen, Bunyan, Edwards và các giáo lý Cải Chánh, kèm ảnh để tải về và chia sẻ.", "trich-dan.html", _body))
urls.append("trich-dan.html")
