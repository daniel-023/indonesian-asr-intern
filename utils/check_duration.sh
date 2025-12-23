RAW="/scratch/users/ntu/daniel02/GigaSpeech2/en/raw_audio/id/onlyabidoang/audio"

module load ffmpeg

find "$RAW" -type f -name '*.webm' -print0 \
  | xargs -0 -I{} ffprobe -v error -show_entries format=duration \
      -of default=noprint_wrappers=1:nokey=1 {} 2>/dev/null \
  | awk '{
      s += $1; 
      c++ 
    } END {
      printf "Files   : %d\n", c;
      printf "H:M:S   : %02d:%02d:%02d\n",
             s/3600, (s%3600)/60, s%60
    }'