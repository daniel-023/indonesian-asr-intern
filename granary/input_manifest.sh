RAW=/scratch/users/ntu/daniel02/Granary/id/raw_audio/granary_test
OUT=/scratch/users/ntu/daniel02/Granary/input_manifest.json

find "$RAW" -name "*.webm" -print0 \
  | xargs -0 -I{} echo "{\"source_audio_filepath\": \"{}\"}" \
  > "$OUT"