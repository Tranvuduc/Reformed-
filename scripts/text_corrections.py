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
3. Split-letter artifact (approved by Duc 2026-11-08): in 667 verses the
   initial letter Â/Ấ of a word was digitised as two letters, "A"+"â/á"
   (671 tokens: "Aáy"->"Ấy" x654, "Aân"->"Ân" x5, "Aâm"->"Âm" x9,
   "Aán-độ"->"Ấn-độ" x2, "Aâu-gu"->"Âu-gu" x1). Merged back mechanically
   at word starts. The merged forms agree with the printed 1934 text
   (kinhthanh.httlvn.org VI1934). Note Acts 27:1: print reads "Âu-gu-ta"
   while the digital source carries "gu ta" as separate words — only the
   letter is merged here; the source's wording is otherwise untouched.
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
    # One-word typo in the digital source ("đều" for "điều"), confirmed
    # against three independent printed-1934 copies (bible.com VIE1925,
    # bible.alpha.org, caugocmoingay.com); approved by Duc 2026-11-08.
    ("psa", 34, 4): "Tôi đã tìm cầu Đức Giê-hô-va, Ngài đáp lại tôi, "
                    "Giải cứu tôi khỏi các điều sợ hãi.",
    # Batch 2026-11-17 (Molly's call): 13 verses where the digital source
    # AND the hub agree on a wrong reading, found by Ken's wide OCR scan of
    # the Bible-app data (241 fixes / 211 verses, 17/11) and fixed the same
    # day in the app repo (f0e4122). Each reading below is verified against
    # HTTLVN VI1934 (+ KJV where noted); the hub's old reading is the same
    # OCR error the app had. Esai 9:6 decided by Molly in Round 101
    # (2 independent 1934 witnesses agree "Ồ"; KJV "O my God").
    ("jug", 16, 9): "Vả, tại trong phòng ở nhà nàng có binh phục. Nàng nói: "
                    "Ớ Sam-sôn, người Phi-li-tin xông hãm ngươi! Song người bứt "
                    "những sợi dây như một sợi chỉ gai đứt khi đụng đến lửa. "
                    "Như vậy, căn nguyên sức mạnh người chẳng tìm ra được.",
    ("jug", 16, 12): "Vậy, Đa-li-la lấy dây lớn mới, trói Sam-sôn rồi nói rằng: "
                     "Ớ Sam-sôn, người Phi-li-tin xông hãm ngươi! Vả, có binh "
                     "đang phục trong một phòng. Nhưng người bứt đứt những sợi "
                     "dây lớn trói cánh tay, y như một sợi chỉ vậy.",
    ("jug", 16, 14): "Đa-li-la lấy con sẻ cột chặt lại, rồi la rằng: "
                     "Ớ Sam-sôn, người Phi-li-tin xông hãm ngươi! Nhưng người "
                     "thức dậy, nhổ con sẻ của khung cửi ra luôn với canh chỉ.",
    ("jug", 16, 20): "Bấy giờ nàng nói: Ớ Sam-sôn, người Phi-li-tin xông hãm "
                     "ngươi! Người thức dậy mà rằng: Ta sẽ ra như các lần "
                     "trước, và gỡ mình cho thoát khỏi tay chúng nó! Nhưng "
                     "người chẳng biết rằng Đức Giê-hô-va đã lìa khỏi mình.",
    ("jug", 7, 11): "Ngươi sẽ nghe điều chúng nó nói, rồi ngươi sẽ cảm biết "
                    "rằng mình có sức mạnh mà hãm dinh chúng nó. Vậy, "
                    "Ghê-đê-ôn đi xuống cùng Phu-ra, đầy tớ mình, đến gần "
                    "nơi lính canh ở đầu dinh.",
    ("psa", 101, 2): "Tôi sẽ ăn ở cách khôn ngoan trong đường trọn vẹn; "
                     "Ồ! Chúa chừng nào sẽ đến cùng tôi? Tôi sẽ lấy lòng "
                     "trọn vẹn mà ăn ở trong nhà tôi.",
    ("job", 11, 18): "Ông sẽ ở bình an vô sự, vì có sự trông cậy; Ông sẽ "
                     "tìm tòi bốn bên, rồi nghỉ ngơi yên hàn vô sự.",
    ("prov", 23, 14): "Khi con đánh nó bằng roi vọt, Ắt giải cứu linh hồn "
                      "nó khỏi âm phủ.",
    ("1sam", 16, 2): "Sa-mu-ên thưa rằng: Làm sao tôi đi đó được? Nếu "
                     "Sau-lơ hay, thì sẽ giết tôi đi. Đức Giê-hô-va phán "
                     "cùng người rằng: Hãy đem theo ngươi một con bò cái tơ, "
                     "và nói rằng: Tôi đến để dâng của tế lễ cho Đức Giê-hô-va.",
    ("exo", 16, 3): "nói cùng hai người rằng: Ôi! thà rằng chúng tôi chịu "
                    "chết về tay Đức Giê-hô-va tại xứ Ê-díp-tô, khi còn ngồi "
                    "kề nồi thịt và ăn bánh chán hê! Vì hai người dẫn dắt "
                    "chúng tôi vào nơi đồng vắng nầy đặng làm cho cả đoàn "
                    "dân đông nầy đều bị chết đói.",
    # 2 Chr 22:2 "hai mươi hai": HTTLVN VI1934 + 2 Vua 8:26 (22, same king);
    # the digital source's "hai mươi" (20) has no manuscript support — an
    # OCR drop of "hai" from "hai mươi hai" (42 of KJV/MT is impossible:
    # his father Jehoram died at 40).
    ("2chron", 22, 2): "A-cha-xia được hai mươi hai tuổi khi người tức vị; "
                       "người cai trị một năm tại Giê-ru-sa-lem; tên mẹ người "
                       "là A-tha-li, con gái của Ôm-ri.",
    ("est", 6, 13): "Ha-man thuật lại cho Xê-rết, vợ mình, và các bạn hữu "
                    "mình hay mọi điều đã xảy đến cho mình. Khi ấy các người "
                    "khôn ngoan và Xê-rết, vợ người, nói rằng: Ông đã khởi "
                    "mòi sa bại trước mặt Mạc-đô-chê rồi; nếu hắn quả thuộc "
                    "về dòng dõi dân Giu-đa, thì ông sẽ chẳng thắng hắn được "
                    "đâu, nhưng sẽ sa bại quả hẳn trước mặt người.",
    ("esai", 9, 6): "mà thưa với Ngài rằng: Ồ, Đức Chúa Trời tôi! tôi hổ "
                    "ngươi thẹn mặt, chẳng dám ngước mặt lên Ngài, là Đức "
                    "Chúa Trời tôi; vì gian ác chúng tôi đã thêm nhiều quá "
                    "đầu chúng tôi, và tội chúng tôi cao lớn tận trời.",
}

MARKER = re.compile(r"^\(\d{1,3}[-:]\d{1,3}\)\s*")

SPLIT = re.compile(r"(?<!\w)A([áâ])")

def _merge_split(m):
    return "Ấ" if m.group(1) == "á" else "Â"

def merge_split(text):
    """Merge the split Â/Ấ artifact (defect class 3) in any rendered text —
    also applied to the app’s study notes, which quote verses with the
    same artifact (4 tokens in 3 notes)."""
    return SPLIT.sub(_merge_split, text)

def fix_verse(bid, ch, vs, text):
    fixed = FIXES.get((bid, ch, vs))
    if fixed is not None:
        return fixed
    return merge_split(MARKER.sub("", text))
