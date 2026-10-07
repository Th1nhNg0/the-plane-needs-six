"""Generate the film's background plate: slate ground, faint unit dot lattice ("the plane"), soft vignette.
Writes components/assets/bg.png (3840x2160 so it stays crisp at 1080p and 4K)."""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

W, H = 3840, 2160
PX_PER_UNIT = H / 8.0            # manim frame is 8 units tall
SPACING = 0.5 * PX_PER_UNIT      # lattice spacing: half a manim unit
BASE = np.array([0x16, 0x19, 0x1F], float)
DOT = (0x23, 0x27, 0x30)

img = Image.new("RGB", (W, H), tuple(int(c) for c in BASE))
d = ImageDraw.Draw(img)
r = 2.6
cx, cy = W / 2, H / 2
for i in range(-40, 41):
    for j in range(-25, 26):
        x, y = cx + i * SPACING, cy + j * SPACING
        if 0 <= x < W and 0 <= y < H:
            d.ellipse([x - r, y - r, x + r, y + r], fill=DOT)
a = np.asarray(img).astype(float)
yy, xx = np.mgrid[0:H, 0:W]
rad = np.sqrt(((xx - cx) / (W / 2)) ** 2 + ((yy - cy) / (H / 2)) ** 2) / np.sqrt(2)
vig = np.ones_like(rad)                              # flat: gradients band after h264 compression
a = a * vig[..., None]
out = Path(__file__).resolve().parents[1] / "components" / "assets"
out.mkdir(parents=True, exist_ok=True)
Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(out / "bg.png", optimize=True)
print("wrote", out / "bg.png")
