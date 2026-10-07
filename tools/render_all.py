"""Render every scene (or a subset) and collect the outputs in renders/scenes/.

Usage: python tools/render_all.py [--quality h|m|l] [--jobs N] [scene ...]
Scenes are listed in film order in SCENES; each renders independently.
"""
import argparse
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENES = [("ch0", "S0_1"), ("ch1", "S1_1"), ("ch1", "S1_2"), ("ch1", "S1_3"), ("ch1", "S1_4"),
          ("ch2", "S2_1"), ("ch2", "S2_2"), ("ch2", "S2_3"), ("ch2", "S2_4"), ("ch2", "S2_5"),
          ("ch3", "S3_1"), ("ch3", "S3_2"), ("ch3", "S3_3"), ("ch3", "S3_4"),
          ("ch4", "S4_1"), ("ch4", "S4_2"), ("ch4", "S4_3"), ("ch4", "S4_4"),
          ("ch5", "S5_0"), ("ch5", "S5_1"), ("ch5", "S5_2"), ("ch5", "S5_3"), ("ch5", "S5_4"), ("ch5", "S5_5"),
          ("ch6", "S6_1"), ("ch6", "S6_2"), ("ch6", "S6_3"), ("ch6", "S6_4"),
          ("ch7", "S7_1"), ("ch7", "S7_2"), ("ch7", "S7_3"),
          ("ch8", "S8_1"), ("ch8", "S8_2"), ("ch8", "Credits")]
QDIR = {"h": "1080p60", "m": "720p30", "l": "480p15"}


def render(ch, sc, q):
    t0 = time.time()
    media = ROOT / "media_jobs" / sc          # one media dir per job: Manim's Tex cache is not safe to share
    p = subprocess.run([sys.executable, "-m", "manim", f"-q{q}", "--media_dir", str(media), f"scenes/{ch}.py", sc],
                       cwd=ROOT, capture_output=True, text=True)
    src = media / "videos" / ch / QDIR[q] / f"{sc}.mp4"
    ok = p.returncode == 0 and src.exists()
    if ok:
        dst = ROOT / "renders" / "scenes" / f"{sc}.mp4"
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    tail = "" if ok else (p.stderr or p.stdout)[-1500:]
    return sc, ok, time.time() - t0, tail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quality", default="h")
    ap.add_argument("--jobs", type=int, default=5)
    ap.add_argument("scenes", nargs="*")
    a = ap.parse_args()
    todo = [(c, s) for c, s in SCENES if not a.scenes or s in a.scenes]
    # longest first so the pool finishes evenly
    order = {"S5_4": 0, "S5_1": 1, "S5_3": 2, "S3_3": 3, "S4_2": 4, "S2_3": 5}
    todo.sort(key=lambda x: order.get(x[1], 99))
    failed = []
    with ThreadPoolExecutor(a.jobs) as ex:
        futs = [ex.submit(render, c, s, a.quality) for c, s in todo]
        for f in as_completed(futs):
            sc, ok, dt, tail = f.result()
            print(f"{'OK  ' if ok else 'FAIL'} {sc} {dt:6.0f}s", flush=True)
            if not ok:
                failed.append(sc)
                print(tail, flush=True)
    print("DONE", "failed:", failed, flush=True)
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
