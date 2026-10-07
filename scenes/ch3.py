"""Chapter 3 · Hadwiger–Nelson: 68 years at 4–7, then 5.   manim -qh scenes/ch3.py S3_1 S3_2 S3_3 S3_4"""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.style import (BG, INK, MUTED, SOFT, EDGE, HOT, ORANGE, SKY, GREEN, YELLOW, BLUE, VERMILLION, PURPLE,
                              PAL, colour, label, maths, tag, marker, stick, burning, region, backed)
from components.graph import UnitGraph, DistanceIndicator
from components.widgets import BoundsLine, hex_tiling, paper_card, WildPlane, unit_stick
from components.narrated import NarratedScene
from scenes.ch2 import spindle_points, SPINDLE_EDGES, rot

S = 2.0
R = 0.4 * S            # hexagon circumradius in manim units (r = 2/5)


def mini_spindle(scale=0.5, angle=0.0, colours=None):
    P = {k: rot(v, angle) for k, v in spindle_points().items()}
    g = UnitGraph(P, scale=scale, marker_size=0.2, stick_width=1.6)
    if colours:
        for k, c in colours.items():
            g.set_colour(k, c)
    return g.move_to(ORIGIN)


class S3_1(NarratedScene):
    scene_id = "s3_1"

    def construct(self):
        W = self.word
        legend = VGroup(*[marker(i, 0.42) for i in range(7)]).arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.6)
        self.play_at(W("seven"), LaggedStart(*[FadeIn(m, scale=0.4) for m in legend], lag_ratio=0.12), run_time=1.0)

        # cue 2: one hexagon, radius 2/5, widest 0.8
        h0 = region(RegularPolygon(6, radius=R, start_angle=PI / 2), ORANGE, opacity=0.35, stroke=2.5)
        self.play_at(W("hexagon", 1), DrawBorderThenFill(h0), run_time=1.0)
        rad = Line(ORIGIN, h0.get_vertices()[1], stroke_color=INK, stroke_width=2.5)
        rlab = maths(r"r = \tfrac{2}{5}", 34, INK).next_to(rad, RIGHT, buff=0.15).shift(DOWN * 0.15)
        self.play_at(W("radius"), Create(rad), Write(rlab), run_time=0.9)
        v = h0.get_vertices()
        diam = Line(v[0], v[3], stroke_color=INK, stroke_width=2.5)
        ind = DistanceIndicator(lambda: diam.get_start(), lambda: diam.get_end(), per_unit=S, offset=0.0, side=1,
                                show_line=False, font_size=34)
        ind.shift(LEFT * 1.2)
        self.play_at(W("widest"), FadeOut(rad), FadeOut(rlab), Create(diam), run_time=0.9)
        ind = VGroup()
        no1 = maths(r"\text{widest} = 2r = 0.8 < 1", 36, INK).next_to(h0, RIGHT, buff=0.8)
        self.play_at(W("no", 1), Write(no1), run_time=0.8)

        # cue 3: the 7-flower, then the tiling
        tiling, cells = hex_tiling(R, 7)
        cells_arr = np.array([c[0] for c in cells])
        centre_idx = int(np.argmin(np.linalg.norm(cells_arr, axis=1)))
        flower_idx = [i for i, (p, c) in enumerate(cells) if np.linalg.norm(p - cells[centre_idx][0]) < np.sqrt(3) * R + 1e-6]
        flower = VGroup(*[tiling[i] for i in flower_idx])
        rest = VGroup(*[t for i, t in enumerate(tiling) if i not in flower_idx])
        self.play_at(W("repeating"), FadeOut(VGroup(h0, diam, ind, no1)), FadeIn(tiling[centre_idx]), run_time=0.8)
        self.play_at(W("surrounded"), LaggedStart(*[FadeIn(tiling[i], scale=0.8) for i in flower_idx if i != centre_idx],
                                                  lag_ratio=0.15), run_time=1.6)
        self.play_at(W("tile"), FadeIn(rest, lag_ratio=0.003), run_time=2.0)
        self.bring_to_front(legend)

        # cue 4: same colour far apart: at least (sqrt21 - 2) r
        c0 = cells[centre_idx]
        same = sorted([c for c in cells if c[1] == c0[1] and np.linalg.norm(c[0] - c0[0]) > 1e-6],
                      key=lambda c: np.linalg.norm(c[0] - c0[0]))
        c1 = same[0]
        assert abs(np.linalg.norm(c1[0] - c0[0]) - np.sqrt(21) * R) < 1e-6      # centres sqrt(21) r apart
        dim = [t.animate.set_fill(opacity=0.08).set_stroke(opacity=0.25) for t, (p, c) in zip(tiling, cells) if c != c0[1]]
        self.play_at(W("same", 1), *dim, run_time=1.0)
        circ = VGroup(*[DashedVMobject(Circle(radius=R, stroke_color=INK, stroke_width=2).move_to(c[0]), num_dashes=40)
                        for c in (c0, c1)])
        u = (c1[0] - c0[0]) / np.linalg.norm(c1[0] - c0[0])
        gap = Line(c0[0] + u * R, c1[0] - u * R, stroke_color=INK, stroke_width=4)
        gap_lab = backed(maths(r"\ge (\sqrt{21} - 2)\,r \approx 1.033", 34, INK)).next_to(gap, UP, buff=0.3)
        self.play_at(W("nearest"), Create(circ), run_time=1.0)
        self.play_at(W("one", 3), Create(gap), run_time=0.8)
        self.play_at(W("least"), Write(gap_lab), run_time=1.2)

        # cue 5: any stick lands on two colours; 7 suffice; borders
        undim = [t.animate.set_fill(opacity=0.32).set_stroke(opacity=0.9) for t, (p, c) in zip(tiling, cells) if c != c0[1]]
        self.play_at(W("so", after=42), FadeOut(VGroup(circ, gap, gap_lab)), *undim, run_time=0.8)
        colour_at = lambda p: cells[int(np.argmin(np.linalg.norm(cells_arr - p, axis=1)))][1]
        s_in = unit_stick(c0[0] + LEFT * 0.35 + DOWN * 0.1, 0.3, 0.7 / 1.0 * 1.0 * 0 + 0.7)   # short: inside one hexagon
        s_in = VGroup(Line(c0[0] + LEFT * 0.3, c0[0] + RIGHT * 0.3, stroke_color=EDGE, stroke_width=3.2),
                      marker(c0[1], 0.36).move_to(c0[0] + LEFT * 0.3), marker(c0[1], 0.36).move_to(c0[0] + RIGHT * 0.3))
        self.play_at(W("stays"), FadeIn(s_in), run_time=0.6)
        rng = np.random.default_rng(1)
        sticks = VGroup()
        for _ in range(6):
            while True:
                p = np.array([rng.uniform(-5, 5), rng.uniform(-2.6, 2.4), 0])
                a = rng.uniform(0, TAU)
                q = p + S * np.array([np.cos(a), np.sin(a), 0])
                if abs(q[0]) < 6.5 and abs(q[1]) < 3.2:
                    break
            assert colour_at(p) != colour_at(q), "a unit stick joined two same-coloured hexagons"
            sticks.add(unit_stick(p, a, S, colour_at(p), colour_at(q)))
        self.play_at(W("reaches"), FadeOut(s_in), LaggedStart(*[FadeIn(s) for s in sticks], lag_ratio=0.2), run_time=1.4)
        le7 = backed(maths(r"\chi(\mathbb{R}^2) \le 7", 52, INK)).move_to(DOWN * 2.6)
        self.play_at(W("seven", 3), Write(le7), run_time=1.0)
        self.play_at(W("borders"), Indicate(VGroup(*[tiling[i] for i in flower_idx]), color=INK, scale_factor=1.0), run_time=1.2)

        # cue 6: the bounds and the history
        bl = BoundsLine(4, 7, y=-2.4)
        self.play_at(self.cue(6), FadeOut(VGroup(tiling, sticks, legend, le7)), FadeIn(bl), run_time=1.0)
        chips = [(W("nelson", 1), bl.chip("Nelson, 1950", 4, size=24)),
                 (W("isbell"), bl.chip("Isbell, 1950", 7, size=24)),
                 (W("hugo"), label("published by Hadwiger, 1961", 26, MUTED).move_to(UP * 0.4))]
        for t, c in chips:
            self.play_at(t, FadeIn(c, shift=UP * 0.15), run_time=0.7)
        ms = mini_spindle(0.55).next_to(chips[2][1], RIGHT, buff=0.6)
        self.play_at(W("moser"), FadeIn(ms), run_time=0.7)
        name = label("The Hadwiger--Nelson problem", 46, INK).to_edge(UP, buff=0.9)
        self.play_at(W("became"), Write(name), run_time=1.4)

        # cue 7: sixty-eight years without movement
        year = ValueTracker(1950)
        yr = always_redraw(lambda: Integer(int(year.get_value()), group_with_commas=False, font_size=48, color=INK)
                           .move_to(UP * 1.6))
        self.play_at(self.cue(7), FadeOut(VGroup(chips[2][1], ms)), FadeIn(yr), run_time=0.5)
        self.play(year.animate.set_value(2017), run_time=self.left(self.audio_duration - 0.6), rate_func=linear)
        self.finish()


class S3_2(NarratedScene):
    scene_id = "s3_2"

    def construct(self):
        W = self.word
        q5 = maths(r"\chi(\mathbb{R}^2) \ge 5\ ?", 56, INK).move_to(UP * 1.5)
        self.play_at(W("suppose"), Write(q5), run_time=1.0)
        ms = mini_spindle(0.9)
        qm = maths("?", 60, MUTED).next_to(ms, RIGHT, buff=0.4)
        self.play_at(W("finite"), FadeIn(ms), FadeIn(qm), run_time=0.8)

        # cue 2: de Bruijn–Erdős
        who = label("de Bruijn & Erd\\H{o}s, 1951", 30, MUTED).to_edge(UP, buff=0.6)
        thm = maths(r"\text{every finite part is } k\text{-colourable} \;\iff\; \text{the whole graph is } k\text{-colourable}",
                    32, INK)
        self.play_at(W("theorem"), FadeOut(VGroup(q5, ms, qm)), FadeIn(who), run_time=0.8)
        self.play_at(W("every", 1), Write(thm), run_time=2.4)

        # cue 3: patches lock together (triangular lattice, a unit-distance graph, coloured (i - j) mod 3)
        self.play_at(self.cue(3), thm.animate.scale(0.75).to_edge(DOWN, buff=0.5), run_time=0.8)
        L = 1.0
        a, b = np.array([L, 0, 0]), np.array([L / 2, L * np.sqrt(3) / 2, 0])
        pts = {}
        for i in range(-9, 10):
            for j in range(-6, 7):
                p = i * a + j * b + UP * 0.4
                if abs(p[0]) < 6.6 and -2.3 < p[1] < 3.2:
                    pts[(i, j)] = p
        good = {k: (k[0] - k[1]) % 3 for k in pts}
        cols3 = [ORANGE, SKY, GREEN]
        patches = [(np.array([-3.0, 1.0, 0]), [0, 1, 2]), (np.array([0.2, -0.3, 0]), [1, 2, 0]),
                   (np.array([3.2, 1.2, 0]), [2, 0, 1])]
        rings = VGroup()
        dots = {}
        for centre, perm in patches:
            rings.add(Circle(radius=2.0, stroke_color=MUTED, stroke_width=2).move_to(centre))
            for k, p in pts.items():
                if np.linalg.norm(p - centre) < 2.0:
                    dots[k] = Dot(p, radius=0.09, color=PAL[cols3[perm[good[k]]]])
        edges = VGroup(*[Line(pts[k], pts[k2], stroke_color=EDGE, stroke_width=1.2, stroke_opacity=0.5)
                         for k in pts for d in ((1, 0), (0, 1), (-1, 1)) for k2 in [(k[0] + d[0], k[1] + d[1])]
                         if k2 in pts and k in dots and k2 in dots])
        self.play_at(W("patches"), Create(rings), FadeIn(edges), FadeIn(VGroup(*dots.values())), run_time=1.4)
        self.play_at(W("own"), Indicate(rings, color=INK, scale_factor=1.03), run_time=0.8)
        self.play_at(W("consistently"), *[d.animate.set_color(PAL[cols3[good[k]]]) for k, d in dots.items()], run_time=1.0)
        all_dots = VGroup(*[Dot(p, radius=0.09, color=PAL[cols3[good[k]]]) for k, p in pts.items()])
        all_edges = VGroup(*[Line(pts[k], pts[k2], stroke_color=EDGE, stroke_width=1.2, stroke_opacity=0.5)
                             for k in pts for d in ((1, 0), (0, 1), (-1, 1)) for k2 in [(k[0] + d[0], k[1] + d[1])]
                             if k2 in pts])
        self.play_at(W("lock"), FadeOut(rings), FadeIn(all_edges), FadeIn(all_dots), run_time=1.4)

        # cue 4: turned around
        back = maths(r"\chi(\mathbb{R}^2) \ge 5 \;\Longrightarrow\; \text{some finite unit-distance } G \text{ has } \chi(G) \ge 5",
                     34, INK).move_to(UP * 0.3)
        self.play_at(W("turn"), FadeOut(VGroup(all_dots, all_edges, edges, *dots.values())), run_time=0.8)
        self.play_at(W("if", 2), Write(back), run_time=2.2)
        back6 = maths(r"\chi(\mathbb{R}^2) \ge 6 \;\Longrightarrow\; \text{some finite unit-distance } G \text{ has } \chi(G) \ge 6",
                      34, INK).move_to(back)
        self.play_at(W("six"), TransformMatchingTex(back, back6), run_time=1.0)

        # cue 5: a target in principle, size unknown
        blob = VGroup(*[mini_spindle(0.35, ang).shift(np.array([np.cos(ang) * 0.9, np.sin(ang) * 0.6, 0]))
                        for ang in np.linspace(0, TAU, 7)[:-1]]).move_to(DOWN * 1.4)
        size = maths(r"|V(G)| = \ ?", 40, INK).next_to(blob, RIGHT, buff=0.8)
        self.play_at(W("hunt"), FadeIn(blob), run_time=1.0)
        self.play_at(W("big"), Write(size), run_time=0.9)

        # cue 6: axiom of choice
        aside = label("relies on the axiom of choice", 30, MUTED, italic=True).to_edge(DOWN, buff=0.4)
        self.play_at(W("axiom"), FadeOut(thm), FadeIn(aside), run_time=0.8)
        self.finish()


class S3_3(NarratedScene):
    scene_id = "s3_3"

    def construct(self):
        W = self.word
        card = paper_card("The chromatic number\nof the plane is at least 5", "Aubrey D. N. J. de Grey · April 2018",
                          w=3.6, h=4.4).scale(0.9)
        self.play_at(W("aubrey"), FadeIn(card, shift=UP * 0.3), run_time=1.0)

        # cue 2: build up, 20425 -> 1581
        rng = np.random.default_rng(3)
        cloud = VGroup(*[mini_spindle(0.4, rng.uniform(0, TAU), {k: c for k, c in zip(spindle_points(), [0, 1, 2, 0, 1, 2, 3])})
                         .shift(np.array([rng.normal(0, 1.6), rng.normal(0, 0.9), 0])) for _ in range(28)])
        cloud.move_to(LEFT * 1.6)
        self.play_at(W("approach"), card.animate.scale(0.55).to_corner(UL, buff=0.4), run_time=0.8)
        self.play_at(W("spindle"), LaggedStart(*[FadeIn(c, scale=0.6) for c in cloud], lag_ratio=0.05), run_time=2.2)
        n = ValueTracker(20425)
        count = always_redraw(lambda: VGroup(Integer(int(n.get_value()), group_with_commas=False, font_size=56, color=INK),
                                             label("vertices", 32, MUTED)).arrange(RIGHT, buff=0.25).move_to(RIGHT * 4 + UP * 0.5))
        self.play_at(W("20"), FadeIn(count), run_time=0.6)
        own = label("checked with his own program", 28, MUTED, italic=True).next_to(count, DOWN, buff=0.4)
        self.play_at(W("programme", 1), FadeIn(own), run_time=0.6)
        self.play_at(W("shrank"), n.animate.set_value(1581), cloud.animate.scale(0.55), run_time=1.6)

        # cue 3: 4^1581 has 952 digits (shown exactly)
        big = 4 ** 1581
        digits = str(big)
        assert len(digits) == 952
        self.play_at(self.cue(3), FadeOut(VGroup(cloud, own, card)), run_time=0.6)
        self.remove(count)
        f = maths(r"4^{1581}", 72, INK).move_to(UP * 1.6)
        self.play_at(W("four", 2), Write(f), run_time=1.0)
        rows = VGroup(*[Text(digits[i:i + 64], font="DejaVu Sans Mono", font_size=20, color=MUTED)
                        for i in range(0, 64 * 6, 64)]).arrange(DOWN, buff=0.12, aligned_edge=LEFT).next_to(f, DOWN, buff=0.5)
        more = label("\\ldots 952 digits in all", 28, INK, italic=True).next_to(rows, DOWN, buff=0.3)
        self.play_at(W("number", after=40), FadeIn(rows, lag_ratio=0.1), run_time=1.4)
        self.play_at(W("digits"), FadeIn(more), run_time=0.6)

        # cue 4: translate into logic; SAT solver
        self.play_at(W("instead"), FadeOut(VGroup(f, rows, more)), run_time=0.6)
        rh = {"a": (-0.5, 0), "b": (0.5, 0), "c": (0, np.sqrt(3) / 2), "d": (0, -np.sqrt(3) / 2)}
        g = UnitGraph(rh, scale=1.6, origin=LEFT * 4.2 + UP * 0.2)
        self.play_at(W("logic"), FadeIn(g), run_time=0.8)
        var = maths(r"x_{v,c} \;=\; \text{``vertex } v \text{ has colour } c\text{''}", 34, INK).move_to(RIGHT * 1.6 + UP * 1.6)
        cl1 = maths(r"x_{v,1} \lor x_{v,2} \lor x_{v,3} \lor x_{v,4}", 32, INK).next_to(var, DOWN, buff=0.45)
        cl2 = maths(r"\lnot\,(x_{u,c} \land x_{v,c}) \quad \text{for each edge } uv", 32, INK).next_to(cl1, DOWN, buff=0.35)
        self.play_at(W("variable"), Write(var), run_time=1.4)
        self.play_at(W("possible", 2), Write(cl1), run_time=1.0)
        self.play_at(W("constraint"), Write(cl2), Indicate(g.sticks, color=INK, scale_factor=1.0), run_time=1.4)
        box = RoundedRectangle(corner_radius=0.15, width=3.0, height=1.2, stroke_color=INK, stroke_width=2.5)
        box_l = label("SAT solver", 34, INK).move_to(box)
        solver = VGroup(box, box_l).move_to(RIGHT * 1.6 + DOWN * 2.0)
        arr = Arrow(cl2.get_bottom(), solver.get_top(), buff=0.15, color=MUTED, stroke_width=2.5)
        self.play_at(W("sat", 1), GrowArrow(arr), FadeIn(solver), run_time=0.9)

        # cue 5: refutation = certificate; a small separate checker
        self.play_at(W("answer"), FadeOut(VGroup(g, var, cl1, cl2, arr)), solver.animate.move_to(LEFT * 4.2), run_time=0.9)
        no = label("no proper 4-colouring", 30, INK, italic=True).next_to(solver, DOWN, buff=0.3)
        self.play_at(W("no", 1), FadeIn(no), run_time=0.6)
        steps = VGroup(*[maths(t, 28, INK) for t in (r"C_1", r"C_2", r"C_3", r"\vdots", r"C_{m}", r"\bot")]).arrange(DOWN, buff=0.18)
        scroll = VGroup(SurroundingRectangle(steps, buff=0.25, color=MUTED, stroke_width=2), steps).move_to(ORIGIN)
        a1 = Arrow(solver.get_right(), scroll.get_left(), buff=0.2, color=MUTED, stroke_width=2.5)
        self.play_at(W("refutation"), GrowArrow(a1), FadeIn(scroll, shift=RIGHT * 0.3), run_time=1.0)
        self.play_at(W("contradiction"), Indicate(steps[-1], color=HOT, scale_factor=1.4), run_time=0.9)
        cert = label("certificate", 32, INK).next_to(scroll, UP, buff=0.3)
        self.play_at(W("certificate", 1), Write(cert), run_time=0.8)
        cbox = VGroup(RoundedRectangle(corner_radius=0.12, width=2.0, height=0.9, stroke_color=INK, stroke_width=2.5),
                      label("checker", 30, INK)).move_to(RIGHT * 4.2)
        cbox[1].move_to(cbox[0])
        a2 = Arrow(scroll.get_right(), cbox.get_left(), buff=0.2, color=MUTED, stroke_width=2.5)
        ok = maths(r"\checkmark", 52, colour(GREEN)).next_to(cbox, DOWN, buff=0.3)
        self.play_at(W("checking", 1), GrowArrow(a2), FadeIn(cbox), run_time=0.9)
        trust = label("no need to trust the solver", 26, MUTED, italic=True).next_to(cbox, UP, buff=0.4)
        self.play_at(W("trusting"), FadeIn(trust), run_time=0.6)
        self.play_at(W("simpler"), FadeIn(ok, scale=1.3), run_time=0.6)

        # cue 6: Polymath16, Heule, Parts
        self.play_at(self.cue(6), FadeOut(VGroup(solver, no, a1, scroll, cert, a2, cbox, trust, ok)), run_time=0.8)
        tl = VGroup(
            VGroup(label("Polymath16", 32, INK), label("an online collaboration, April 2018", 24, MUTED)),
            VGroup(label("Heule, 2018", 32, INK), label("553 vertices; certificates of 14,000--19,000 steps, about 1 s to check", 24, MUTED)),
            VGroup(label("Parts, 2020", 32, INK), label("509 vertices; and a proof a human can verify by hand", 24, MUTED)),
        )
        for row in tl:
            row.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        tl.arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to(UP * 0.4)
        self.play_at(W("polymath"), FadeIn(tl[0], shift=RIGHT * 0.2), run_time=0.8)
        self.play_at(W("553") - 1.5, FadeIn(tl[1], shift=RIGHT * 0.2), run_time=0.8)
        self.play_at(W("parts"), FadeIn(tl[2], shift=RIGHT * 0.2), run_time=0.8)

        # cue 7: the number line moves
        bl = BoundsLine(4, 7, y=-2.7)
        self.play_at(self.cue(7), FadeIn(bl), tl.animate.shift(UP * 0.3).set_opacity(0.6), run_time=0.9)
        self.play_at(W("five", after=126), Transform(bl.bracket, bl.set_bounds(5, 7)), run_time=1.0)
        yr = label("2018", 28, MUTED).next_to([bl.x(6), bl.y, 0], UP, buff=0.45)
        self.play(FadeIn(yr), run_time=0.5)
        self.finish()


class S3_4(NarratedScene):
    scene_id = "s3_4"

    def construct(self):
        W = self.word
        bl = BoundsLine(5, 7, y=-2.7)
        self.add(bl)
        blob = VGroup(*[mini_spindle(0.35, ang).shift(np.array([np.cos(ang) * 0.9, np.sin(ang) * 0.6, 0]))
                        for ang in np.linspace(0, TAU, 9)[:-1]]).move_to(UP * 0.9).fade(0.65)
        q6 = maths(r"\chi(G) \ge 6\ ?", 44, INK).next_to(blob, RIGHT, buff=0.7)
        self.play_at(W("found"), FadeIn(blob), Write(q6), run_time=1.2)
        note = label("none published, as far as I can find", 28, MUTED, italic=True).next_to(blob, DOWN, buff=0.5)
        self.play_at(W("as"), FadeIn(note), run_time=0.8)
        must = maths(r"\chi(\mathbb{R}^2) \ge 6 \;\Longrightarrow\; \text{such a } G \text{ exists}", 36, INK).to_edge(UP, buff=0.6)
        self.play_at(W("compactness"), Write(must), run_time=1.4)
        size = maths(r"|V(G)| = \ ?", 40, INK).next_to(q6, DOWN, buff=0.4)
        self.play_at(W("size"), Write(size), run_time=0.8)
        plane = WildPlane(cell=0.2, seed=41, dim=0.3)
        self.play_at(W("stranger"), FadeOut(VGroup(blob, q6, note, must, size, bl)), FadeIn(plane.image), run_time=1.6)
        self.finish()
