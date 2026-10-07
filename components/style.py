"""Visual identity (v2, approved after the Checkpoint C re-review): mathematical and minimal, 3b1b spirit,
original assets.

- near-black ground, no UI chrome (no panels, pills, badges, textures)
- all text set in LaTeX (Computer Modern); on-screen words are sparse, maths preferred
- colours are carried by glowing dots and translucent regions (Okabe–Ito palette, colour-blind safe)
- a clash is shown by the edge itself burning red-orange
Older helper names (label, panel, tag, glyph, marker, stick) are kept so scene code stays stable.
"""
import numpy as np
from manim import (PI, Circle, Dot, Line, VGroup, Tex, MathTex, ManimColor, config)

BG = ManimColor("#0F1013")
INK = ManimColor("#ECEAE4")
SOFT = ManimColor("#8A8F99")
MUTED = SOFT
FAINT = ManimColor("#23262D")
EDGE = ManimColor("#D4D1CA")
HOT = ManimColor("#FF5A3C")
HOT_RING = HOT

PAL = [ManimColor(c) for c in ("#F2A900", "#5BC0F0", "#1FB58F", "#F3E85A", "#3D8FE0", "#E5672A", "#D98CB8")]
COLOURS = [(n, c) for n, c in zip(("orange", "blue", "green", "yellow", "deep blue", "vermillion", "pink"), PAL)]
ORANGE, SKY, GREEN, YELLOW, BLUE, VERMILLION, PURPLE = range(7)
UNIT = 2.0

config.background_color = BG


def colour(i):
    return PAL[i]


# ---------------------------------------------------------------- text ------------------------------------------
_ESC = {"&": r"\&", "%": r"\%", "#": r"\#", "_": r"\_"}  # "$...$" is allowed for inline maths
_SYM = {"≤": r"$\le$", "≥": r"$\ge$", "⇒": r"$\Rightarrow$", "√": r"$\surd$", "≈": r"$\approx$", "·": r"$\cdot$",
        "✓": r"$\checkmark$", "✗": r"$\times$", "→": r"$\to$", "−": "--", "α": r"$\alpha$", "χ": r"$\chi$",
        "θ": r"$\theta$", "≠": r"$\neq$", "≡": r"$\equiv$", "°": r"$^\circ$", "π": r"$\pi$", "–": "--", "—": "---",
        "ő": r"\H{o}", "×": r"$\times$", "○": r"$\circ$"}


def _esc(s):
    return "".join(_SYM.get(ch, _ESC.get(ch, ch)) for ch in s)


def label(text, size=30, color=INK, weight="NORMAL", italic=False, **kw):
    body = _esc(text)
    if weight == "BOLD":
        body = r"\textbf{" + body + "}"
    if italic:
        body = r"\textit{" + body + "}"
    if "\\\\" not in body:
        body = r"\mbox{" + body + "}"      # single line: never let LaTeX wrap it
    return Tex(body, font_size=size * 1.25, color=color)


def maths(tex, size=40, color=INK):
    return MathTex(tex, font_size=size * 1.25, color=color)


def tag(text, size=24, color=SOFT, **kw):
    """Small italic aside (replaces the old pill tags)."""
    return label(text, size, color, italic=True)


def panel(mob, pad=0.0):
    """No chrome: kept for API compatibility, returns the content unchanged."""
    return mob


# ---------------------------------------------------------------- geometry --------------------------------------
def marker(i, size=0.38):
    """Vertex: glowing dot (concentric layers, exact centre) or, for i=None, a hollow ring.
    Element 0 is an invisible frame circle of fixed radius so bounding boxes and transforms never drift."""
    r = size * 0.24
    frame = Circle(radius=size * 0.62, color=BG).set_stroke(BG, width=0, opacity=0).set_fill(BG, opacity=0)
    if i is None:
        body = VGroup(Circle(radius=r * 1.05).set_fill(BG, 1).set_stroke(EDGE, 2.5))
    else:
        col = PAL[i]
        body = VGroup(*[Circle(radius=r * k).set_fill(col, a).set_stroke(width=0)
                        for k, a in ((3.2, 0.05), (2.4, 0.08), (1.7, 0.14))], Dot(radius=r, color=col))
    return VGroup(frame, body).set_z_index(5)


def glyph(i, size=0.3, **kw):
    """Small plain coloured dot (legends, thumbnails)."""
    return Dot(radius=size * 0.32, color=PAL[i])


def blank_marker(size=0.38):
    return marker(None, size)


def stick(p, q, width=3.2, color=None, glow=False):
    return Line(p, q, stroke_color=color or EDGE, stroke_width=width)


def burning(p, q, w=5):
    """A clashing edge: hot core with a soft red bloom."""
    return VGroup(Line(p, q, stroke_color=HOT, stroke_width=w * 5, stroke_opacity=0.12),
                  Line(p, q, stroke_color=HOT, stroke_width=w * 2.4, stroke_opacity=0.25),
                  Line(p, q, stroke_color=HOT, stroke_width=w)).set_z_index(4)


def region(mob, c, opacity=0.32, stroke=1.4):
    return mob.set_fill(PAL[c], opacity).set_stroke(PAL[c], stroke, opacity=0.9)

# compatibility names used by older widget code
PANEL = FAINT
PANEL_EDGE = FAINT
FONT = "Inter"


def backed(mob, opacity=0.8, buff=0.14):
    """Soft background behind text that sits over busy colour (a 3b1b idiom, not a UI panel)."""
    mob.add_background_rectangle(color=BG, opacity=opacity, buff=buff)
    return mob
