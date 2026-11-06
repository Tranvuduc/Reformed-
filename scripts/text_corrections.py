#!/usr/bin/env python3
"""Surgical corrections to the Bible app's 1934 verse data, applied by every
hub generator that renders verse text (build_bible, build_catechism,
build_encyclopedia). Approved by Duc 2026-11-06 ("Repair the corrupted verses
against the printed 1934 text"). The Bible app repo itself is NOT modified —
these fixes live in the hub's render pipeline so they survive regeneration.

Two defect classes, both verified against the source data 2026-11-06:
1. Mojibake / truncation in 4 verses. Restored to the printed 1934 wording;
   Gen 40:12 and Ezek 48:35 additionally cross-checked against independent
   online copies of the 1934 text (kinhthanh.httlvn.org VI1934; VIE1925 on
   bible.com / vietchristian BTT), which agree word-for-word.
2. Leading reference markers "(039-22)" style left in 242 verses by the
   digital source's alternate numbering. Not part of the printed text;
   stripped mechanically.
"""
import re

FIXES = {
    ("mat", 6, 10): "Nước Cha được đến; ý Cha được nên, ở đất như trời!",
    ("isa", 55, 8): "Đức Giê-hô-va phán: Ý tưởng ta chẳng phải ý tưởng các ngươi, "
                    "đường lối các ngươi chẳng phải đường lối ta.",
    ("gen", 40, 12): "Giô-sép nói: Ý-nghĩa chiêm bao đó là thể nầy: "
                     "Ba nhành nho tức là ba ngày.",
    ("ezek", 48, 35): "Châu vi thành sẽ có mười tám ngàn cần; và rày về sau "
                      "tên thành sẽ là: “Đức Giê-hô-va ở đó!”",
}

MARKER = re.compile(r"^\(\d{1,3}[-:]\d{1,3}\)\s*")

def fix_verse(bid, ch, vs, text):
    fixed = FIXES.get((bid, ch, vs))
    if fixed is not None:
        return fixed
    return MARKER.sub("", text)
