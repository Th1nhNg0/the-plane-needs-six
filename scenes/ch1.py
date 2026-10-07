"""Chapter 1 · The colouring game.   manim -qh scenes/ch1.py S1_1 S1_2 S1_3 S1_4"""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.style import (BG, INK, MUTED, HOT, HOT_RING, region, backed, ORANGE, SKY, GREEN, colour, glyph, label, maths, panel, tag,
                              marker, stick)
from components.graph import clash, UnitGraph, DistanceIndicator
from components.widgets import (WildPlane, unit_stick, stick_ends, hex_tiling, stripes, status)
from components.narrated import NarratedScene

S = 2.0   # manim units per world unit


def rule_card():
    return backed(maths(r"|xy| = 1 \;\Rightarrow\; c(x) \neq c(y)", 26, MUTED)).to_corner(DL, buff=0.5)


class S1_1(NarratedScene):
    scene_id = "s1_1"

    def construct(self):
        W = self.word
        L = 5.0                                   # close-up: 1 world unit = 5 manim units
        a = LEFT * L / 2 + DOWN * 0.3
        bpt = ValueTracker(1.0)                   # world distance of the right pin
        pin_a = marker(None, 0.42).move_to(a)
        pin_b = marker(None, 0.42).move_to(a + RIGHT * L)
        rod = always_redraw(lambda: stick(pin_a.get_center(), pin_b.get_center(), 6))
        pin_b.add_updater(lambda m: m.move_to(a + RIGHT * L * bpt.get_value()))
        ind = DistanceIndicator(lambda: pin_a.get_center(), lambda: pin_b.get_center(), per_unit=L, offset=0.6, side=1,
                                font_size=40)
        self.play_at(self.cue(1), Create(rod), GrowFromCenter(pin_a), GrowFromCenter(pin_b), run_time=1.0)
        self.add(rod, pin_a, pin_b)
        self.play_at(W("about", 1), FadeIn(ind), run_time=0.8)

        # cue 2: exactly one apart -> different colours
        card = rule_card()
        self.play_at(W("different", 1), Transform(pin_a, marker(ORANGE, 0.42).move_to(pin_a)),
                     Transform(pin_b, marker(SKY, 0.42).move_to(pin_b)), FadeIn(card), run_time=0.6)
        pin_b.clear_updaters()
        pin_b.add_updater(lambda m: m.move_to(a + RIGHT * L * bpt.get_value()))

        # cue 3: 0.999 ok, 1.001 ok, exactly 1 forbidden
        ok = lambda: label("allowed", 32, MUTED, italic=True).next_to(VGroup(pin_a, pin_b), DOWN, buff=0.6)
        self.play_at(W("distance", 1) - 0.3, bpt.animate.set_value(0.999),
                     Transform(pin_b, marker(ORANGE, 0.42).move_to(a + RIGHT * L * 0.999)), run_time=0.8)
        t1 = ok()
        self.play_at(W("allowed", 1), FadeIn(t1), run_time=0.5)
        self.play_at(W("1", 1) - 0.4, bpt.animate.set_value(1.001), FadeOut(t1), run_time=0.8)
        t2 = ok()
        self.play_at(W("fine"), FadeIn(t2), run_time=0.5)
        self.play_at(W("only", 2), bpt.animate.set_value(1.0), FadeOut(t2), run_time=0.8)
        a_, z, ring = clash(pin_a.get_center(), pin_b.get_center(), run_time=1.0)
        no = label("forbidden", 32, HOT, italic=True).next_to(VGroup(pin_a, pin_b), DOWN, buff=0.6)
        self.play_at(W("forbidden"), a_, FadeIn(no), run_time=1.0)

        # cue 4: every point simply gets a colour
        pin_b.clear_updaters()
        rng = np.random.default_rng(2)
        xs, ys = np.arange(-6.75, 6.8, 0.5), np.arange(-2.75, 3.3, 0.5)
        dots = VGroup(*[Dot([x, y, 0], radius=0.07) for x in xs for y in ys])

        def recolour():
            return [d.animate.set_color(colour([ORANGE, SKY, GREEN][rng.integers(3)])) for d in dots]

        for d in dots:
            d.set_color(colour([ORANGE, SKY, GREEN][rng.integers(3)]))
        self.play_at(self.cue(4), FadeOut(VGroup(rod, pin_a, pin_b, ind, z, ring, no)), FadeIn(dots, lag_ratio=0.002),
                     run_time=1.2)
        self.play_at(W("every", 1), *recolour(), run_time=0.4)
        self.play_at(W("every", 2), *recolour(), run_time=0.4)
        tiles = VGroup(hex_tiling(0.35, 3, extent=(1.8, 1.6))[0], label("✗", 40, HOT_RING, weight="BOLD"))
        tiles[1].move_to(tiles[0])
        blobs = VGroup(*[Circle(radius=r).set_fill(colour(c), 0.9).set_stroke(width=0).shift(v)
                         for r, c, v in ((0.5, ORANGE, LEFT * 0.3), (0.45, SKY, RIGHT * 0.35 + UP * 0.2),
                                         (0.4, GREEN, DOWN * 0.35 + RIGHT * 0.2))])
        blobs = VGroup(blobs, label("✗", 40, HOT_RING, weight="BOLD").move_to(blobs))
        not_this = VGroup(backed(VGroup(tiles, label("not tiles", 22, MUTED)).arrange(DOWN, buff=0.15), 0.95, 0.25),
                          backed(VGroup(blobs, label("not regions", 22, MUTED)).arrange(DOWN, buff=0.15), 0.95, 0.25)
                          ).arrange(RIGHT, buff=0.5).to_corner(UR, buff=0.5)
        self.play_at(W("tiles"), FadeIn(not_this[0], shift=DOWN * 0.2), run_time=0.6)
        self.play_at(W("regions"), FadeIn(not_this[1], shift=DOWN * 0.2), run_time=0.6)
        self.play_at(W("each", 1), *recolour(), run_time=0.4)
        self.play_at(W("simply"), *recolour(), run_time=0.4)
        self.play_at(W("that's", after=36), *recolour(), run_time=0.4)
        self.finish()


class S1_2(NarratedScene):
    scene_id = "s1_2"

    def construct(self):
        W = self.word
        head = backed(label("Two colours?", 40, INK)).to_edge(UP, buff=0.5)
        card = rule_card()
        self.add(card)
        self.play_at(self.cue(1) + 1.8, FadeIn(head, shift=DOWN * 0.15), run_time=0.7)

        # cue 2: stripes narrower than one
        st = stripes(0.8 * S, colours=(ORANGE, SKY)).set_z_index(-50)
        width_note = backed(maths(r"\text{width} = 0.8 < 1", 30, INK)).to_edge(DOWN, buff=1.3)
        self.play_at(W("stripes", 1), FadeIn(st), run_time=1.0)
        self.bring_to_front(head, card)
        self.play_at(W("narrower"), FadeIn(width_note), run_time=0.6)
        x0 = 0.8 * S * 0.5                         # boundary between stripe 0 and stripe 1
        s1 = unit_stick([x0 - 0.5 * S, 0.3, 0], 0, S, ORANGE, SKY)
        self.play_at(W("drop"), FadeIn(s1, shift=DOWN * 0.5), FadeOut(width_note), run_time=0.7)
        ok = VGroup()
        self.play_at(W("different", 1), FadeIn(ok), run_time=0.4)

        # cue 3: tilt -> same stripe; or two stripes apart -> same colour
        s2 = unit_stick([-0.3 * S, -0.48 * S + 0.3, 0], np.arccos(0.6), S, ORANGE, ORANGE)   # horizontal span 0.6
        self.play_at(W("tilt"), Transform(s1, s2), FadeOut(ok), run_time=0.9)
        a, z, ring = clash(*stick_ends(s1), run_time=0.8)
        self.play_at(W("same", 1), a)
        self.remove(z, ring)
        s3 = unit_stick([0.35 * S, 0.3, 0], 0, S, ORANGE, ORANGE)  # world x 0.35 -> 1.35: stripes 0 and 2 (both orange)
        self.play_at(W("two", 2), Transform(s1, s3), run_time=0.8)
        a, z, ring = clash(*stick_ends(s1), run_time=0.8)
        self.play_at(W("colour", 1), a)
        self.remove(z, ring)

        # cue 4: checkerboard and rings fail the same way
        cb = VGroup(*[region(Square(0.7 * S), ORANGE if (i + j) % 2 else SKY)
                      .move_to([(i + 0.5) * 0.7 * S, (j + 0.5) * 0.7 * S, 0]) for i in range(-7, 7) for j in range(-4, 4)]
                    ).set_z_index(-50)
        sc = unit_stick([0.1 * S, 0.1 * S, 0], PI / 4, S, SKY, SKY)   # world (0.1,0.1)->(0.81,0.81): cells (0,0),(1,1), both sky
        self.play_at(W("checkerboards"), FadeOut(st), FadeIn(cb), Transform(s1, sc), run_time=0.8)
        a, z, ring = clash(*stick_ends(s1), run_time=0.7)
        self.play(a)
        self.remove(z, ring)
        rings = VGroup(*[region(Annulus(inner_radius=k * 0.6 * S, outer_radius=(k + 1) * 0.6 * S), ORANGE if k % 2 else SKY)
                         for k in range(10)]).set_z_index(-50)
        # chord from radius 0.3 to radius 1.3 along a line: both in even rings (0 and 2) -> sky/sky
        sr = unit_stick([0.3 * S, 0, 0], 0, S, SKY, SKY)
        self.play_at(W("rings"), FadeOut(cb), FadeIn(rings), Transform(s1, sr), run_time=0.8)
        a, z, ring = clash(*stick_ends(s1), run_time=0.7)
        self.play(a)
        self.remove(z, ring)

        # cue 5: pause and try
        tryit = label("Pause, and try to find a 2-colouring.", 32, MUTED, italic=True)
        self.play_at(W("worth"), FadeOut(rings), FadeOut(s1), FadeIn(tryit), run_time=0.8)

        # cue 6: three points at mutual distance one
        tri = {"a": (-0.5, -0.29), "b": (0.5, -0.29), "c": (0, np.sqrt(3) / 2 - 0.29)}
        g = UnitGraph(tri, scale=S * 1.3, origin=DOWN * 0.3)
        self.play_at(W("three", 1), FadeOut(tryit), FadeIn(g.markers, lag_ratio=0.3), FadeOut(head), run_time=0.9)
        self.play_at(W("exactly"), LaggedStart(*[Create(s) for s in g.sticks], lag_ratio=0.3), run_time=1.2)
        side = label("equilateral · side 1", 26, MUTED).next_to(g, DOWN, buff=0.45)
        self.play_at(W("equilateral"), FadeIn(side), run_time=0.6)

        # cue 7: colour the corners
        self.play_at(W("pair"), g.colour_anim("a", ORANGE, 0.4))
        self.play_at(W("needs"), g.colour_anim("b", SKY, 0.4))
        for c, nb, t in ((ORANGE, "a", W("three", 3) - 1.6), (SKY, "b", W("three", 3) - 0.8)):
            self.until(t)
            self.play(g.colour_anim("c", c, 0.2))
            a, z, ring = clash(g.pos("c"), g.pos(nb), run_time=0.45)
            self.play(a)
            self.remove(z, ring)
        self.play_at(W("three", 3), g.colour_anim("c", GREEN, 0.4))

        # cue 8: two can never be enough
        verdict = maths(r"\text{triangle} \;\Rightarrow\; \text{at least 3 colours}", 34, INK).to_edge(UP, buff=0.6)
        self.play_at(W("never"), FadeIn(verdict, shift=DOWN * 0.15), run_time=0.7)
        self.play_at(W("just"), Indicate(g, color=INK, scale_factor=1.08), run_time=1.0)
        self.finish()


class S1_3(NarratedScene):
    scene_id = "s1_3"

    def construct(self):
        W = self.word
        card = rule_card()
        self.add(card)
        tri = {"a": (-0.5, 0), "b": (0.5, 0), "c": (0, np.sqrt(3) / 2)}
        g = UnitGraph(tri, scale=0.8, origin=np.array([5.4, 2.2, 0]), marker_size=0.26, stick_width=3)
        for k, c in zip("abc", (ORANGE, SKY, GREEN)):
            g.set_colour(k, c)
        head = backed(label("Three colours?", 40, INK)).to_edge(UP, buff=0.5)
        self.play_at(self.cue(1), FadeIn(g), FadeIn(head), run_time=0.8)
        for k, w in zip("abc", ("orange", "blue", "green")):
            self.play_at(W(w), Indicate(g.mk[k], color=INK, scale_factor=1.5), run_time=0.6)

        # cue 2: hexagons, 3-coloured, neighbours differ
        R = 0.4
        tiling, cells = hex_tiling(R * S, 3, opacity=0.8)
        tiling.set_z_index(-50)
        self.play_at(W("hexagons", 1), FadeIn(tiling, lag_ratio=0.002), run_time=1.2)
        self.bring_to_front(head, card, g)
        c0 = min(cells, key=lambda c: np.linalg.norm(c[0]))
        nbrs = [c for c in cells if abs(np.linalg.norm(c[0] - c0[0]) - np.sqrt(3) * R * S) < 1e-6]
        hl = VGroup(*[RegularPolygon(6, radius=R * S, start_angle=PI / 2).set_stroke(INK, 4).set_fill(opacity=0)
                      .move_to(c[0]) for c in [c0] + nbrs])
        self.play_at(W("differ"), Create(hl), run_time=0.8)

        # cue 3: inside one hexagon nothing is a unit apart; across an edge colours differ
        diam = Line(c0[0] + UP * R * S, c0[0] + DOWN * R * S, stroke_color=INK, stroke_width=4)
        dlab = backed(maths(r"\text{widest} = 0.8 < 1", 30, INK)).next_to(c0[0], RIGHT, buff=1.2)
        self.play_at(W("small"), FadeOut(hl), Create(diam), FadeIn(dlab), run_time=0.8)
        self.play_at(W("safe", 1) - 0.3, Indicate(dlab, color=INK), run_time=0.6)
        n0 = nbrs[0]
        mid = (c0[0] + n0[0]) / 2
        d = (n0[0] - c0[0]) / np.linalg.norm(n0[0] - c0[0])
        p = mid - d * 0.5 * S
        ang = np.arctan2(d[1], d[0])
        s1 = unit_stick(p, ang, S, c0[1], n0[1])
        self.play_at(W("neighbouring", 2), FadeOut(diam), FadeOut(dlab), FadeIn(s1), run_time=0.7)
        okm = VGroup()
        self.play_at(W("safe", 2), FadeIn(okm), run_time=0.4)

        # cue 4: same-colour hexagons one hexagon apart; the stick reaches across
        same = [c for c in cells if c[1] == c0[1] and abs(np.linalg.norm(c[0] - c0[0]) - 3 * R * S) < 1e-6]
        b = same[0]
        hb = VGroup(*[RegularPolygon(6, radius=R * S, start_angle=PI / 2).set_stroke(INK, 5).set_fill(opacity=0).move_to(c[0])
                      for c in (c0, b)])
        self.play_at(W("same", 1), FadeOut(okm), Create(hb), run_time=0.8)
        u = (b[0] - c0[0]) / np.linalg.norm(b[0] - c0[0])
        start = c0[0] + u * 0.1 * S
        target = np.arctan2(u[1], u[0])
        piv = ValueTracker(target + 1.2)
        rot = always_redraw(lambda: unit_stick(start, piv.get_value(), S))
        self.play_at(W("stick", 2), FadeOut(s1), FadeIn(rot), run_time=0.5)
        self.play(piv.animate.set_value(target), run_time=self.left(W("other") - 0.2))
        self.remove(rot)
        s_bad = unit_stick(start, target, S, c0[1], b[1])
        self.add(s_bad)
        a, z, ring = clash(*stick_ends(s_bad), run_time=0.8)
        self.play_at(W("other"), a)

        # cue 5: bigger hexagons -> the stick fits inside one
        self.play_at(W("bigger"), FadeOut(VGroup(s_bad, z, ring, hb)), tiling.animate.scale(1.5, about_point=c0[0]),
                     run_time=1.0)
        s_in = unit_stick(c0[0] + LEFT * 0.5 * S + UP * 0.05, 0, S, c0[1], c0[1])
        self.play_at(W("fits"), FadeIn(s_in), run_time=0.5)
        a, z, ring = clash(*stick_ends(s_in), run_time=0.8)
        self.play_at(W("single"), a)

        # cue 6: no comfortable size
        bar = Line(LEFT * 2.5, RIGHT * 2.5, stroke_color=INK, stroke_width=3)
        ends = VGroup(label("small hexagons ✗", 22, HOT_RING).next_to(bar, LEFT, buff=0.25),
                      label("✗ large hexagons", 22, HOT_RING).next_to(bar, RIGHT, buff=0.25))
        slider = backed(VGroup(ends[0], bar, ends[1])).to_edge(DOWN, buff=1.3)
        self.play_at(W("comfortable"), FadeIn(slider), run_time=0.7)

        # cue 7-8: not a proof; invitation
        qm = label("3 colours: undecided, so far", 40, INK)
        self.play_at(W("that's", after=49), FadeOut(VGroup(tiling, s_in, z, ring, slider, g)), FadeIn(qm), run_time=0.9)
        inv = label("Pause, and try to break three colours, or rescue them.", 28, MUTED, italic=True).next_to(qm, DOWN, buff=0.5)
        self.play_at(W("pause"), FadeIn(inv, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S1_4(NarratedScene):
    scene_id = "s1_4"

    def construct(self):
        W = self.word
        planes = [WildPlane(cell=c, seed=s, dim=0.38) for s, c in ((11, 0.25), (12, 0.12), (13, 0.4), (14, 0.18),
                                                                    (15, 0.3), (16, 0.15))]
        cur = planes[0].image
        self.play_at(self.cue(1), FadeIn(cur), run_time=0.5)
        times = np.linspace(self.cue(1) + 1.0, self.cue_end(1), len(planes))
        for t, pl in zip(times[1:], planes[1:]):
            self.until(t)
            self.remove(cur)
            cur = pl.image
            self.add(cur)
        st = unit_stick(LEFT * S / 2, 0, S)
        self.play_at(self.cue(2), FadeIn(st), run_time=0.6)
        self.play_at(W("past"), FadeOut(cur), run_time=1.4)
        self.play_at(W("stick"), Indicate(st, color=INK, scale_factor=1.3), run_time=1.0)
        self.finish()
