#!/bin/sh
for file in *.mp4; do
  # Extract audio (if it doesn't exist)
  audio_file="${file%.*}.aac"

  if [ ! -s "$audio_file" ]; then
    ffmpeg -y -i "$file" -vn "$audio_file"
  fi

  # Create directory for the subtitles
  out_dir="${file%.*}/cz"
  mkdir -p "$out_dir"

  # Run whisperx + symlink the video (if the directory is empty)
  if [ -z "$(ls -A "$out_dir")" ]; then
    whisperx "$audio_file" \
        --model large-v3 \
        --language Czech \
        --segment_resolution chunk \
        --task transcribe \
        --output_dir "$out_dir" \
        --output_format srt

    ln -s "../../$(basename "$file")" "$out_dir/$(basename "$file")"
  fi
done
