#!/usr/bin/env bash
# Final mastering pass: two-pass loudnorm to -14 LUFS / -1 dBTP, video re-encoded at high quality.
# Usage: build/master.sh renders/v2-raw.mp4 renders/skinny-fat-reel-v2.mp4
set -euo pipefail
IN="$1"; OUT="$2"
J=$(ffmpeg -hide_banner -i "$IN" -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/{/,/}/p')
MI=$(echo "$J" | python3 -I -c "import json,sys;d=json.load(sys.stdin);print(f\"measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}\")")
ffmpeg -v error -y -i "$IN" -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11:$MI:linear=true" -ar 48000 -c:a aac -b:a 192k -movflags +faststart "$OUT"
ffmpeg -hide_banner -i "$OUT" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):" | tail -2
