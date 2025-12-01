# Remove trailing slash from input dir
in_dir="${1%/}"

# Output file
out_dir="${2%/}"
mkdir -p "$out_dir"
manifest="$out_dir/input_manifest.json"

# Generate JSONL manifest
find "$in_dir" -name "*.webm" -print0 \
  | xargs -0 -I{} echo "{\"source_audio_filepath\": \"{}\"}" \
  > "$manifest"

echo "Created manifest at: $manifest"