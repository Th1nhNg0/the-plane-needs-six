"""Assemble one narration track per scene from its clips, with measured cue times.

Usage: python tools/assemble_audio.py s2_3 [...] | --all

For each clip: decode to 48 kHz mono, trim leading/trailing silence (TTS padding), so that the pauses between
segments are exactly the scripted [beat] gaps. The scene track is loudness-normalised (two-pass, linear gain)
to config loudness_lufs. Output:
  audio/scenes/<id>.wav
  audio/scenes/<id>.timing.json  ->  {"duration": s, "segments": [{"i", "start", "end", "text"}]}
Animation reads the timing file: measured audio is the source of truth for timing.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "config" / "voice.json").read_text())
NARR = {s["id"]: s for s in json.loads((ROOT / "scripts" / "narration.json").read_text())}
MAN = json.loads((ROOT / "audio" / "manifest.json").read_text())["clips"]
OUT = ROOT / "audio" / "scenes"
SR = 48000
LEAD_IN = 0.4  # silence before the first word of a scene


def decode(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def trim(x, thresh_db=-45.0, pad=0.03):
    win = int(0.01 * SR)
    n = len(x) // win
    if n == 0:
        return x
    rms = np.sqrt(np.mean(x[: n * win].reshape(n, win) ** 2, axis=1) + 1e-12)
    loud = np.where(20 * np.log10(rms) > thresh_db)[0]
    if len(loud) == 0:
        return x
    a = max(0, loud[0] * win - int(pad * SR))
    b = min(len(x), (loud[-1] + 1) * win + int(pad * SR))
    return x[a:b]


def assemble(sid):
    sc = NARR[sid]
    pieces, segs, t = [np.zeros(int(LEAD_IN * SR), np.float32)], [], LEAD_IN
    for i, text in enumerate(sc["segments"]):
        clip = MAN.get(f"{sid}/{i + 1:02d}")
        if not clip:
            raise SystemExit(f"missing clip {sid}/{i + 1:02d}; run tools/tts.py {sid}")
        x = trim(decode(ROOT / clip["file"]))
        d = len(x) / SR
        segs.append({"i": i + 1, "start": round(t, 3), "end": round(t + d, 3), "text": text})
        pieces.append(x)
        t += d
        if i < len(sc["gaps"]):
            g = sc["gaps"][i]
            pieces.append(np.zeros(int(g * SR), np.float32))
            t += g
    pieces.append(np.zeros(int(CFG["scene_tail_seconds"] * SR), np.float32))
    y = np.concatenate(pieces)
    meter = pyln.Meter(SR)
    y = pyln.normalize.loudness(y, meter.integrated_loudness(y), CFG["loudness_lufs"])
    peak = np.max(np.abs(y))
    if peak > 0.98:
        y *= 0.98 / peak
    OUT.mkdir(parents=True, exist_ok=True)
    sf.write(OUT / f"{sid}.wav", y, SR, subtype="PCM_16")
    timing = {"scene": sid, "duration": round(len(y) / SR, 3), "segments": segs}
    (OUT / f"{sid}.timing.json").write_text(json.dumps(timing, indent=1, ensure_ascii=False))
    print(f"{sid}: {timing['duration']:.2f}s, {len(segs)} segments")


if __name__ == "__main__":
    ids = list(NARR) if "--all" in sys.argv else sys.argv[1:]
    for sid in ids:
        assemble(sid)
