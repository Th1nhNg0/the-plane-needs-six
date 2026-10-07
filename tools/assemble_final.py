"""Assemble renders/scenes/*.mp4 into renders/final.mp4 (loudness-normalised) and write renders/final.srt.

Usage: python tools/assemble_final.py
- every scene gets an AAC 48 kHz audio track (silent if the scene has none, e.g. Credits)
- concatenation copies the video stream (all scenes share Manim's encoder settings)
- loudness: two-pass EBU R128 to -16 LUFS integrated, -1.5 dBTP
- subtitles: the *script* text (exact spelling), timed with the measured word timestamps of each scene
"""
import json
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENE_DIR = ROOT / "renders" / "scenes"
AUDIO = ROOT / "audio" / "scenes"
ORDER = ["S0_1", "S1_1", "S1_2", "S1_3", "S1_4", "S2_1", "S2_2", "S2_3", "S2_4", "S2_5", "S3_1", "S3_2", "S3_3", "S3_4",
         "S4_1", "S4_2", "S4_3", "S4_4", "S5_0", "S5_1", "S5_2", "S5_3", "S5_4", "S5_5", "S6_1", "S6_2", "S6_3", "S6_4",
         "S7_1", "S7_2", "S7_3", "S8_1", "S8_2", "Credits"]
TARGET_I, TARGET_TP = -16.0, -1.5


def run(*a, **kw):
    return subprocess.run(list(a), check=True, capture_output=True, text=True, **kw)


def probe(path, entries):
    out = run("ffprobe", "-v", "error", "-show_entries", entries, "-of", "json", str(path)).stdout
    return json.loads(out)


def duration(path):
    return float(probe(path, "format=duration")["format"]["duration"])


def has_audio(path):
    return any(s.get("codec_type") == "audio" for s in probe(path, "stream=codec_type").get("streams", []))


def normalise_scene(src, dst):
    if has_audio(src):
        run("ffmpeg", "-y", "-v", "error", "-i", str(src), "-map", "0:v", "-map", "0:a", "-c:v", "copy",
            "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k", str(dst))
    else:
        run("ffmpeg", "-y", "-v", "error", "-i", str(src), "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
            "-map", "0:v", "-map", "1:a", "-shortest", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(dst))


def loudnorm(src, dst):
    p = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(src), "-af",
                        f"loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", p.stderr, re.S).group(0))
    af = (f"loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    run("ffmpeg", "-y", "-v", "error", "-i", str(src), "-c:v", "copy", "-af", af, "-ar", "48000",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(dst))
    return m


def norm_words(s):
    return re.findall(r"[a-z0-9]+", s.lower().replace("'", ""))


def fmt(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def chunks(text, maxlen=84):
    words, out, cur = text.split(), [], []
    for w in words:
        if cur and len(" ".join(cur + [w])) > maxlen:
            out.append(cur)
            cur = []
        cur.append(w)
        if re.search(r"[.?!:]$", w) and len(" ".join(cur)) > 30:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def two_lines(ws, width=42):
    s = " ".join(ws)
    if len(s) <= width:
        return s
    best = min(range(1, len(ws)), key=lambda k: abs(len(" ".join(ws[:k])) - len(" ".join(ws[k:]))))
    return " ".join(ws[:best]) + "\n" + " ".join(ws[best:])


def subtitles(offsets):
    cues = []
    for sid, off in offsets:
        tf = AUDIO / f"{sid.lower()}.timing.json"
        wf = AUDIO / f"{sid.lower()}.words.json"
        if not tf.exists():
            continue
        timing = json.loads(tf.read_text())
        words = json.loads(wf.read_text())
        for seg in timing["segments"]:
            sw = [w for w in words if seg["start"] - 0.35 <= w["s"] <= seg["end"] + 0.2]
            n_s = len(seg["text"].split())
            pos = 0
            for ch in chunks(seg["text"]):
                a, b = pos, pos + len(ch)
                pos = b
                if sw:
                    ia = min(int(a * len(sw) / n_s), len(sw) - 1)
                    ib = min(max(int(b * len(sw) / n_s) - 1, ia), len(sw) - 1)
                    t0, t1 = max(sw[ia]["s"], seg["start"] - 0.1), min(sw[ib]["e"] + 0.15, seg["end"] + 0.4)
                else:
                    t0, t1 = seg["start"] + (seg["end"] - seg["start"]) * a / n_s, seg["start"] + (seg["end"] - seg["start"]) * b / n_s
                cues.append((off + t0, off + max(t1, t0 + 0.8), two_lines(ch)))
    # no overlaps
    for i in range(len(cues) - 1):
        if cues[i][1] > cues[i + 1][0]:
            cues[i] = (cues[i][0], cues[i + 1][0] - 0.02, cues[i][2])
    out = "\n".join(f"{i}\n{fmt(a)} --> {fmt(b)}\n{t}\n" for i, (a, b, t) in enumerate(cues, 1))
    (ROOT / "renders" / "final.srt").write_text(out)
    return len(cues)


def main():
    missing = [s for s in ORDER if not (SCENE_DIR / f"{s}.mp4").exists()]
    if missing:
        raise SystemExit(f"missing scene renders: {missing}")
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        lst, offsets, t = [], [], 0.0
        for s in ORDER:
            n = d / f"{s}.mp4"
            normalise_scene(SCENE_DIR / f"{s}.mp4", n)
            lst.append(f"file '{n}'")
            offsets.append((s, t))
            t += duration(n)
        (d / "list.txt").write_text("\n".join(lst) + "\n")
        raw = d / "raw.mp4"
        run("ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(d / "list.txt"), "-c", "copy", str(raw))
        m = loudnorm(raw, ROOT / "renders" / "final.mp4")
    n = subtitles(offsets)
    (ROOT / "renders" / "scene_offsets.json").write_text(json.dumps(offsets, indent=1))
    print(f"final.mp4: {duration(ROOT / 'renders' / 'final.mp4') / 60:.2f} min; input loudness {m['input_i']} LUFS -> {TARGET_I}; "
          f"{n} subtitle cues")


if __name__ == "__main__":
    main()
