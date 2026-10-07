"""Chapter 0 · Cold open.   manim -qh scenes/ch0.py S0_1"""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.style import BG, INK, MUTED, HOT_RING, ORANGE, SKY, GREEN, label, maths, panel, marker
from components.graph import clash
from components.widgets import BoundsLine, WildPlane, unit_stick, stick_ends, paper_card
from components.narrated import NarratedScene

S = 1.6  # manim units per world unit


def find_drop(plane, rng, same, tries=4000, box=(5.5, 3.0)):
    """Random stick placement whose two pins have equal (same=True) or different colours on the plane."""
    for _ in range(tries):
        p = np.array([rng.uniform(-box[0], box[0]), rng.uniform(-box[1], box[1]), 0])
        a = rng.uniform(0, TAU)
        q = p + S * np.array([np.cos(a), np.sin(a), 0])
        if abs(q[0]) > 6.6 or abs(q[1]) > 3.6:
            continue
        if (plane.colour_at(p) == plane.colour_at(q)) == same:
            return p, a
    raise RuntimeError("no placement found")


class S0_1(NarratedScene):
    scene_id = "s0_1"

    def construct(self):
        W = self.word
        rng = np.random.default_rng(7)

        # cue 1-2: a single stick drifts in and lands; "one unit"
        st = unit_stick(ORIGIN + LEFT * S / 2, 0, S)
        st.shift(UP * 4.6).rotate(-0.9)
        self.play_at(self.cue(1), st.animate(rate_func=rate_functions.ease_out_cubic).move_to(ORIGIN).rotate(0.9),
                     run_time=1.8)
        one = label("1", 30, INK).next_to(st, UP, buff=0.25)
        self.play_at(W("one", 1), FadeIn(one, shift=DOWN * 0.1), run_time=0.5)

        # "drop it anywhere on a flat plane": the plane floods in as a wild 3-colouring
        plane = WildPlane(cell=0.2, seed=3, dim=0.38)
        self.play_at(W("plane", 1), FadeIn(plane.image), FadeOut(one), run_time=1.2)
        self.bring_to_front(st)

        def drop(same, rt=0.6):
            p, a = find_drop(plane, rng, same)
            c1, c2 = plane.colour_at(p), plane.colour_at(p + S * np.array([np.cos(a), np.sin(a), 0]))
            new = unit_stick(p, a, S, c1, c2)
            return new

        # "Wherever it lands, its two ends must sit on different colours"
        for t in (W("wherever"), W("lands"), W("ends")):
            new = drop(False)
            self.play_at(t, Transform(st, new), run_time=0.55)
        self.play_at(W("different", 1), Indicate(VGroup(st[1], st[2]), color=INK, scale_factor=1.4), run_time=0.8)

        # cue 3: "no matter where the stick falls" — one falls on a same-colour pair: clash
        for t in (W("never"), W("matter")):
            self.play_at(t, Transform(st, drop(False)), run_time=0.5)
        bad = drop(True)
        self.play_at(W("falls"), Transform(st, bad), run_time=0.5)
        a, z, ring = clash(*stick_ends(st), run_time=0.9)
        self.play(a)
        self.remove(z, ring)

        # cue 4: many sticks rain down; some clash; big question mark
        rain = VGroup()
        sparks = []
        for i in range(24):
            same = i % 6 == 0
            p, ang = find_drop(plane, rng, same)
            s = unit_stick(p, ang, S, plane.colour_at(p), plane.colour_at(p + S * np.array([np.cos(ang), np.sin(ang), 0])),
                           size=0.24, width=4)
            rain.add(s)
            if same:
                sparks.append(s)
        self.play_at(self.cue(4) - 0.4, LaggedStart(*[FadeIn(s, shift=DOWN * 0.6) for s in rain], lag_ratio=0.03),
                     FadeOut(st), run_time=1.4)
        anims, residue = [], []
        for s in sparks:
            a, z, ring = clash(*stick_ends(s), run_time=0.7)
            anims.append(a)
            residue += [z, ring]
        q = label("?", 140, INK, weight="BOLD")
        q_bg = panel(q, pad=0.3)
        self.play(*anims, FadeIn(q_bg, scale=0.8), run_time=0.9)
        self.remove(*residue)

        # cue 5: history on the bounds line
        bl = BoundsLine(4, 7, y=-2.6)
        bl.bracket.set_opacity(0)
        self.play_at(self.cue(5), FadeOut(rain), FadeOut(q_bg), plane.image.animate.set_opacity(0.18),
                     FadeIn(bl.axis), FadeIn(bl.chi), run_time=1.0)
        self.add(bl)
        b47 = bl.set_bounds(4, 7)
        y1950 = bl.chip("1950", 5.5)
        self.play_at(W("between"), Transform(bl.bracket, b47), FadeIn(y1950), run_time=1.0)
        b57 = bl.set_bounds(5, 7)
        y2018 = bl.chip("2018", 6)
        self.play_at(W("became"), Transform(bl.bracket, b57), FadeOut(y1950), FadeIn(y2018), run_time=1.0)

        # cue 6: the 2026 preprint
        card = paper_card("The Euclidean plane is\nnot five-colorable", "OpenAI · September 23, 2026", w=3.4, h=4.0)
        card.scale(0.85).move_to(UP * 0.9)
        self.play_at(W("september"), FadeIn(card, shift=UP * 0.3), run_time=1.0)
        claim = label("5 is not enough?", 26, INK).next_to([bl.x(5), bl.y, 0], UP, buff=0.5)
        ghost = Line([bl.x(6), bl.y - 0.22, 0], [bl.x(6), bl.y + 0.22, 0], stroke_color=HOT_RING, stroke_width=5)
        self.play_at(W("claimed"), FadeOut(y2018), FadeIn(claim), Create(ghost), run_time=0.9)
        self.play(Wiggle(bl.bracket[1][0], scale_value=1.15), run_time=1.0)

        # cue 7: three questions this video answers
        qs = VGroup(label("how could anyone prove it?", 26, INK), label("what exactly was proved?", 26, INK),
                    label("what do we know about how it was found?", 26, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        qs.next_to(card, RIGHT, buff=0.8)
        self.play_at(self.cue(7), card.animate.shift(LEFT * 2.6), run_time=0.8)
        qs.next_to(card, RIGHT, buff=0.6).shift(LEFT * 0.0)
        for i, t in enumerate((W("prove"), W("proved"), W("found"))):
            self.play_at(t - 0.2, FadeIn(qs[i], shift=RIGHT * 0.15), run_time=0.6)

        # cue 8: title
        title = label("The Plane Needs Six", 64, INK, weight="BOLD")
        self.play_at(self.cue(8), FadeOut(VGroup(card, qs, claim, ghost, bl)), FadeOut(plane.image), run_time=0.6)
        self.play(FadeIn(title, scale=1.05), run_time=0.9)
        self.finish()
