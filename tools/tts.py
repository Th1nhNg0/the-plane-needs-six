"""Generate narration clips with ElevenLabs (one clip per narration segment), cached by text hash.

Usage:
  python tools/tts.py s2_3 [s2_4 ...]     # generate missing clips for these scenes
  python tools/tts.py --all               # every scene in scripts/narration.json
  python tools/tts.py --dry-run s2_3      # show what would be generated and the character cost

Cache key = sha256(model_id, voice_id, voice settings, segment text). Neighbouring text is passed as
previous_text/next_text for prosody continuity but is deliberately NOT part of the key, so editing one
sentence regenerates exactly one clip.
The API key is read from ELEVENLABS_API_KEY, .env, or the legacy ../.env and is never logged.
"""
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "config" / "voice.json").read_text())
NARR = json.loads((ROOT / "scripts" / "narration.json").read_text())
CLIPS = ROOT / "audio" / "clips"
MANIFEST = ROOT / "audio" / "manifest.json"


def api_key():
    if os.environ.get("ELEVENLABS_API_KEY", "").strip():
        return os.environ["ELEVENLABS_API_KEY"].strip()
    for envfile in (ROOT / ".env", ROOT.parent / ".env"):
        if envfile.exists():
            for line in envfile.read_text().splitlines():
                if line.strip().startswith("ELEVENLABS_API_KEY="):
                    value = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if value:
                        return value
    raise SystemExit("Set ELEVENLABS_API_KEY in your environment or .env")


def text_hash(text):
    key = json.dumps([CFG["model_id"], CFG["voice_id"], CFG["voice_settings"], text], sort_keys=True)
    return hashlib.sha256(key.encode()).hexdigest()


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return round(float(out.strip()), 3)


def load_manifest():
    return json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {"clips": {}}


def synth(text, prev, nxt, key):
    body = {"model_id": CFG["model_id"], "text": text, "voice_settings": CFG["voice_settings"]}
    if CFG.get("use_context", True):
        if prev:
            body["previous_text"] = prev
        if nxt:
            body["next_text"] = nxt
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{CFG['voice_id']}?output_format={CFG['output_format']}"
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"xi-api-key": key, "Content-Type": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:300]
            if e.code in (429, 500, 502, 503) and attempt < 3:
                time.sleep(4 * (attempt + 1))
                continue
            raise SystemExit(f"TTS HTTP {e.code}: {msg}")


def main(argv):
    dry = "--dry-run" in argv
    ids = [a for a in argv if not a.startswith("--")]
    scenes = NARR if "--all" in argv else [s for s in NARR if s["id"] in ids]
    if not scenes:
        raise SystemExit("no matching scenes")
    man = load_manifest()
    key = None if dry else api_key()
    cost = 0
    for sc in scenes:
        d = CLIPS / sc["id"]
        d.mkdir(parents=True, exist_ok=True)
        segs = sc["segments"]
        for i, text in enumerate(segs):
            h = text_hash(text)
            name = f"{i + 1:02d}_{h[:10]}"
            mp3 = d / f"{name}.mp3"
            entry_id = f"{sc['id']}/{i + 1:02d}"
            if mp3.exists():
                status = "cached"
            else:
                cost += len(text)
                if dry:
                    print(f"would generate {entry_id} ({len(text)} chars)")
                    continue
                audio = synth(text, segs[i - 1] if i else None, segs[i + 1] if i + 1 < len(segs) else None, key)
                mp3.write_bytes(audio)
                (d / f"{name}.txt").write_text(text + "\n")
                status = "generated"
                print(f"generated {entry_id} ({len(text)} chars)")
            # drop stale clips for this segment index
            for old in d.glob(f"{i + 1:02d}_*"):
                if not old.name.startswith(name):
                    old.unlink()
            man["clips"][entry_id] = {"scene": sc["id"], "segment": i + 1, "model": CFG["model_id"],
                                      "voice_id": CFG["voice_id"], "file": str(mp3.relative_to(ROOT)),
                                      "text_file": str((d / f"{name}.txt").relative_to(ROOT)),
                                      "duration_s": duration(mp3), "text_hash": h, "chars": len(text),
                                      "status": status if status == "cached" and entry_id in man["clips"] else "ok"}
        # drop segments beyond current count
        for old_id in [k for k in man["clips"] if k.startswith(sc["id"] + "/") and int(k.split("/")[1]) > len(segs)]:
            del man["clips"][old_id]
    if not dry:
        MANIFEST.write_text(json.dumps(man, indent=1, ensure_ascii=False))
    print(f"characters {'needed' if dry else 'billed'} this run: {cost}")


if __name__ == "__main__":
    main(sys.argv[1:])
