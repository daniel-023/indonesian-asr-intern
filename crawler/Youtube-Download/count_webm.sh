#!/usr/bin/env bash
# Usage: ./count_webm.sh [BASE_DIR]
set -euo pipefail

BASE="${1:-/content/drive/MyDrive/GigaSpeech2/id/raw_audio}"

# How many parallel probes to run (falls back sensibly on macOS/others)
CORES="$( (command -v nproc >/dev/null && nproc) || (command -v sysctl >/dev/null && sysctl -n hw.ncpu) || echo 4 )"

grand_files=0
grand_seconds=0

echo "📊 Summary of all channels in $BASE"
echo "----------------------------------------------------"

# Speed up awk a touch
export LC_ALL=C

for channel_dir in "$BASE"/*; do
  [[ -d "$channel_dir" ]] || continue

  channel="$(basename "$channel_dir")"
  audio_dir="$channel_dir/audio"

  if [[ ! -d "$audio_dir" ]]; then
    echo "⚠️  Skipping $channel (no audio/ folder)"
    continue
  fi

  # Gather files once (null-delimited; safe for weird filenames)
  mapfile -d '' files < <(find "$audio_dir" -type f -name '*.webm' -print0)

  num_files="${#files[@]}"
  if (( num_files == 0 )); then
    echo "🎞️  Channel: $channel"
    echo "    Videos: 0"
    echo "    Duration: 0.00 hours"
    echo "----------------------------------------------------"
    continue
  fi

  # Parallel ffprobe across files and sum durations
  # - If ffprobe fails on a file, treat its duration as 0 to keep things moving.
  total_seconds="$(
    printf '%s\0' "${files[@]}" \
    | xargs -0 -n 1 -P "$CORES" -I{} bash -c '
        d=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$1" 2>/dev/null || true)
        # Guard against empty/NaN output
        if [[ -z "$d" || "$d" == "N/A" ]]; then echo 0; else echo "$d"; fi
      ' _ {} \
    | awk '{s+=$1} END{printf "%.6f", s}'
  )"

  total_hours="$(awk -v s="$total_seconds" 'BEGIN {printf "%.2f", s/3600}')"

  echo "🎞️  Channel: $channel"
  echo "    Videos: $num_files"
  echo "    Duration: $total_hours hours"
  echo "----------------------------------------------------"

  # Accumulate grand totals (use awk to keep floating precision)
  grand_files=$((grand_files + num_files))
  grand_seconds="$(awk -v g="$grand_seconds" -v t="$total_seconds" 'BEGIN {printf "%.6f", g+t}')"
done

grand_hours="$(awk -v s="$grand_seconds" 'BEGIN {printf "%.2f", s/3600}')"

echo "📊 GRAND TOTAL"
echo "    Total videos: $grand_files"
echo "    Total duration: $grand_hours hours"
