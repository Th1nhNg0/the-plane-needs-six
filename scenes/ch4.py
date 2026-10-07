"""Chapter 4 · Why 6 is harder.   manim -qh scenes/ch4.py S4_1 S4_2 S4_3 S4_4"""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.style import (BG, INK, MUTED, SOFT, EDGE, HOT, ORANGE, SKY, GREEN, YELLOW, PAL, colour, label, maths,
                              tag, marker, burning, region, backed)
from components.widgets import BoundsLine, hex_tiling, stripes, WildPlane
from components.narrated import NarratedScene
from scenes.ch3 import mini_spindle

ALPHA = np.sqrt(2) / 10           # irrational fraction of a full turn


class S4_1(NarratedScene):
    scene_id = "s4_1"

    def construct(self):
        W = self.word
        goal = maths(r"\text{prove } \chi(\mathbb{R}^2) \ge 6", 44, INK).to_edge(UP, buff=0.6)
        self.play_at(W("six"), Write(goal), run_time=1.0)
        g = mini_spindle(1.2, colours={k: c for k, c in zip(["p", "a1", "b1", "t1", "a2", "b2", "t2"], [0, 1, 2, 0, 1, 2, 3])})
        self.play_at(W("five", 1), FadeIn(g), run_time=0.8)
        rng = np.random.default_rng(2)
        fanout = VGroup(*[mini_spindle(0.45, 0, {k: int(rng.integers(5)) for k in ["p", "a1", "b1", "t1", "a2", "b2", "t2"]})
                          for _ in range(24)])
        fanout.arrange_in_grid(4, 6, buff=0.35).scale(0.9).move_to(DOWN * 0.3)
        self.play_at(W("every"), FadeOut(g), LaggedStart(*[FadeIn(f, scale=0.7) for f in fanout], lag_ratio=0.03), run_time=1.2)
        count = backed(maths(r"5^{1000} \text{ colourings}", 52, INK)).move_to(DOWN * 0.3).set_z_index(10)
        self.play_at(W("power"), Write(count), fanout.animate.fade(0.75), run_time=1.2)

        # cue 2: and the graph must first be found
        hay = VGroup(*[mini_spindle(rng.uniform(0.25, 0.5), rng.uniform(0, TAU)).move_to([rng.uniform(-6.3, 6.3),
                                                                                             rng.uniform(-3.4, 2.6), 0])
                       for _ in range(40)]).fade(0.7)
        self.play_at(W("before"), FadeOut(VGroup(fanout, count)), run_time=0.6)
        self.play_at(W("found"), LaggedStart(*[FadeIn(h) for h in hay], lag_ratio=0.02), run_time=1.6)
        qm = backed(maths(r"\text{which } G\,?", 48, INK))
        self.play_at(W("unimaginably"), Write(qm), run_time=0.9)

        # cue 3 / 4: existence vs non-existence
        self.play_at(W("compare"), FadeOut(VGroup(hay, qm, goal)), run_time=0.7)
        divider = Line(UP * 3.2, DOWN * 2.6, stroke_color=MUTED, stroke_width=1.5)
        lt = label("a colouring exists", 34, INK).move_to(LEFT * 3.5 + UP * 2.9)
        rt = label("no colouring exists", 34, INK).move_to(RIGHT * 3.5 + UP * 2.9)
        tiles, _ = hex_tiling(0.35, 7, extent=(5.2, 3.6), center=LEFT * 3.5 + DOWN * 0.1)
        self.play_at(W("show", 2), Create(divider), FadeIn(lt), FadeIn(tiles), run_time=1.0)
        one = label("one example, anyone can check it", 28, MUTED, italic=True).next_to(tiles, DOWN, buff=0.35)
        self.play_at(W("one", 2), FadeIn(one), run_time=0.7)
        self.play_at(W("proving"), FadeIn(rt), run_time=0.7)
        steps = VGroup(*[maths(t, 26, INK) for t in (r"C_1", r"C_2", r"\vdots", r"\bot")]).arrange(DOWN, buff=0.12)
        scroll = VGroup(SurroundingRectangle(steps, buff=0.2, color=MUTED, stroke_width=2), steps).move_to(RIGHT * 3.5 + UP * 0.5)
        cert = label("a certificate, once the graph is given", 26, MUTED, italic=True).next_to(scroll, DOWN, buff=0.3)
        self.play_at(W("solvers"), FadeIn(scroll), FadeIn(cert), run_time=0.9)
        need = maths(r"\text{but first: find } G \text{ with } \chi(G) \ge 6", 32, INK).next_to(cert, DOWN, buff=0.5)
        self.play_at(W("someone"), Write(need), run_time=1.4)

        # cue 5: the lower bound stayed at five
        bl = BoundsLine(5, 7, y=-2.9)
        self.play_at(W("from"), FadeOut(VGroup(divider, lt, rt, tiles, one, scroll, cert, need)), FadeIn(bl), run_time=0.9)
        year = ValueTracker(2018)
        yr = always_redraw(lambda: Integer(int(year.get_value()), group_with_commas=False, font_size=48, color=INK).move_to(UP * 0.6))
        self.add(yr)
        self.play(year.animate.set_value(2026), run_time=self.left(W("five", after=53)), rate_func=linear)
        self.play(Indicate(bl.bracket[1][0], color=INK, scale_factor=1.3), run_time=0.8)
        self.finish()


class S4_2(NarratedScene):
    """Colourings you can't draw: the circle toy problem (ours; its mechanism reappears in the paper's Lemma 6.4)."""
    scene_id = "s4_2"

    def construct(self):
        W = self.word
        anyf = maths(r"c : \mathbb{R}^2 \to \{1, \dots, k\} \quad \text{\emph{any} function}", 44, INK)
        self.play_at(W("any", 1) - 1.0, Write(anyf), run_time=1.4)

        # cue 2: drawn colourings have areas; most colourings can't be drawn
        hx, _ = hex_tiling(0.28, 3, extent=(1.9, 1.3))
        st = stripes(0.35, extent=(2.2, 0.6), colours=(ORANGE, SKY))
        blobs = VGroup(*[region(Circle(radius=r), c, opacity=0.4).shift(v) for r, c, v in
                         ((0.7, ORANGE, LEFT * 0.4), (0.6, SKY, RIGHT * 0.45 + UP * 0.2), (0.5, GREEN, DOWN * 0.45 + RIGHT * 0.1))])
        frames = VGroup()
        for m in (hx, st, blobs):
            box = Rectangle(width=2.6, height=2.0, stroke_color=MUTED, stroke_width=1.5)
            frames.add(VGroup(m.move_to(box), box))
        for f in frames[:2]:
            f[0].set_clip_path = None
        frames.arrange(RIGHT, buff=0.6).move_to(UP * 0.2)
        self.play_at(W("every", 1), anyf.animate.scale(0.7).to_edge(UP, buff=0.5),
                     LaggedStart(*[FadeIn(f) for f in frames], lag_ratio=0.3), run_time=1.6)
        areas = VGroup(*[maths(r"\text{area of each colour}", 24, MUTED).next_to(f, DOWN, buff=0.25) for f in frames])
        self.play_at(W("measure"), FadeIn(areas), run_time=0.8)
        wild = WildPlane(cell=0.04, seed=9, dim=0.55)
        wild.image.stretch_to_fit_width(2.6).stretch_to_fit_height(2.0)
        wild_box = Group(wild.image, Rectangle(width=2.6, height=2.0, stroke_color=MUTED, stroke_width=1.5))
        wild_box.scale(0.8).move_to(DOWN * 1.75)
        cant = label("most colourings look like nothing we can draw", 26, MUTED, italic=True).next_to(wild_box, DOWN, buff=0.25)
        self.play_at(W("most"), FadeOut(areas), frames.animate.shift(UP * 0.4), FadeIn(wild_box), FadeIn(cant), run_time=1.0)

        # cue 3: the toy problem
        toy = label("a toy problem", 30, MUTED, italic=True).to_corner(UL, buff=0.5)
        C = LEFT * 2.6 + DOWN * 0.3
        Rc = 2.4
        circle = Circle(radius=Rc, stroke_color=EDGE, stroke_width=2.5).move_to(C)
        self.play_at(W("toy"), FadeOut(Group(frames, wild_box, cant, anyf)), FadeIn(toy), run_time=0.8)
        self.play_at(W("circle", 1), Create(circle), run_time=1.0)
        th0 = PI / 2
        pt = lambda th: C + Rc * np.array([np.cos(th), np.sin(th), 0])
        arc = Arc(radius=Rc + 0.3, start_angle=th0, angle=ALPHA * TAU, arc_center=C, stroke_color=INK, stroke_width=4)
        a_lab = maths(r"\alpha", 40, INK).move_to(C + (Rc + 0.7) * np.array([np.cos(th0 + ALPHA * PI), np.sin(th0 + ALPHA * PI), 0]))
        self.play_at(W("angle"), Create(arc), Write(a_lab), run_time=0.9)
        a_val = maths(r"\alpha = \tfrac{\sqrt{2}}{10}\ \text{of a turn}\ \ (\text{irrational})", 36, INK).move_to(RIGHT * 3.2 + UP * 1.6)
        self.play_at(W("root"), Write(a_val), run_time=1.2)
        rule = maths(r"c(\theta) \neq c(\theta + \alpha)", 44, INK).next_to(a_val, DOWN, buff=0.6)
        self.play_at(W("any", 3), Write(rule), run_time=1.2)

        # cue 4: hop around the circle, alternating
        q2 = maths(r"\text{2 colours?}", 36, INK).next_to(rule, DOWN, buff=0.6)
        self.play_at(W("can"), FadeIn(q2), FadeOut(arc), FadeOut(a_lab), run_time=0.6)
        hops = VGroup()
        dots = VGroup()
        N = 260
        for n in range(N):
            th = th0 + n * ALPHA * TAU
            dots.add(Dot(pt(th), radius=0.075 if n < 4 else 0.05, color=PAL[ORANGE if n % 2 == 0 else SKY]))
            if n < 6:
                hops.add(ArcBetweenPoints(pt(th), pt(th + ALPHA * TAU), angle=-0.6, stroke_color=MUTED, stroke_width=1.8))
        self.play_at(W("start"), FadeIn(dots[0], scale=2), run_time=0.5)
        for n, w in ((1, W("next", 1)), (2, W("next", 2)), (3, W("so", after=49))):
            self.play_at(w - 0.3, Create(hops[n - 1]), FadeIn(dots[n], scale=2), run_time=0.5)
        self.play_at(W("because"), LaggedStart(*[FadeIn(d) for d in dots[4:]], lag_ratio=0.02), FadeOut(hops[:3]),
                     run_time=self.cue_end(4) - W("because"))

        # cue 5: every chain, via the axiom of choice: two colours work (arbitrary)
        chains = VGroup()
        rng = np.random.default_rng(3)
        for s in range(3):
            base = rng.uniform(0, TAU)
            for n in range(140):
                th = base + n * ALPHA * TAU
                chains.add(Dot(pt(th), radius=0.04, color=PAL[ORANGE if n % 2 == 0 else SKY]))
        self.play_at(W("chain", 1), LaggedStart(*[FadeIn(d) for d in chains], lag_ratio=0.002), run_time=2.0)
        choice = label("the axiom of choice picks a start in every chain", 26, MUTED, italic=True).next_to(q2, DOWN, buff=0.4)
        self.play_at(W("axiom"), FadeIn(choice), run_time=0.7)
        yes = maths(r"\text{arbitrary: 2 colours suffice}", 36, INK).move_to(q2)
        self.play_at(W("yes"), FadeOut(q2), FadeIn(yes), run_time=0.7)

        # cue 6: alternating means invariant under rotation by 2 alpha
        speck = VGroup(dots, chains)
        self.play_at(W("draw", 1), FadeOut(VGroup(choice, a_val)), rule.animate.next_to(yes, UP, buff=0.5), run_time=0.8)
        two = maths(r"c(\theta + 2\alpha) = c(\theta)", 44, INK).next_to(yes, DOWN, buff=0.6)
        self.play_at(W("twice", 2), Write(two), run_time=1.2)
        self.play_at(W("rotate"), Rotate(speck, angle=2 * ALPHA * TAU, about_point=C), run_time=1.8)
        irr = label("2α is an irrational rotation too", 26, MUTED, italic=True).next_to(two, DOWN, buff=0.3)
        self.play_at(W("irrational", 3), FadeIn(irr), run_time=0.6)

        # cue 7: a colouring with honest areas, invariant under an irrational rotation, is constant
        self.play_at(self.cue(7), FadeOut(speck), FadeOut(irr), run_time=0.6)
        cols = [ORANGE, SKY, ORANGE, SKY, SKY, ORANGE]
        cuts = [0, 0.7, 1.9, 2.6, 3.7, 4.9, TAU]
        ring = VGroup(*[AnnularSector(inner_radius=Rc - 0.18, outer_radius=Rc + 0.18, start_angle=cuts[i], angle=cuts[i + 1] - cuts[i],
                                      fill_color=PAL[cols[i]], fill_opacity=0.85, stroke_width=0).shift(C) for i in range(6)])
        honest = label("honest arcs", 26, MUTED, italic=True).next_to(circle, DOWN, buff=0.3)
        self.play_at(W("honest"), FadeIn(ring), FadeIn(honest), run_time=0.8)
        blur = VGroup(*[ring.copy().rotate(k * 2 * ALPHA * TAU, about_point=C).set_opacity(0.18) for k in range(1, 12)])
        self.play_at(W("unchanged", 2), LaggedStart(*[FadeIn(b) for b in blur], lag_ratio=0.15), run_time=2.2)
        mix = AnnularSector(inner_radius=Rc - 0.18, outer_radius=Rc + 0.18, angle=TAU, fill_color=interpolate_color(PAL[ORANGE], PAL[SKY], 0.5),
                            fill_opacity=0.85, stroke_width=0).shift(C)
        const = maths(r"\Rightarrow\ c \text{ constant (almost everywhere)}", 30, INK).next_to(two, DOWN, buff=0.4)
        self.play_at(W("single"), FadeOut(VGroup(ring, blur)), FadeIn(mix), Write(const), run_time=1.2)
        self.play_at(W("contradicts"), Indicate(rule, color=HOT, scale_factor=1.15), run_time=1.0)

        # cue 8: verdict
        self.play_at(self.cue(8), FadeOut(VGroup(mix, circle, honest, rule, two, const, yes, toy)), run_time=0.7)
        lcol = VGroup(label("arbitrary colourings", 34, INK), maths(r"2 \text{ colours suffice}", 38, INK)).arrange(DOWN, buff=0.35)
        rcol = VGroup(label("measurable colourings", 34, INK), maths(r"\text{impossible}", 38, HOT)).arrange(DOWN, buff=0.35)
        cols2 = VGroup(lcol, rcol).arrange(RIGHT, buff=2.5).move_to(UP * 0.8)
        self.play_at(W("two", after=97), FadeIn(lcol), run_time=0.8)
        self.play_at(W("no", after=101), FadeIn(rcol), run_time=0.8)

        # cue 9: measurable = has a well-defined area; the gap
        defn = maths(r"\text{measurable set} = \text{a set with a well-defined area}", 36, INK).to_edge(DOWN, buff=1.4)
        self.play_at(W("measurable", 1), Write(defn), run_time=1.4)
        gap = DoubleArrow(lcol.get_right(), rcol.get_left(), buff=0.3, color=MUTED, stroke_width=2.5)
        gl = label("the gap", 28, MUTED, italic=True).next_to(gap, UP, buff=0.15)
        self.play_at(W("gap", 2), GrowFromCenter(gap), FadeIn(gl), run_time=0.8)
        icon = Circle(radius=0.35, stroke_color=EDGE, stroke_width=2).to_corner(DR, buff=0.5)
        self.play_at(W("keep"), FadeOut(VGroup(cols2, gap, gl, defn)), FadeIn(icon), run_time=1.0)
        self.finish()


class S4_3(NarratedScene):
    scene_id = "s4_3"

    def construct(self):
        W = self.word
        top = label("any colouring", 30, INK).to_edge(UP, buff=0.6)
        bl = BoundsLine(5, 7, y=1.7)
        self.play_at(self.cue(1), FadeIn(top), FadeIn(bl), run_time=0.8)
        rows = VGroup(
            maths(r"\text{measurable colourings:}\ \ \chi_m(\mathbb{R}^2) \ge 5 \quad \text{(Falconer, 1981)}", 32, INK),
            maths(r"\text{map-type colourings:}\ \ \ge 6 \quad \text{(Townsend)}", 32, INK),
            maths(r"\text{polygonal colourings:}\ \ \ge 7 \quad \text{(Sokolov \& Voronov, 2025)}", 32, INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(DOWN * 1.2)
        nice = label("nicely behaved colourings", 28, MUTED, italic=True).next_to(rows, UP, buff=0.45).align_to(rows, LEFT)
        self.play_at(W("measurable", 1), FadeIn(nice), run_time=0.6)
        self.play_at(W("1981"), Write(rows[0]), run_time=1.4)
        y2018 = bl.chip("de Grey, 2018", 5)
        arr = CurvedArrow(rows[0].get_top() + RIGHT * 2.5, y2018.get_bottom() + DOWN * 0.1, angle=-0.5, color=MUTED, stroke_width=2)
        yrs = label("37 years earlier", 24, MUTED, italic=True).next_to(arr, RIGHT, buff=0.1)
        self.play_at(W("37"), FadeIn(y2018), Create(arr), FadeIn(yrs), run_time=1.0)
        self.play_at(W("map"), FadeOut(VGroup(arr, yrs)), Write(rows[1]), run_time=1.3)
        self.play_at(W("2025"), Write(rows[2]), run_time=1.6)
        # cue 4
        self.play_at(W("none"), Indicate(VGroup(top, bl), color=INK, scale_factor=1.04), rows.animate.set_opacity(0.45),
                     run_time=1.2)
        # cue 5: Payne's cautionary example
        self.play_at(self.cue(5), FadeOut(VGroup(rows, nice, y2018)), run_time=0.7)
        payne = label("Payne, 2009", 30, MUTED).move_to(UP * 0.2)
        self.play_at(W("payne"), FadeIn(payne), run_time=0.6)
        rng = np.random.default_rng(6)
        pts = [np.array([rng.uniform(-5.5, 5.5), rng.uniform(-3.3, -0.7), 0]) for _ in range(28)]
        sparse = VGroup(*[Line(p, p + 0.9 * np.array([np.cos(a), np.sin(a), 0]), stroke_color=EDGE, stroke_width=1.5, stroke_opacity=0.6)
                          for p in pts for a in rng.uniform(0, TAU, 2)])
        sdots = VGroup(*[Dot(p, radius=0.05, color=INK) for p in pts])
        self.play_at(W("join"), FadeIn(sparse), FadeIn(sdots), run_time=1.0)
        f2 = backed(maths(r"\text{anything goes: } 2 \text{ colours}", 36, INK)).move_to(LEFT * 3.3 + DOWN * 2.0)
        f5 = backed(maths(r"\text{measurable: at least } 5", 36, INK)).move_to(RIGHT * 3.3 + DOWN * 2.0)
        self.play_at(W("two"), Write(f2), run_time=1.0)
        self.play_at(W("needs"), Write(f5), run_time=1.0)
        self.play_at(W("similar"), Indicate(VGroup(f2, f5), color=INK, scale_factor=1.06), run_time=1.0)
        self.finish()


class S4_4(NarratedScene):
    scene_id = "s4_4"

    def construct(self):
        W = self.word
        base = DOWN * 3.4
        fork = DOWN * 0.8
        trunk = Line(base, fork, stroke_color=EDGE, stroke_width=6)
        r1 = CubicBezier(fork, fork + UP * 1.2, LEFT * 3 + UP * 1.4, LEFT * 5.2 + UP * 2.8).set_stroke(EDGE, 6)
        r2 = CubicBezier(fork, fork + UP * 1.2, RIGHT * 3 + UP * 1.4, RIGHT * 5.2 + UP * 2.8).set_stroke(EDGE, 6)
        self.play_at(W("roads"), Create(trunk), run_time=0.7)
        l1 = label("find a much bigger finite graph,\\\\ and certify it", 30, INK).move_to(LEFT * 4.1 + UP * 0.6)
        l2 = label("tame arbitrary colourings,\\\\ then use measurable tools", 30, INK).move_to(RIGHT * 4.1 + UP * 0.6)
        self.play_at(W("find", 1), Create(r1), FadeIn(l1), run_time=1.0)
        self.play_at(W("tame"), Create(r2), FadeIn(l2), run_time=1.0)
        self.play_at(W("second"), r1.animate.set_stroke(opacity=0.2), l1.animate.set_opacity(0.3),
                     r2.animate.set_stroke(colour(ORANGE)), run_time=1.0)
        self.finish()
