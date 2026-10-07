"""Style frames for approval (stills).  manim -qh -s scenes/style_test.py Frame1 Frame2 Frame3"""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.look import (BG, INK, SOFT, EDGE, HOT, PAL, ORANGE, SKY, GREEN, vertex, edge, burning, tex, math,
                             region)

R3 = np.sqrt(3)
THETA = np.arccos(5 / 6)


def axis(phi):
    return np.array([-np.sin(phi), np.cos(phi), 0.0])


def rot(v, a):
    c, s = np.cos(a), np.sin(a)
    return np.array([c * v[0] - s * v[1], s * v[0] + c * v[1], 0.0])


def rhombus(phi):
    d = axis(phi)
    return {"m1": rot(d, PI / 6), "m2": rot(d, -PI / 6), "t": R3 * d}


class Frame1(Scene):
    """The spindle at the moment the far tips reach distance exactly 1."""

    def construct(self):
        S, PIN = 2.6, np.array([0, -2.7, 0])
        sc = lambda w: PIN + S * np.asarray(w)
        r1, r2 = rhombus(-THETA / 2), rhombus(THETA / 2)
        P = {"p": np.zeros(3), "a1": r1["m1"], "b1": r1["m2"], "t1": r1["t"],
             "a2": r2["m1"], "b2": r2["m2"], "t2": r2["t"]}
        col = {"p": ORANGE, "a1": SKY, "b1": GREEN, "t1": ORANGE, "a2": SKY, "b2": GREEN, "t2": ORANGE}
        E = [("p", "a1"), ("p", "b1"), ("a1", "b1"), ("a1", "t1"), ("b1", "t1"),
             ("p", "a2"), ("p", "b2"), ("a2", "b2"), ("a2", "t2"), ("b2", "t2")]
        arc = DashedVMobject(Arc(radius=S * R3, start_angle=60 * DEGREES, angle=60 * DEGREES, arc_center=PIN,
                                 stroke_color=SOFT, stroke_width=1.5), num_dashes=24)
        guides = VGroup(*[DashedLine(sc(P["p"]), sc(P[t]), dash_length=0.08, stroke_color=SOFT, stroke_width=1.5)
                          for t in ("t1", "t2")])
        self.add(arc, guides)
        self.add(*[edge(sc(P[a]), sc(P[b])) for a, b in E])
        self.add(burning(sc(P["t1"]), sc(P["t2"])))
        self.add(*[vertex(col[k]).move_to(sc(P[k])) for k in P])
        d = math(r"|t_1 t_2| = 1", 40).next_to(VGroup(Dot(sc(P["t1"])), Dot(sc(P["t2"]))), UP, buff=0.45)
        eq1 = math(r"t_1 \equiv p", 34, SOFT).next_to(sc(P["t1"]), RIGHT, buff=0.35)
        eq2 = math(r"t_2 \equiv p", 34, SOFT).next_to(sc(P["t2"]), LEFT, buff=0.35)
        lp = math("p", 34, SOFT).next_to(sc(P["p"]), DOWN, buff=0.25)
        self.add(d, eq1, eq2, lp)


class Frame2(Scene):
    """A 3-colouring by hexagons fails: one unit stick joins two same-coloured cells."""

    def construct(self):
        R = 0.8   # circumradius in manim units (0.4 world units at 2 units per world unit)
        w = np.sqrt(3) * R
        g = VGroup()
        cells = []
        for r in range(-5, 6):
            for q in range(-9, 10):
                x, y = w * (q + r / 2), 1.5 * R * r
                if abs(x) > 8 or abs(y) > 4.8:
                    continue
                c = [ORANGE, SKY, GREEN][(q - r) % 3]
                g.add(region(RegularPolygon(6, radius=R, start_angle=PI / 2).move_to([x, y, 0]), c, opacity=0.30,
                             stroke=1.2))
                cells.append(((q, r), np.array([x, y, 0]), c))
        self.add(g)
        a = np.array([0.0, 0.0, 0])
        u = np.array([np.cos(PI / 6), np.sin(PI / 6), 0])          # towards the same-coloured cell (1, 1)
        p, q = a + u * 0.2, a + u * 2.2                             # length 2.0 manim = 1 world unit
        for (qq, rr), cpos, c in cells:
            if (qq, rr) in ((0, 0), (1, 1)):
                self.add(RegularPolygon(6, radius=R, start_angle=PI / 2).move_to(cpos).set_stroke(PAL[c], 4).set_fill(opacity=0))
        self.add(burning(p, q), vertex(ORANGE).move_to(p), vertex(ORANGE).move_to(q))
        lab = math(r"|pq| = 1", 40).next_to(Line(p, q), UP, buff=0.35).shift(LEFT * 0.4)
        self.add(BackgroundRectangle(lab, fill_color=BG, fill_opacity=0.75, buff=0.12), lab)


class Frame3(Scene):
    """Title card."""

    def construct(self):
        S, PIN = 1.1, np.array([3.6, -2.2, 0])
        sc = lambda w: PIN + S * np.asarray(w)
        r1, r2 = rhombus(-THETA / 2), rhombus(THETA / 2)
        P = [np.zeros(3), r1["m1"], r1["m2"], r1["t"], r2["m1"], r2["m2"], r2["t"]]
        E = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (0, 4), (0, 5), (4, 5), (4, 6), (5, 6), (3, 6)]
        ghost = VGroup(*[edge(sc(P[a]), sc(P[b]), w=2, opacity=0.35) for a, b in E],
                       *[vertex(c).move_to(sc(P[i])) for i, c in enumerate([0, 1, 2, 0, 1, 2, 3])])
        title = tex(r"The Plane Needs Six", 84)
        sub = math(r"6 \le \chi(\mathbb{R}^2) \le 7", 44, SOFT).next_to(title, DOWN, buff=0.5)
        VGroup(title, sub).move_to(LEFT * 1.4 + UP * 0.4)
        self.add(ghost, title, sub)
