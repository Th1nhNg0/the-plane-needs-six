"""Parse the chapter scripts (scripts/ch*.md).

Usage:
  python tools/script_tool.py timing   # estimate durations, write `time:` fields, print table
  python tools/script_tool.py export   # write scripts/narration.json (scene -> segments) for the TTS step

Each scene's narration is split at [beat] / [beat2] markers into segments; each segment is one TTS clip.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
WPM = 150.0
BEAT = {"[beat]": 0.6, "[beat2]": 1.4}
SCENE_TAIL = 1.0  # silence after each scene's narration (seconds)

SCENE_RE = re.compile(r"^## (S\d+\.\d+) · (.+?)(?:\s+←.*)?$", re.M)
META_RE = re.compile(r"`id: (\w+)` · `target: (\d+):(\d+)` · `time: [^`]*`")


def parse():
    scenes = []
    for path in sorted(SCRIPTS.glob("ch[0-9].md")):
        text = path.read_text()
        heads = list(SCENE_RE.finditer(text))
        for k, h in enumerate(heads):
            body = text[h.end(): heads[k + 1].start() if k + 1 < len(heads) else len(text)]
            meta = META_RE.search(body)
            narr = re.search(r"\*\*NARRATION\*\*\n((?:>.*\n?)+)", body)
            if not (meta and narr):
                raise SystemExit(f"{path.name} {h.group(1)}: missing id/target or NARRATION")
            prose = " ".join(l[1:].strip() for l in narr.group(1).splitlines())
            parts = re.split(r"(\[beat2?\])", prose)
            segs, gaps = [], []
            for p in parts:
                if p in BEAT:
                    gaps.append(BEAT[p])
                elif p.strip():
                    segs.append(p.strip())
            gaps = gaps[: max(len(segs) - 1, 0)]
            scenes.append(dict(file=path.name, label=h.group(1), title=h.group(2).strip(),
                               id=meta.group(1), target=int(meta.group(2)) * 60 + int(meta.group(3)),
                               segments=segs, gaps=gaps))
    return scenes


def est(scene):
    words = sum(len(s.split()) for s in scene["segments"])
    return words, words / WPM * 60 + sum(scene["gaps"]) + SCENE_TAIL


def mmss(t):
    return f"{int(t // 60)}:{int(round(t % 60)):02d}"


def timing():
    scenes = parse()
    t = 0.0
    rows, chars = [], 0
    for s in scenes:
        words, d = est(s)
        s["start"], s["end"] = t, t + d
        t += d
        chars += sum(len(x) for x in s["segments"])
        rows.append((s["label"], s["title"], words, d, s["target"]))
    # write back
    for path in sorted(SCRIPTS.glob("ch[0-9].md")):
        text = path.read_text()
        for s in scenes:
            if s["file"] != path.name:
                continue
            text = re.sub(rf"(`id: {s['id']}` · `target: \d+:\d+` · )`time: [^`]*`",
                          lambda m: m.group(1) + f"`time: {mmss(s['start'])}–{mmss(s['end'])} (est.)`", text)
        path.write_text(text)
    print(f"{'scene':7} {'title':42} {'words':>5} {'est':>6} {'target':>6}")
    for label, title, w, d, tg in rows:
        flag = "  <-- off by >25%" if abs(d - tg) > 0.25 * tg else ""
        print(f"{label:7} {title[:42]:42} {w:5d} {mmss(d):>6} {mmss(tg):>6}{flag}")
    print(f"TOTAL narration+beats ≈ {mmss(t)}  | TTS characters ≈ {chars}  | segments = {sum(len(s['segments']) for s in scenes)}")


def export():
    scenes = parse()
    out = [dict(id=s["id"], label=s["label"], title=s["title"], segments=s["segments"], gaps=s["gaps"]) for s in scenes]
    (SCRIPTS / "narration.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"wrote {len(out)} scenes")


if __name__ == "__main__":
    {"timing": timing, "export": export}[sys.argv[1] if len(sys.argv) > 1 else "timing"]()
