#!/bin/bash
# master_chunk.sh — raw TTS wav -> mastered mp3.
# SAME chain as render-one.sh tts_one (voice locked 2026-11-17):
# atempo 0.92 (~214 wpm -> ~196 wpm) + 0.5 s trailing silence, then
# acompressor + alimiter + loudnorm two-pass (I=-20, TP=-3.5, LRA=11).
# NEVER apply noise reduction to TTS material (measured damage).
#
# Usage: master_chunk.sh <in.wav> <out.mp3> [atempo]
set -euo pipefail
IN="$1"; OUT="$2"; ATEMPO="${3:-0.92}"
[ -s "$IN" ] || { echo "FAILED: missing or empty wav: $IN" >&2; exit 1; }
ffmpeg -y -v error -i "$IN" -f lavfi -i anullsrc=r=24000:cl=mono \
  -filter_complex "[0:a]atempo=${ATEMPO}[a];[1:a]atrim=0:0.5[s];[a][s]concat=n=2:v=0:a=1[out]" \
  -map "[out]" -b:a 128k "$OUT.tmp.mp3"
ffmpeg -v info -i "$OUT.tmp.mp3" \
  -af "acompressor=threshold=-18dB:ratio=2:attack=0.2:release=1,alimiter=limit=-3.5dB,loudnorm=I=-20:TP=-3.5:LRA=11:print_format=json" \
  -f null - 2> "$OUT.loudnorm.log"
read -r MI MTP MLRA MTHRESH MOFF <<<"$(python3 - "$OUT.loudnorm.log" <<'PYEOF'
import json, sys
s = open(sys.argv[1]).read()
j = json.loads(s[s.index('{'):s.rindex('}') + 1])
print(j['input_i'], j['input_tp'], j['input_lra'], j['input_thresh'], j['target_offset'])
PYEOF
)"
echo "loudnorm measured: I=$MI TP=$MTP LRA=$MLRA thresh=$MTHRESH offset=$MOFF"
ffmpeg -y -v error -i "$OUT.tmp.mp3" \
  -af "acompressor=threshold=-18dB:ratio=2:attack=0.2:release=1,alimiter=limit=-3.5dB,loudnorm=I=-20:TP=-3.5:LRA=11:measured_I=${MI}:measured_TP=${MTP}:measured_LRA=${MLRA}:measured_thresh=${MTHRESH}:offset=${MOFF}:linear=true" \
  -ar 24000 -b:a 128k "$OUT"
rm -f "$OUT.tmp.mp3" "$OUT.loudnorm.log"
[ -s "$OUT" ] || { echo "FAILED: empty mp3: $OUT" >&2; exit 1; }
echo "mastered: $OUT ($(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")s)"
