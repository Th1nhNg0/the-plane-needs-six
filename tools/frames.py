"""Extract frames from a render and tile them into a labelled contact sheet for visual QA.

Usage: python tools/frames.py VIDEO OUT.png [t1 t2 ...]   (default: every 6 s)
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw


def main(video, out, times):
    if not times:
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                    video], capture_output=True, text=True).stdout)
        times = [round(t, 1) for t in list(frange(1.0, dur - 0.2, 6.0))]
    tiles = []
    with tempfile.TemporaryDirectory() as d:
        for t in times:
            p = Path(d) / f"{t}.png"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", video, "-frames:v", "1",
                            "-vf", "scale=640:-1", str(p)], check=True)
            im = Image.open(p).convert("RGB")
            ImageDraw.Draw(im).text((8, 6), f"{t:.1f}s", fill=(255, 80, 80))
            tiles.append(im)
    cols = 3
    w, h = tiles[0].size
    sheet = Image.new("RGB", (cols * w + (cols - 1) * 4, ((len(tiles) + cols - 1) // cols) * (h + 4)), (60, 60, 60))
    for i, im in enumerate(tiles):
        sheet.paste(im, ((i % cols) * (w + 4), (i // cols) * (h + 4)))
    sheet.save(out)
    print(out, len(tiles), "frames")


def frange(a, b, s):
    while a < b:
        yield a
        a += s


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3:]])
