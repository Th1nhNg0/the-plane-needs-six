"""Visual identity v2: mathematical, minimal, 3b1b-spirit (original assets).
- near-black ground, no chrome; LaTeX (Computer Modern) for all text; colours carried by glowing dots and
  translucent regions; clashes shown by the edge itself burning red."""
import numpy as np
from manim import (VGroup, Dot, Circle, Line, DashedLine, Tex, MathTex, ManimColor, RegularPolygon, config,
                   ORIGIN, PI)

BG = ManimColor("#0F1013")
INK = ManimColor("#ECEAE4")
SOFT = ManimColor("#8A8F99")
EDGE = ManimColor("#D4D1CA")
HOT = ManimColor("#FF5A3C")

# Okabe–Ito, colour-blind safe (slightly lifted for glow on black)
PAL = [ManimColor(c) for c in ("#F2A900", "#5BC0F0", "#1FB58F", "#F3E85A", "#3D8FE0", "#E5672A", "#D98CB8")]
ORANGE, SKY, GREEN, YELLOW, BLUE, VERMILLION, PURPLE = range(7)
NAMES = ["orange", "blue", "green", "yellow", "deep blue", "vermillion", "pink"]

config.background_color = BG


def vertex(c=None, r=0.085):
    """Dot with a soft glow, all layers concentric (exact centre = the vertex). c=None -> hollow ink ring."""
    if c is None:
        return VGroup(Circle(radius=r).set_fill(BG, 1).set_stroke(EDGE, 2.5))
    col = PAL[c]
    glow = VGroup(*[Circle(radius=r * k).set_fill(col, a).set_stroke(width=0)
                    for k, a in ((3.2, 0.05), (2.4, 0.08), (1.7, 0.14))])
    return VGroup(glow, Dot(radius=r, color=col))


def edge(p, q, w=3, color=EDGE, opacity=1.0):
    return Line(p, q, stroke_color=color, stroke_width=w, stroke_opacity=opacity)


def burning(p, q, w=5):
    """A clashing edge: hot core with a soft red bloom."""
    return VGroup(Line(p, q, stroke_color=HOT, stroke_width=w * 5, stroke_opacity=0.12),
                  Line(p, q, stroke_color=HOT, stroke_width=w * 2.4, stroke_opacity=0.25),
                  Line(p, q, stroke_color=HOT, stroke_width=w))


def tex(s, size=36, color=INK):
    return Tex(s, font_size=size, color=color)


def math(s, size=40, color=INK):
    return MathTex(s, font_size=size, color=color)


def region(poly, c, opacity=0.38, stroke=1.6):
    return poly.set_fill(PAL[c], opacity).set_stroke(PAL[c], stroke, opacity=0.9)


def note(s, size=24):
    """Small italic aside (used for required epistemic labels instead of UI pills)."""
    return Tex(r"\textit{" + s + "}", font_size=size, color=SOFT)
