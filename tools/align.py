"""Word-level alignment and transcript check of assembled scene audio (local faster-whisper).

Usage: python tools/align.py s2_3 [...] | --all
Writes audio/scenes/<id>.words.json and prints a word-diff between the script and what was heard, which flags
mispronounced or dropped words for QA.
"""
import difflib
import json
import re
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
from faster_whisper import WhisperModel

ROOT = Path(__file__).resolve().parents[1]
SC = ROOT / "audio" / "scenes"
_model = None


def model():
    global _model
    if _model is None:
        _model = WhisperModel("small.en", device="cpu", compute_type="int8")
    return _model


def norm(s):
    return re.findall(r"[a-z0-9]+", s.lower().replace("'", ""))


def align(sid):
    y, sr = sf.read(SC / f"{sid}.wav", dtype="float32")
    if sr != 16000:
        idx = np.arange(0, len(y), sr / 16000)
        y = np.interp(idx, np.arange(len(y)), y).astype(np.float32)
    segs, _ = model().transcribe(y, word_timestamps=True, language="en", beam_size=5)
    words = [{"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)} for s in segs for w in s.words]
    (SC / f"{sid}.words.json").write_text(json.dumps(words, ensure_ascii=False))
    timing = json.loads((SC / f"{sid}.timing.json").read_text())
    script = norm(" ".join(s["text"] for s in timing["segments"]))
    heard = norm(" ".join(w["w"] for w in words))
    sm = difflib.SequenceMatcher(a=script, b=heard, autojunk=False)
    diffs = [(op, " ".join(script[a1:a2]), " ".join(heard[b1:b2])) for op, a1, a2, b1, b2 in sm.get_opcodes() if op != "equal"]
    # dead air: gaps between consecutive words > 2 s
    gaps = [(words[i]["e"], words[i + 1]["s"]) for i in range(len(words) - 1) if words[i + 1]["s"] - words[i]["e"] > 2.0]
    print(f"{sid}: {len(words)} words, match ratio {sm.ratio():.3f}, gaps>2s: {gaps}")
    for d in diffs:
        print("   ", d)


if __name__ == "__main__":
    ids = [p.name.split(".")[0] for p in sorted(SC.glob("*.timing.json"))] if "--all" in sys.argv else sys.argv[1:]
    for sid in ids:
        align(sid)
