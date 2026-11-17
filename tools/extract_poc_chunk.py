#!/usr/bin/env python3
"""Extract the POC chunk for the GitHub Actions audiobook render test.

Takes the Sinners translation, drops the front matter (title + source
notes, everything before the first '## ' heading), strips Markdown
markers, and cuts the first N chars at a sentence boundary so the chunk
is a clean, speakable passage. The same script runs on the Actions
runner and locally, so both renders use a byte-identical chunk.

Usage:
    python3 tools/extract_poc_chunk.py \
        --src translations/308-sinners-in-the-hands-of-an-angry-god-edwards.txt \
        --chars 4000 --out poc-sinners/part_aa.txt
"""

import argparse
import re


def clean(text: str) -> str:
    # Drop Markdown headings markers, emphasis, links (keep link text),
    # bare URLs, and horizontal rules. Keep the words.
    text = re.sub(r"(?m)^#{1,6}\s*", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"https?://\S+", "", text)
    text = text.replace("*", "")
    text = re.sub(r"(?m)^\s*---\s*$", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def main():
    parser = argparse.ArgumentParser(description="Extract POC audiobook chunk")
    parser.add_argument("--src", required=True)
    parser.add_argument("--chars", type=int, default=4000)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    with open(args.src, encoding="utf-8") as handle:
        lines = handle.read().splitlines()

    # Start at the first '## ' heading (the sermon title); everything
    # before it is front matter (title, source notes, links).
    start = next(i for i, line in enumerate(lines) if line.startswith("## "))
    body = clean("\n".join(lines[start:]))

    cut = body[: args.chars]
    # Back off to the last sentence end so we never cut mid-sentence.
    ends = [cut.rfind(m) for m in (". ", "! ", "? ", ".\n", "!\n", "?\n", "… ", "…\n")]
    last = max(ends)
    if last > len(cut) - 600:
        cut = cut[: last + 1]
    else:  # no sentence end nearby: cut at the last space
        cut = cut[: cut.rfind(" ")]

    with open(args.out, "w", encoding="utf-8") as handle:
        handle.write(cut.strip() + "\n")

    print(f"chunk_chars={len(cut.strip())} (asked {args.chars})")
    print(f"first: {cut.strip()[:100]!r}")
    print(f"last: {cut.strip()[-100:]!r}")
    print(f"out={args.out}")


if __name__ == "__main__":
    main()
