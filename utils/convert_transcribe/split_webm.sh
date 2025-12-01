#!/bin/bash

in_dir=${1%/}
segment_seconds=${2:-600}  # default 600 if not given

for in_file in "${in_dir}"/*.webm; do
  [ -e "$in_file" ] || continue
  base="${in_file%.webm}"

  ffmpeg ... -segment_time "$segment_seconds" "${base}_part%03d.webm"
  rm "$in_file"
done