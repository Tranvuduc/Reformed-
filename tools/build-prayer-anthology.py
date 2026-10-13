#!/usr/bin/env python3
"""Assemble 'Tuyen Tap Loi Cau Nguyen Thanh Giao' from existing translations.
Verbatim excerpts only; no retranslation."""
import re

T = '/home/hatch/workspace/reformed-site/translations/'

def read(fn):
    with open(T + fn, encoding='utf-8') as f:
        return f.read()

# ---------- Spurgeon pulpit prayers (I-XXVI; headers vary in case) ----------
spur = read('arch-spurgeon-prayers.txt')
# cut off the closing sermon first
spur = spur.split('Chìa Khóa Vàng của Sự Cầu Nguyện.')[0]
parts = re.split(r'(?m)^(LỜI CẦU NGUYỆN|Lời Cầu Nguyện|Bài Cầu Nguyện) ([IVXL]+)\.$', spur)
spur_prayers = {}
for i in range(1, len(parts) - 1, 3):
    num = parts[i + 1].strip()
    body = parts[i + 2]
    lines = body.strip().split('\n')
    j = 0
    while j < len(lines) and not lines[j].strip():
        j += 1
    prayer = '\n'.join(lines[j + 1:]).strip()  # drop subtitle line
    spur_prayers[num] = prayer
print('spurgeon prayers found:', len(spur_prayers))

# ---------- Whitefield occasion prayers ----------
wf = read('arch-whitefield-prayers-occasions.txt')
wparts = re.split(r'(?m)^LỜI CẦU NGUYỆN CHO ', wf)
wf_prayers = []
for p in wparts[1:]:
    nl = p.find('\n')
    wf_prayers.append(p[nl + 1:].strip())
assert len(wf_prayers) == 6
# 0=seeker(tái sinh) 1=mới tỉnh thức 2=bỏ rơi thuộc linh 3=bị ghét bỏ vì đạo
# 4=dạy dỗ trẻ em 5=đầy tớ

# ---------- Bayly ----------
bayly = read('bayly-piety.txt').split('\n')
def bayly_section(header):
    s = next(i for i, l in enumerate(bayly) if l.strip() == header)
    e = s + 1
    while e < len(bayly):
        ls = bayly[e].strip()
        if ls.startswith('## ') or ls == '---':
            break
        e += 1
    seg = bayly[s + 1:e]
    while seg and not seg[-1].strip():
        seg.pop()
    while seg and seg[-1].strip().startswith('Lạy Cha chúng tôi ở trên trời'):
        seg.pop()
        while seg and not seg[-1].strip():
            seg.pop()
    while seg and not seg[0].strip():
        seg.pop(0)
    return '\n'.join(seg).strip()

bayly_morning = bayly_section('## Một Lời Cầu Nguyện Buổi Sáng Ngắn Hơn.')
bayly_morning2 = bayly_section('## Lời Cầu Nguyện Ngắn Cho Buổi Sáng.')
bayly_evening = bayly_section('## Một Lời Cầu Nguyện Buổi Tối Khác, Ngắn Hơn.')

# ---------- Baxter liturgy (petition-peace): paragraphs ----------
bax = read('arch-baxter-petition-peace.txt').split('\n')
def para_at(lines, start):
    i = start - 1
    seg = []
    while i < len(lines) and lines[i].strip():
        seg.append(lines[i]); i += 1
    return '\n'.join(seg).strip()

bax_communion = para_at(bax, 390)
bax_consecrate = para_at(bax, 414)
bax_sick = para_at(bax, 592)

# ---------- Baxter family prayers (compassionate-warning appendix) ----------
baxc = read('arch-baxter-compassionate-warning.txt').split('\n')
baxc_general = para_at(baxc, 440)    # long general prayer
baxc_children = para_at(baxc, 451)   # children & servants
baxc_family = para_at(baxc, 460)     # simple family prayer
baxc_fm_morn = para_at(baxc, 464)    # family morning
baxc_fm_eve = para_at(baxc, 468)     # family evening
baxc_resurr = para_at(baxc, 472)     # resurrection praise
baxc_oldage = para_at(baxc, 474)     # old age

# ---------- Baxter saints rest: love-debt prayer ----------
baxs = read('baxter-saintsrest.txt').split('\n')
bax_love = para_at(baxs, 1653)

# ---------- Whitefield communion morning (lines 59-63) ----------
wfc = read('arch-whitefield-communion-morning.txt').split('\n')
wf_communion = '\n'.join(wfc[58:63]).strip()

# ---------- Flavel mourners covenant (lines 934-938) ----------
fl = read('arch-flavel-token-mourners.txt').split('\n')
flavel_covenant = '\n'.join(fl[933:938]).strip()

# ---------- Checkbook one-liners ----------
chk = read('spurgeon-checkbook.txt').split('\n')
chk_trial = chk[495].strip()
chk_feb11 = chk[507].strip()
chk_mar9 = chk[824].strip()
chk_apr23 = chk[1358].strip()
chk_may13 = chk[1569].strip()
chk_convict = chk[1974].strip()   # convicted of sin -> deeper hatred of evil
chk_act = chk[1998].strip()       # see God acting
chk_limp = chk[2317].strip()      # limping pilgrim

# ---------- sanity ----------
checks = {
    'spur I': spur_prayers['I'], 'spur II': spur_prayers['II'],
    'spur III': spur_prayers['III'], 'spur V': spur_prayers['V'],
    'spur VI': spur_prayers['VI'], 'spur VII': spur_prayers['VII'],
    'spur VIII': spur_prayers['VIII'], 'spur XI': spur_prayers['XI'],
    'spur XIV': spur_prayers['XIV'], 'spur XVIII': spur_prayers['XVIII'],
    'spur XXI': spur_prayers['XXI'],
    'wf seeker': wf_prayers[0], 'wf hated': wf_prayers[3],
    'wf new': wf_prayers[1],
    'bayly morn': bayly_morning, 'bayly eve': bayly_evening,
    'bax communion': bax_communion, 'bax sick': bax_sick,
    'baxc children': baxc_children, 'baxc morn': baxc_fm_morn,
    'baxc eve': baxc_fm_eve, 'bax love': bax_love,
    'wf communion': wf_communion, 'flavel': flavel_covenant,
    'chk trial': chk_trial, 'chk feb11': chk_feb11, 'chk mar9': chk_mar9,
    'chk apr23': chk_apr23, 'chk may13': chk_may13, 'chk limp': chk_limp,
    'chk act': chk_act,
}
for name, txt in checks.items():
    assert len(txt) > 15, f'TOO SHORT: {name}'
    assert 'NEEDS REVIEW' not in txt, f'NEEDS REVIEW in {name}'
print(f'sanity ok: {len(checks)} excerpts, all clean')

SPUR_T, SPUR_A = 'Lời Cầu Nguyện Của C. H. Spurgeon', 'C. H. Spurgeon'
WF_T, WF_A = 'Những Lời Cầu Nguyện Cho Nhiều Dịp', 'George Whitefield'
BAY_T, BAY_A = 'Thực Hành Sự Tin Kính', 'Lewis Bayly'
BAX_T, BAX_A = 'Lời Thỉnh Nguyện Vì Hòa Bình', 'Richard Baxter'
BAXC_T, BAXC_A = 'Lời Cảnh Báo Đầy Thương Xót', 'Richard Baxter'
BAXS_T, BAXS_A = 'Sự Yên Nghỉ Đời Đời Của Các Thánh', 'Richard Baxter'
WFC_T, WFC_A = 'Bạn Đồng Hành Buổi Dự Tiệc Thánh', 'George Whitefield'
FL_T, FL_A = 'Lời Nhắn Nhủ Cho Kẻ Than Khóc', 'John Flavel'
CHK_T, CHK_A = 'Sổ Séc Của Đức Tin', 'C. H. Spurgeon'

def src(t, a):
    return f'(Trích từ {t} — {a})'

def prayer(title, body, t, a):
    return f'### {title}\n\n{body}\n\n{src(t, a)}'

sections = []
def section(heading, ps):
    sections.append('## ' + heading + '\n\n' + '\n\n---\n\n'.join(ps))

section('I. Ngợi Khen Và Tạ Ơn', [
    prayer('Sự Giúp Đỡ Từ Nơi Cao', spur_prayers['I'], SPUR_T, SPUR_A),
    prayer('Tạ Ơn Đức Chúa Trời', spur_prayers['II'], SPUR_T, SPUR_A),
    prayer('Tình Yêu Không Đo Lường, Không Cùng', spur_prayers['III'], SPUR_T, SPUR_A),
    prayer('Hỡi Linh Hồn Ta, Hãy Ngợi Khen Đức Giê-hô-va', spur_prayers['XIV'], SPUR_T, SPUR_A),
])
section('II. Buổi Sáng Và Buổi Tối', [
    prayer('Lời Cầu Nguyện Buổi Sáng', bayly_morning, BAY_T, BAY_A),
    prayer('Lời Cầu Nguyện Buổi Sáng Cho Gia Đình', baxc_fm_morn, BAXC_T, BAXC_A),
    prayer('Lời Cầu Nguyện Buổi Tối', bayly_evening, BAY_T, BAY_A),
    prayer('Lời Cầu Nguyện Buổi Tối Cho Gia Đình', baxc_fm_eve, BAXC_T, BAXC_A),
])
section('III. Xưng Tội Và Ăn Năn', [
    prayer('Dưới Huyết', spur_prayers['XI'], SPUR_T, SPUR_A),
    prayer('Những Sự Lạ Lùng Của Đồi Can-va-ri', spur_prayers['VI'], SPUR_T, SPUR_A),
    prayer('Lời Cầu Nguyện Của Người Khao Khát Được Tái Sinh', wf_prayers[0], WF_T, WF_A),
])
section('IV. Cầu Thay Cho Người Khác', [
    prayer('Nguyện Mọi Dân Tộc Ngợi Khen Ngài', spur_prayers['VII'], SPUR_T, SPUR_A),
    prayer('Lời Cầu Nguyện Cho Con Cái Và Người Hầu', baxc_children, BAXC_T, BAXC_A),
    prayer('Xin Giúp Con Hầu Việc Chủ Con', chk_may13, CHK_T, CHK_A),
])
section('V. Trong Hoạn Nạn, Bệnh Tật Và Thử Thách', [
    prayer('Lời Cầu Nguyện Cho Người Bị Bắt Bớ Vì Đạo', wf_prayers[3], WF_T, WF_A),
    prayer('Lời Cầu Nguyện Cho Người Bệnh', bax_sick, BAX_T, BAX_A),
    prayer('Lời Giao Ước Của Kẻ Than Khóc', flavel_covenant, FL_T, FL_A),
    prayer('Lời Cầu Nguyện Trong Lò Luyện', chk_trial, CHK_T, CHK_A),
    prayer('Lời Cầu Nguyện Của Kẻ Hành Hương Khập Khiễng', chk_limp, CHK_T, CHK_A),
])
section('VI. Tiệc Thánh Và Đời Sống Hội Thánh', [
    prayer('Dâng Lên Vua Đời Đời', spur_prayers['V'], SPUR_T, SPUR_A),
    prayer('Lời Dọn Lòng Trước Tiệc Thánh', wf_communion, WFC_T, WFC_A),
    prayer('Lời Cầu Nguyện Trước Tiệc Thánh', bax_communion, BAX_T, BAX_A),
])
section('VII. Ân Điển, Đức Tin Và Sự Nên Thánh', [
    prayer('Ôi, Xin Thêm Ân Điển!', spur_prayers['XVIII'], SPUR_T, SPUR_A),
    prayer('Sự Dạn Dĩ Trước Ngai Ân Điển', spur_prayers['XXI'], SPUR_T, SPUR_A),
    prayer('Lời Cầu Nguyện Cho Sự Nên Thánh', spur_prayers['VIII'], SPUR_T, SPUR_A),
])
section('VIII. Lời Cầu Nguyện Ngắn Hằng Ngày', [
    prayer('Món Nợ Tình Yêu', bax_love, BAXS_T, BAXS_A),
    prayer('Xin Làm Trọn Lời Này Cho Con', chk_feb11, CHK_T, CHK_A),
    prayer('Xin Ban Phước Cho Của Cải Chúng Con', chk_mar9, CHK_T, CHK_A),
    prayer('Xin Ban Cho Chúng Con Đức Tin Để Thắng', chk_apr23, CHK_T, CHK_A),
    prayer('Xin Giúp Chúng Con Thấy Ngài Đang Hành Động', chk_act, CHK_T, CHK_A),
])

intro = """# Tuyển Tập Lời Cầu Nguyện Thanh Giáo

Tuyển tập này gồm 30 lời cầu nguyện được sưu tầm từ các bản dịch tiếng Việt trong Thư Viện Cơ Đốc & Thần Học Cải Chánh, gồm những tác giả Thanh giáo và Cải chánh như C. H. Spurgeon, George Whitefield, Richard Baxter, Lewis Bayly và John Flavel. Các lời cầu nguyện được trích nguyên văn từ các bản dịch có sẵn, không dịch mới cũng không chỉnh sửa câu chữ, và được sắp xếp theo tám chủ đề: ngợi khen và tạ ơn, buổi sáng và buổi tối, xưng tội và ăn năn, cầu thay cho người khác, hoạn nạn bệnh tật và thử thách, Tiệc Thánh và đời sống Hội Thánh, ân điển đức tin và sự nên thánh, cùng những lời cầu nguyện ngắn cho mỗi ngày. Xin nói rõ: mọi bản dịch trong thư viện đều do AI hỗ trợ và chưa được mục sư duyệt (AI, chưa duyệt) — tuyển tập sưu tầm này cũng vậy; xin độc giả đối chiếu với Kinh Thánh khi sử dụng.
"""

doc = intro + '\n' + '\n\n'.join(sections) + '\n\nTRANSLATION STATUS: COMPLETE\n'
with open(T + 'tuyen-tap-cau-nguyen-thanh-giao.txt', 'w', encoding='utf-8') as f:
    f.write(doc)
print('wrote anthology')
