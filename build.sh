#!/usr/bin/env bash
# One-command rebuild of "The Plane Needs Six".
#   ./build.sh            full build at 1080p60 -> renders/final.mp4 + renders/final.srt
#   QUALITY=l ./build.sh  fast draft (480p15)
# Narration clips are cached by text hash: only changed sentences are sent to ElevenLabs.
set -euo pipefail
cd "$(dirname "$0")"
QUALITY="${QUALITY:-h}"
JOBS="${JOBS:-6}"

[ -d .venv ] || { uv venv -q .venv --python 3.12 && . .venv/bin/activate && uv pip install -q -r requirements.txt; }
. .venv/bin/activate

python tools/script_tool.py export          # scripts/ch*.md -> scripts/narration.json
python tools/tts.py --all                   # ElevenLabs eleven_v4; cached clips are reused
python tools/assemble_audio.py --all        # per-scene tracks + measured cue times
python tools/align.py --all                 # word timestamps + transcript check (renders nothing)
python tools/render_all.py --quality "$QUALITY" --jobs "$JOBS"
python tools/assemble_final.py              # concat, loudness-normalise, subtitles
if [ -f audio/music/manifest.json ]; then
  python tools/mix_music.py                 # cached music only; no extra API calls or animation renders
  echo "music edition: renders/final_with_music.mp4, renders/final_with_music.srt"
fi
echo "done: renders/final.mp4, renders/final.srt"
