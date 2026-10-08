#!/usr/bin/env python3
"""Add the 100 pipeline Vietnamese translations to mg.json["vn"] so they appear
in the app's 'Tiếng Việt' source filter and in tieng-viet.html.

Each entry gets id "vnb-<slug>" (no collision with English book ids) and
"vnb": 1 marker. Idempotent: skips ids already present.
"""
import json, os

# 100 pipeline book ids, in TRANSLATION-100.md order
PIPELINE = [
"spurgeon/grace","owen/mort","bonar/peace","baxter/unconverted","bunyan/grace",
"owen/temptation","watson/contentment","knox/prayer","hooker/just","charnock/nec_regen",
"bonar/rentveil","boston/crook","rutherford/letters","doddridge/evidences","owen/faith",
"owen/sin_grace","charnock/cleansing","flavel/christlovely","edwards/treatiseongrace",
"charnock/instr_regen","sibbes/bruisedreed","brooks/remedies","burroughs/contentment",
"bunyan/fearofgod","alleine_j/alarm","bayly/piety","westminster/shorter","creeds/heidelberg",
"alleine_r/rebuke","alleine_r/heartwork","watson/cordial","flavel/saintindeed","baxter/causes",
"owen/eshcol","owen/conscience","baxter/practical","berkhof/summary","baxter/pastor",
"spurgeon/till_he_come","spurgeon/checkbook","owen/glory","owen/indwellingsin",
"owen/spirituallyminded","doddridge/rise","doddridge/regen","charnock/nat_regen",
"charnock/efficient_regeneration","charnock/reconcil","owen/worship","owen/churchlove",
"owen/schism","owen/apostasy","owen/psalm130","owen/discourses","owen/trinity",
"owen/justice","owen/display","bunyan/holy_war","bunyan/badman","ryle/matthew",
"ryle/upperroom","alexander_a/evidences","alexander_a/canon","schaff/person",
"hodge/darwinism","bavinck/revelation","kuyper/ascent","kuyper/greater","edwards/will",
"watson/beatitudes","watson/tencommandments","rutherford/triumph","baxter/saintsrest",
"calvin/relics","owen/pastorspeople","kuyper/islam","owen/liturgies","alexander_a/moralscience",
"brooks/smoothstones","boston/beauties","anthology/daily-meditations",
"anthology/gospel-promises","anthology/lordsprayer-meditations","boettner/predestination",
"ryle/holiness","edwards/affections","watson/bodyofdivinity","watson/lordsprayer",
"edwards/sermons","kuyper/neartogod","berkhof/ntintro","owen/justification",
"flavel/methodofgrace","flavel/fountainoflife","kuyper/holyspirit","flavel/soul",
"boyce/abstract","spurgeon/morningevening","edwards/trinity","knox/history",
]
assert len(PIPELINE) == 100, len(PIPELINE)

TY_KEYWORDS = [
    ("sermons", ["bài giảng"]),
    ("devotional", ["tĩnh nguyện", "hằng ngày", "buổi sáng", "buổi chiều", "suy ngẫm",
                     "kinh lạy cha", "lạy cha", "cầu nguyện"]),
    ("catechism", ["vấn đáp", "tín điều", "heidelberg", "westminster"]),
    ("history", ["lịch sử", "tuyển thư", "thử thách và thắng lợi"]),
    ("systematic", ["thần học hệ thống", "thân thể thần học", "tóm tắt"]),
    ("classic", ["cuộc chiến", "badman"]),
    ("commentary", ["chú giải", "giải nghĩa"]),
]

def guess_ty(title):
    t = title.lower()
    for ty, kws in TY_KEYWORDS:
        if any(k in t for k in kws):
            return ty
    return "doctrine"

idx = json.load(open("translations/index.json", encoding="utf-8"))
mg = json.load(open("mg.json", encoding="utf-8"))
have = {r["id"] for r in mg["vn"]}
added = 0
for e in idx:
    bid = e["id"]
    if bid not in PIPELINE or e.get("hold"):
        continue
    slug = os.path.splitext(e["file"])[0]
    if not os.path.exists(f"translations/{e['file']}"):
        print(f"SKIP (no file): {bid}")
        continue
    vid = "vnb-" + slug
    if vid in have:
        continue
    title = e.get("title", bid)
    author = e.get("author", "")
    mg["vn"].append({
        "id": vid,
        "ty": guess_ty(title),
        "a": author,
        "col": "#0d1b2a",
        "url": f"/ban-dich/{slug}.html",
        "en": {"t": f"{title} (Vietnamese)",
               "n": "Vietnamese translation by Reformed Vietnam (AI-assisted, not yet reviewed). Public-domain original."},
        "vi": {"t": title,
               "n": "Bản dịch tiếng Việt do Reformed Vietnam thực hiện (AI hỗ trợ, chưa duyệt). Nguyên tác thuộc phạm vi công cộng."},
        "vnb": 1,
    })
    added += 1

json.dump(mg, open("mg.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"added {added}; mg.json vn total: {len(mg['vn'])}")
