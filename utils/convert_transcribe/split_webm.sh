IN_DIR="/home/users/ntu/daniel02/scratch/GigaSpeech2/id/raw_audio/mono/Idntimes/audio"
SEGMENT_SECONDS=600 # 10 mins

# Loop through all .webm files in IN_DIR
for in_file in "${IN_DIR}"/*.webm; do
  [ -e "$in_file" ] || continue  # Skip if no files

  base="${in_file%.webm}"

  ffmpeg -hide_banner -loglevel error -y \
    -i "$in_file" \
    -c copy \
    -map 0 \
    -f segment \
    -segment_time "$SEGMENT_SECONDS" \
    -reset_timestamps 1 \
    "${base}_part%03d.webm"

  rm "$in_file"
done
