"""Resolve helper-AI related_books strings to live library reader pages.

Built 2026-11-06 by the integrator: every mapping below was verified against the
library index (translations/index-lite.json) and the live sitemap — the URL is a
real /ban-dich/<slug>.html page. Helper title variants of the same work (the
helpers rendered some titles differently, incl. English originals) map to the
same library page. Works that could not be resolved confidently map to None and
are omitted from pages (never linked blindly).

Key: the exact "Title — Author" string from the helper files.
Value: (library display label, url) or None.
"""

BOOK_LINKS = {
    "Chủ Quyền Của Đức Chúa Trời — A. W. Pink":
        ("Chủ Quyền Của Đức Chúa Trời — A. W. Pink", "/ban-dich/mg1-049-sovereignty-of-god-pink.html"),
    "Cuộc Hành Trình Của Người Hành Hương — John Bunyan":
        ("Hành Trình Của Người Lữ Hành — John Bunyan", "/ban-dich/001-pilgrims-progress-bunyan.html"),
    "Hành Trình Của Người Lữ Khách — John Bunyan":
        ("Hành Trình Của Người Lữ Hành — John Bunyan", "/ban-dich/001-pilgrims-progress-bunyan.html"),
    "The Pilgrim's Progress — John Bunyan":
        ("Hành Trình Của Người Lữ Hành — John Bunyan", "/ban-dich/001-pilgrims-progress-bunyan.html"),
    "Giáo Lý Cơ Đốc Giáo — John Calvin":
        ("Giáo Lý Cơ Đốc Giáo — John Calvin", "/ban-dich/mg1-121-institutes-of-the-christian-religion-reformed-theo-calvin.html"),
    "Giáo Lý Cơ Đốc — John Calvin":
        ("Giáo Lý Cơ Đốc Giáo — John Calvin", "/ban-dich/mg1-121-institutes-of-the-christian-religion-reformed-theo-calvin.html"),
    "The Institutes of the Christian Religion — John Calvin":
        ("Giáo Lý Cơ Đốc Giáo — John Calvin", "/ban-dich/mg1-121-institutes-of-the-christian-religion-reformed-theo-calvin.html"),
    "Bình Luận Rô-ma — John Calvin":
        ("Chú Giải Thư Rô-ma — John Calvin", "/ban-dich/013-commentary-romans-calvin.html"),
    "Phương Pháp Cầu Nguyện — Matthew Henry":
        ("Một Phương Pháp Cầu Nguyện — Matthew Henry", "/ban-dich/334-method-for-prayer-with-scripture-expressions-henry.html"),
    "Sự Chết Của Sự Chết Trong Sự Chết Của Đấng Christ — John Owen":
        ("Sự Chết Của Sự Chết Trong Sự Chết Của Đấng Christ — John Owen", "/ban-dich/arch-owen-death-of-death.html"),
    "Sự Xưng Công Chính Bởi Đức Tin — John Owen":
        ("Giáo Lý Xưng Công Chính Bởi Đức Tin — John Owen", "/ban-dich/owen-justification.html"),
    "The Doctrine of Justification by Faith — John Owen":
        ("Giáo Lý Xưng Công Chính Bởi Đức Tin — John Owen", "/ban-dich/owen-justification.html"),
    "Sự Nên Thánh — J. C. Ryle":
        ("Sự Nên Thánh — J. C. Ryle", "/ban-dich/ryle-holiness.html"),
    "Tất Cả Ân Điển — Charles Spurgeon":
        ("Tất Cả Bởi Ân Điển — Charles Spurgeon", "/ban-dich/spurgeon-grace.html"),
    "Faith's Checkbook — C. H. Spurgeon":
        ("Sổ Séc Của Đức Tin — C. H. Spurgeon", "/ban-dich/spurgeon-checkbook.html"),
    "Kho Báu Đức Tin — Charles H. Spurgeon":
        ("Sổ Séc Của Đức Tin — C. H. Spurgeon", "/ban-dich/spurgeon-checkbook.html"),
    "Tội Nhân Trong Tay Một Đức Chúa Trời Thạnh Nộ — Jonathan Edwards":
        ("Kẻ Có Tội Trong Tay Đức Chúa Trời Thạnh Nộ — Jonathan Edwards", "/ban-dich/308-sinners-in-the-hands-of-an-angry-god-edwards.html"),
    "Tội Nhân Trong Tay Đức Chúa Trời Thịnh Nộ — Jonathan Edwards":
        ("Kẻ Có Tội Trong Tay Đức Chúa Trời Thạnh Nộ — Jonathan Edwards", "/ban-dich/308-sinners-in-the-hands-of-an-angry-god-edwards.html"),
    "Hệ Thống Thần Học — Charles Hodge":
        ("Thần Học Hệ Thống — Charles Hodge", "/ban-dich/869-systematic-theology-questions-hodge.html"),
    # Unresolved against the library index — omitted from pages on purpose:
    "Chú Giải Kinh Thánh — Matthew Henry": None,          # no single-volume match
    "Tóm Lược Thần Học — Charles Hodge": None,            # no confident match
    "The Westminster Confession of Faith — Westminster Assembly": None,  # not a library book
}

def resolve(book_strings):
    """Return a list of (label, url) for the strings that resolve, deduped by url."""
    out, seen = [], set()
    for s in book_strings:
        v = BOOK_LINKS.get(s)
        if v and v[1] not in seen:
            seen.add(v[1]); out.append(v)
    return out
