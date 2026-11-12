#!/usr/bin/env python3
"""Build podcast.xml (RSS 2.0 + iTunes) for the "Sách Nói Cải Chánh" podcast.

Source of truth for book order/titles/authors: tools/sach-noi-entries.json
(only entries whose "listen" URL is set are included). Episode files and
sizes come from the Archive.org metadata API for each item. One episode per
MP3 file on the item (single-file books = exactly one episode).

Run: python3 scripts/build_podcast.py  -> writes ./podcast.xml at repo root.
Re-run after each new book is wired on /sach-noi.html.
"""
import json
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://reformedvietnam.com"
CHANNEL_TITLE = "Sách Nói Cải Chánh"
AI_LABEL = "Giọng đọc AI, bản dịch AI, chưa duyệt."

# Per-book episode descriptions (Spark, Round 22 S4 pack, verified 2026-11-09).
DESCRIPTIONS = {
    "reformed-vietnam-audiobook-plumer-letter-death-child": "Một bức thư an ủi dịu dàng của William S. Plumer gửi người bạn vừa mất con thơ: nỗi đau được đặt trong vòng tay của Đấng Christ, Đấng đã khóc, và trong hy vọng chắc chắn của giao ước ân điển.",
    "reformed-vietnam-audiobook-whitefield-barren-fig-tree": "George Whitefield giảng về cây vả không trái trong Ma-thi-ơ 21 và Mác 11, trong ngày kiêng ăn và hạ mình tại Scotland. Hãy nghe lời cảnh báo ấy và đem lại trái xứng với sự ăn năn.",
    "reformed-vietnam-audiobook-rutherford-cry-from-dead": "Bài giảng Tiệc Thánh của Samuel Rutherford mời bạn đến gần Đấng Christ và ăn uống tại bàn của Cha. Hãy lắng nghe tiếng kêu dịu dàng ấy và chạy về thiên đàng cùng Ngài.",
    "reformed-vietnam-audiobook-baxter-chi-dan-nguoi-benh": "Richard Baxter viết những lời chỉ dẫn ngắn này cho người bệnh thiếu vắng mục sư bên cạnh: bảy lời khuyên về sự chết, sự phán xét và nhu cầu ăn năn ngay khi còn có thể.",
    "reformed-vietnam-audiobook-hervey-thu-canh-tinh-altamont": "Bức thư cảnh tỉnh của mục sư James Hervey gởi ông Richard N— năm 1763: một lời cảnh báo nghiêm khắc về sự chết, sự phán xét và nhu cầu ăn năn — cùng câu chuyện về cái chết kinh khiếp của Altamont.",
    "reformed-vietnam-audiobook-flavel-christlovely": "John Flavel bày tỏ Đấng Christ đáng yêu trọn vẹn trong thân vị, chức vụ và các mối quan hệ của Ngài. Hãy lắng nghe và yêu mến Đấng Cứu Chuộc ấy càng hơn.",
    "reformed-vietnam-audiobook-bonar-followlamb": "Horatius Bonar viết những lời khuyên ấm áp dành cho người mới tin Chúa, để bước đi theo Chiên Con mỗi ngày. Hãy nghe trọn cuốn sách và lớn lên trong đức tin nơi Ngài.",
    "reformed-vietnam-audiobook-owen-mortification": "John Owen viết luận văn kinh điển về Rô-ma 8:13 — sự cần thiết, bản chất và phương cách giết chết tội lỗi trong tín hữu, qua 14 chương.",
    "reformed-vietnam-audiobook-sibbes-bruised-reed": "Richard Sibbes giảng về Ê-sai 42:3 — Đấng Christ không bẻ gãy cây sậy đã dập, không dập tắt bấc đèn còn khói: an ủi cho những người đức tin yếu đuối, qua 28 chương.",
    "reformed-vietnam-audiobook-spurgeon-morning-evening": "C. H. Spurgeon suy ngẫm Lời Chúa mỗi buổi sáng và buổi chiều — 366 ngày, 732 bài, theo Kinh Thánh 1934. Sách nói dài nhất của thư viện.",
    "reformed-vietnam-audiobook-watson-beatitudes": "Các Phước Lành — Thomas Watson. Loạt bài giảng về Ma-thi-ơ 5, tám mối phước của Bài Giảng Trên Núi. Sách nói dài 16 giờ 20 phút.",
    "reformed-vietnam-audiobook-brooks-precious-remedies": "Thomas Brooks vạch trần các mưu kế của Sa-tan — lôi kéo linh hồn phạm tội, giữ linh hồn khỏi các bổn phận thánh, giam hãm trong buồn bã và nghi ngờ — và đưa ra phương thuốc từ Lời Chúa, qua 4 phần và phụ lục.",
    "reformed-vietnam-audiobook-ryle-holiness": "J. C. Ryle giảng về sự nên thánh theo Kinh Thánh — tội lỗi, sự nên thánh, sự thánh khiết thực tiễn, cuộc chiến đấu, cái giá phải trả, sự tăng trưởng, sự chắc chắn, Môi-se, Lót, và Đấng Christ là tất cả.",
    "reformed-vietnam-audiobook-bunyan-grace": "John Bunyan kể hành trình của chính mình: từ đời sống phóng đãng, chửi rủa và phạm thượng đến sự bình an trong Đấng Christ qua Phúc Âm — tự truyện thuộc linh viết trong tù năm 1666.",
    "reformed-vietnam-audiobook-spurgeon-checkbook": "C. H. Spurgeon sắp xếp 366 lời hứa quý báu của Đức Chúa Trời cho mỗi ngày trong năm, kèm lời bình ngắn từ kinh nghiệm — một cuốn sổ séc đức tin để đem từng lời hứa đến trình dâng trước Chúa.",
}


def fetch_item(identifier):
    url = f"https://archive.org/metadata/{identifier}"
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def fmt_duration(seconds):
    seconds = int(round(float(seconds)))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def main():
    entries = json.loads((ROOT / "tools" / "sach-noi-entries.json").read_text(encoding="utf-8"))
    books = []
    for e in entries:
        listen = (e.get("listen") or "").strip()
        if not listen:
            continue
        identifier = listen.rstrip("/").split("/")[-1]
        books.append((identifier, e["title"], e["author"]))
    if not books:
        sys.exit("no wired books found")

    items_xml = []
    ep_no = 0
    total_eps = 0
    for identifier, title, author in books:
        data = fetch_item(identifier)
        meta = data.get("metadata", {})
        added = meta.get("addeddate", "")
        try:
            base = datetime.strptime(added, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
        except ValueError:
            base = datetime(2026, 1, 1, tzinfo=timezone.utc)
        mp3s = [
            f for f in data.get("files", [])
            if f.get("source") == "original" and f["name"].lower().endswith(".mp3")
        ]
        mp3s.sort(key=lambda f: f["name"])
        if not mp3s:
            sys.exit(f"{identifier}: no original MP3 files found")
        desc = DESCRIPTIONS.get(identifier, "")
        if AI_LABEL not in desc:
            desc = (desc + " " + AI_LABEL).strip()
        n = len(mp3s)
        for i, f in enumerate(mp3s):
            ep_no += 1
            total_eps += 1
            if n == 1:
                ep_title = f"{title} — {author}"
            else:
                ep_title = f"{title} — {author} · Phần {i + 1}/{n}"
            url = f"https://archive.org/download/{identifier}/{f['name']}"
            pub = format_datetime(base + timedelta(hours=i))
            dur = fmt_duration(f.get("length", 0))
            items_xml.append(
                "    <item>\n"
                f"      <title>{escape(ep_title)}</title>\n"
                f"      <description>{escape(desc)}</description>\n"
                f"      <enclosure url=\"{escape(url, {'\"': '&quot;'})}\" length=\"{f['size']}\" type=\"audio/mpeg\"/>\n"
                f"      <guid isPermaLink=\"true\">{escape(url)}</guid>\n"
                f"      <pubDate>{pub}</pubDate>\n"
                f"      <itunes:duration>{dur}</itunes:duration>\n"
                f"      <itunes:episode>{ep_no}</itunes:episode>\n"
                "      <itunes:episodeType>full</itunes:episodeType>\n"
                "    </item>"
            )
        print(f"{identifier}: {n} episode(s)")

    now = format_datetime(datetime.now(timezone.utc))
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{escape(CHANNEL_TITLE)}</title>
    <link>{SITE}/sach-noi.html</link>
    <atom:link href="{SITE}/podcast.xml" rel="self" type="application/rss+xml"/>
    <description>Sách nói Cơ Đốc Cải Chánh tiếng Việt — các tác phẩm kinh điển của Spurgeon, Owen, Sibbes, Ryle, Bunyan và nhiều tác giả khác, do Thư Viện Cải Chánh (reformedvietnam.com) thực hiện. {AI_LABEL}</description>
    <language>vi</language>
    <lastBuildDate>{now}</lastBuildDate>
    <itunes:author>Reformed Vietnam</itunes:author>
    <managingEditor>reformedvn@gmail.com (Reformed Vietnam)</managingEditor>
    <itunes:owner>
      <itunes:name>Reformed Vietnam</itunes:name>
      <itunes:email>reformedvn@gmail.com</itunes:email>
    </itunes:owner>
    <itunes:type>serial</itunes:type>
    <itunes:explicit>no</itunes:explicit>
    <itunes:image href="{SITE}/podcast-cover.jpg"/>
    <itunes:category text="Religion &amp; Spirituality">
      <itunes:category text="Christianity"/>
    </itunes:category>
{chr(10).join(items_xml)}
  </channel>
</rss>
"""
    out = ROOT / "podcast.xml"
    out.write_text(feed, encoding="utf-8")
    print(f"wrote {out} — {len(books)} books, {total_eps} episodes")


if __name__ == "__main__":
    main()
