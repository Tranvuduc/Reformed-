#!/usr/bin/env python3
"""Shared topic mapping for the hub's Learn modules (Phase 2).

The encyclopedia's loci tags (scripts/helper-data/encyclopedia-loci.json)
are the single source of truth for "which doctrine is this about". Hỏi Đáp
questions are grouped by the locus of their first related encyclopedia
entry, with a small curated OVERRIDES table for the few questions whose
first link points at a neighbouring doctrine (reviewed by the integrator
2026-11-11 against each question's wording).

Used by scripts/build_answers.py (topic field + grouped landing) and by any
future grouping (learning paths, hubs). Pure functions + data: importing
this module has no side effects.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
_loci = json.loads((ROOT / "scripts/helper-data/encyclopedia-loci.json").read_text(encoding="utf-8"))

LOCI = {l["id"]: l for l in _loci["loci"]}
# slug -> locus id (exactly one primary locus per encyclopedia entry)
SLUG_TO_LOCUS = {}
for _lid, _slugs in _loci["map"].items():
    for _s in _slugs:
        assert _s not in SLUG_TO_LOCUS, f"duplicate locus assignment: {_s}"
        SLUG_TO_LOCUS[_s] = _lid

# Question slug -> locus id, for questions whose first related encyclopedia
# entry belongs to a neighbouring doctrine. Reasons (integrator, 2026-11-11):
# - duc-tin-va-khoa-hoc: first link is duc-tin (faith) but the question is
#   about whether Scripture and science conflict -> Kinh Thánh & Mặc Khải.
# - an-tu-thuoc-linh: first link is su-phuc-vu (service) but the question
#   is about gifts IN the church -> Hội Thánh & Thánh Lễ.
# - phep-la-va-an-tu-dac-biet: first link is phep-la (God's power) but the
#   question is about the Spirit's gifts continuing -> Đức Thánh Linh.
# - ma-quy-co-that: first link is ma-quy (the Devil) but the question is
#   "should believers fear?" — a Christian-life question -> Đời Sống.
# - su-keu-goi-cua-chua-trong-doi-song: first link is su-keu-goi (effectual
#   calling) but the question is about vocation in daily life -> Đời Sống.
# - an-chay-co-doc: first link is kieng-an (fasting) which IS doi-song;
#   kept here explicitly so a future loci change cannot move it silently.
OVERRIDES = {
    "duc-tin-va-khoa-hoc-co-mau-thuan-khong": "kinh-thanh",
    "an-tu-thuoc-linh-la-gi-lam-sao-biet-an-tu-cua-minh": "hoi-thanh",
    "phep-la-va-an-tu-dac-biet-con-tiep-dien-khong": "duc-thanh-linh",
    "ma-quy-co-that-khong-tin-huu-co-nen-so-khong": "doi-song",
    "su-keu-goi-cua-chua-trong-doi-song-la-gi": "doi-song",
    "an-chay-co-doc-la-gi-co-can-khong": "doi-song",
}


def locus_of_encyclopedia_slug(slug):
    """Locus id for an encyclopedia slug ('tien-dinh' is the pre-fix alias)."""
    if slug == "tien-dinh":
        slug = "su-tien-dinh"
    return SLUG_TO_LOCUS[slug]


def topic_for_answer(answer):
    """Topic (locus id) for one answers-starters entry.

    Rule: the locus of the first related encyclopedia entry, unless the
    question slug is in OVERRIDES. Raises KeyError on an unknown slug so a
    bad link fails the build loudly instead of silently mis-grouping.
    """
    slug = answer["slug"]
    if slug in OVERRIDES:
        return OVERRIDES[slug]
    return locus_of_encyclopedia_slug(answer["related_encyclopedia"][0])


def topic_name(locus_id):
    return LOCI[locus_id]["name_vi"]
