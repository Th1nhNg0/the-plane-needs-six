"""Unit-distance graph renderer, colouring transitions, clash marker, distance indicator."""
import itertools

import numpy as np
from manim import (Text, Succession, VGroup, VMobject, Line, DashedLine, Dot, Circle, DecimalNumber, AnimationGroup, Succession,
                   Create, FadeIn, FadeOut, Transform, ReplacementTransform, GrowFromCenter, Indicate, Flash,
                   ShowPassingFlash, always_redraw, rate_functions, there_and_back, UP, DOWN, LEFT, RIGHT, ORIGIN, PI)

from .style import BG, INK, MUTED, HOT, HOT_RING, glyph, blank_marker, label, colour, marker, stick, burning

TOL = 1e-6


class UnitGraph(VGroup):
    """Vertices given in *world* coordinates (unit distance = 1); drawn at `scale` manim units per world unit.

    Edges default to all unit-distance pairs. Vertices are glyph markers (blank until coloured)."""

    def __init__(self, points, edges=None, scale=2.0, origin=ORIGIN, marker_size=0.38, stick_width=3.2, **kw):
        super().__init__(**kw)
        self.world = {k: np.array([*p, 0.0][:3], dtype=float) for k, p in points.items()}
        self.scale_ = scale
        self.origin = np.array(origin, dtype=float)
        if edges is None:
            edges = [(a, b) for a, b in itertools.combinations(self.world, 2)
                     if abs(np.linalg.norm(self.world[a] - self.world[b]) - 1) < 1e-9]
        self.edge_keys = list(edges)
        self.colours = {k: None for k in self.world}
        self.marker_size = marker_size
        self.sticks = VGroup(*[self._stick(a, b, stick_width) for a, b in self.edge_keys])
        self.markers = VGroup(*[marker(None, marker_size).move_to(self.pos(k)) for k in self.world])
        self.mk = dict(zip(self.world, self.markers))
        self.st = dict(zip(self.edge_keys, self.sticks))
        self.add(self.sticks, self.markers)

    def pos(self, k):
        return self.origin + self.scale_ * self.world[k]

    def _stick(self, a, b, w):
        return stick(self.pos(a), self.pos(b), w)

    def live_pos(self, k):
        return self.mk[k].get_center()

    # colouring -------------------------------------------------------------------------
    def colour_anim(self, k, c, run_time=0.5):
        """Morph vertex k's marker into colour c's glyph (c=None -> blank)."""
        new = marker(c, self.marker_size).move_to(self.mk[k])
        self.colours[k] = c
        old = self.mk[k]
        anim = Transform(old, new, run_time=run_time)
        return anim

    def set_colour(self, k, c):
        new = marker(c, self.marker_size).move_to(self.mk[k])
        self.mk[k].become(new)
        self.colours[k] = c

    def misalignment(self):
        """Largest distance between a vertex marker's shape centroid and the point where its sticks meet."""
        worst = 0.0
        for k in self.world:
            body = self.mk[k][-1]
            # The invisible frame circle stays a circle through every Transform, and every glyph is built with its
            # centroid at the frame's centre (style.glyph), so the frame centre is the drawn shape's centroid.
            c = self.mk[k][0].get_center()
            ends = [s.get_start() if np.linalg.norm(s.get_start() - c) < np.linalg.norm(s.get_end() - c) else s.get_end()
                    for (a, b), s in zip(self.edge_keys, self.sticks) if k in (a, b)]
            d = max([0.0] + [float(np.linalg.norm(e - c)) for e in ends])
            if d > 1e-3:
                print(f"  misaligned {k}: {d:.4f} body={type(body).__name__} centre={np.round(c, 3)} ends={[np.round(e, 3).tolist() for e in ends]}")
            worst = max(worst, d)
        return worst

    def clashes(self):
        return [(a, b) for a, b in self.edge_keys
                if self.colours[a] is not None and self.colours[a] == self.colours[b]]


def clash(p, q, run_time=0.9):
    """The edge pq burns: returns (animation, residue, extra). Residue = the burning edge, kept on screen."""
    b = burning(p, q)
    anim = Succession(FadeIn(b, run_time=run_time * 0.35),
                      Indicate(b, color=HOT, scale_factor=1.0, run_time=run_time * 0.65))
    return anim, b, VGroup()


class DistanceIndicator(VGroup):
    """Callipers: a dimension line offset from segment (getter_a, getter_b) with end ticks and a live readout.
    `per_unit` converts manim length to world distance. Turns bright ink exactly at 1.000."""

    def __init__(self, get_a, get_b, per_unit=2.0, offset=0.42, side=1, decimals=3, font_size=34, show_line=True):
        super().__init__()
        self.get_a, self.get_b = get_a, get_b
        self.per_unit, self.offset, self.side, self.decimals = per_unit, offset, side, decimals

        def build():
            a, b = np.array(get_a()), np.array(get_b())
            d = b - a
            L = np.linalg.norm(d) + 1e-12
            n = np.array([-d[1], d[0], 0.0]) / L * side
            val = L / per_unit
            exact = abs(val - 1) < 5e-4
            col = INK if exact else MUTED
            a2, b2 = a + n * offset, b + n * offset
            g = VGroup()
            if show_line:
                g.add(Line(a2, b2, stroke_color=col, stroke_width=1.6))
                for e in (a2, b2):
                    g.add(Line(e - n * 0.07, e + n * 0.07, stroke_color=col, stroke_width=1.6))
            num = DecimalNumber(val, num_decimal_places=decimals, font_size=font_size * 1.1, color=col)
            num.move_to((a2 + b2) / 2 + n * 0.3)
            g.add(num)
            return g

        self.add(always_redraw(build))
