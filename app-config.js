window.RV_CONFIG = {
  SRCS: ["ccel", "vn", "mg", "ia", "pg", "lv", "dg", "lig", "other"],
  MEDIA: ["read", "pdf", "epub", "audio"],
  TYPES: ["systematic", "commentary", "sermons", "devotional", "doctrine", "catechism", "history", "collected", "bible", "classic"],
  ERAS: ["anc", "ref", "pur", "aw", "mod", "c20"],
  LEVELS: [
    {k:"new",t:["Mới tin Chúa","New believer"],d:["Đọc nhẹ, dễ vào","Gentle and clear"],ids:["bunyan/pilgrim","bonar/peace","ryle/holiness","flavel/lovely","spurgeon/grace"]},
    {k:"grow",t:["Đang lớn lên","Growing"],d:["Đời sống thuộc linh","Deeper devotion"],ids:["owen/mort","watson/contentment","baxter/saints_rest","boston/crook","edwards/affections"]},
    {k:"deep",t:["Học sâu","Studying"],d:["Thần học hệ thống","Systematic theology"],ids:["calvin/institutes","edwards/will","hodge/theology1","berkhof/systematictheology","kuyper/holy_spirit"]}
  ],
  SHELVES: [
    {k:"vn",sr:"vn",t:["Tiếng Việt","Vietnamese readings"],p:function(b){return b.au==="vn";},o:function(a,b){return(a.id.indexOf("vn-")===0?1:0)-(b.id.indexOf("vn-")===0?1:0)}},
    {k:"aud",md:"audio",t:["Sách nói","Audiobooks"],p:function(b){return hasM(b,"audio");},o:function(a,b){return(a.au==="lv"?1:0)-(b.au==="lv"?1:0)}}
  ],
  TILES: [
    ["tieng-viet.html","Đọc sách tiếng Việt","Read in Vietnamese","Đọc ngay, không cần dịch","Ready to read, no translation needed"],
    ["chu-de/","Tìm hiểu một chủ đề","Explore a topic","Ân điển, Hội Thánh, cầu nguyện…","Grace, church, prayer…"],
    ["sach-noi.html","Nghe sách nói","Listen","Nghe khi đi đường","Listen on the go"],
    ["hom-nay.html","Bài đọc hôm nay","Today's reading","Mỗi ngày một đoạn ngắn","One short passage a day"]
  ]
};
