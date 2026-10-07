"""Chapter 8 · Why it matters.   manim -qh scenes/ch8.py S8_1 S8_2"""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.style import INK, MUTED, SOFT, EDGE, HOT, ORANGE, SKY, GREEN, PAL, colour, label, maths, backed
from components.widgets import BoundsLine, ProofRail, hex_tiling, status
from components.narrated import NarratedScene
from scenes.ch3 import mini_spindle


class S8_1(NarratedScene):
    scene_id = "s8_1"

    def construct(self):
        W, C = self.word, self.wc
        q = label("What changed?", 44, INK).to_edge(UP, buff=0.8)
        self.play_at(self.cue(1), Write(q), run_time=0.8)
        bl = BoundsLine(4, 7, y=-0.4, width=10)
        yr = label("1950", 34, INK).move_to(UP * 1.2)
        self.play_at(C(2, "1950"), FadeIn(bl), FadeIn(yr), run_time=0.9)
        self.play_at(C(2, "2018"), Transform(bl.bracket, bl.set_bounds(5, 7)), Transform(yr, label("2018", 34, INK).move_to(yr)), run_time=0.9)
        rep = label("if it holds up; formal check reported by OpenAI", 26, MUTED, italic=True).next_to(bl, DOWN, buff=0.9)
        self.play_at(C(2, "reports"), FadeIn(rep), run_time=0.8)
        self.play_at(C(2, "six"), Transform(bl.bracket, bl.set_bounds(6, 7)), Transform(yr, label("2026", 34, INK).move_to(yr)), run_time=0.9)
        ans = maths(r"\chi(\mathbb{R}^2) \in \{6, 7\}", 48, INK).next_to(yr, UP, buff=0.4)
        self.play_at(C(2, "answer"), FadeOut(q), Write(ans), run_time=1.0)

        # cue 3: which one is open
        qm = maths("?", 56, HOT).move_to([bl.x(6.5), bl.y + 0.6, 0])
        self.play_at(self.cue(3), FadeIn(qm, scale=1.4), run_time=0.6)
        hx, _ = hex_tiling(0.3, 7, extent=(2.4, 1.6))
        hx.move_to(LEFT * 4.6 + UP * 1.6)
        hl = label("Isbell's hexagons: best possible?", 24, MUTED, italic=True).next_to(hx, DOWN, buff=0.2)
        self.play_at(C(3, "hexagons"), FadeIn(hx), FadeIn(hl), run_time=0.8)
        ex = label("or an exotic 6-colouring?", 24, MUTED, italic=True).move_to(RIGHT * 4.4 + UP * 1.6)
        self.play_at(C(3, "exotic"), FadeIn(ex), run_time=0.7)

        # cue 4: the unseen graph
        blob = VGroup(*[mini_spindle(0.3, a).shift(np.array([np.cos(a) * 0.8, np.sin(a) * 0.5, 0]))
                        for a in np.linspace(0, TAU, 9)[:-1]]).move_to(DOWN * 2.6 + RIGHT * 3.2).fade(0.6)
        bt = label("a finite graph needing 6 colours: nobody has seen it", 24, MUTED, italic=True).next_to(blob, LEFT, buff=0.4)
        self.play_at(self.cue(4), FadeOut(rep), FadeIn(blob), FadeIn(bt), run_time=1.0)

        # cue 5: a tool left behind
        tool = backed(maths(r"\text{proper } k\text{-colouring} \iff \text{weak measurable } k\text{-colouring} \quad (\text{every } k)", 30, INK))
        tool.to_edge(DOWN, buff=0.35)
        self.play_at(C(5, "transfer"), FadeOut(VGroup(blob, bt)), Write(tool), run_time=1.6)
        self.finish()


class S8_2(NarratedScene):
    scene_id = "s8_2"

    def construct(self):
        W, C = self.word, self.wc
        q = label("What does this release show?", 40, INK).to_edge(UP, buff=0.6)
        self.play_at(self.cue(1), Write(q), run_time=0.9)
        lh = label("shows", 32, colour(GREEN)).move_to(LEFT * 4.6 + UP * 1.9)
        rh = label("doesn't show", 32, HOT)
        shows = VGroup(label("a long, technical proof engaging decades of work (33 references)", 26, INK),
                       label("main statement formalized; checked by machine, per OpenAI", 26, INK),
                       label("a route around the finite-graph search", 26, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        shows.next_to(lh, DOWN, buff=0.3).align_to(lh, LEFT)
        dont = VGroup(*[VGroup(status("NOT PUBLIC", 18), label(t, 26, INK)).arrange(RIGHT, buff=0.2)
                        for t in ("how often the model is wrong (selected results only)", "how much human guidance",
                                  "effort compared with human research")]).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        rh.next_to(shows, DOWN, buff=0.55).align_to(lh, LEFT)
        dont.next_to(rh, DOWN, buff=0.3).align_to(lh, LEFT)
        self.play_at(self.cue(2), FadeIn(lh), FadeIn(shows[0]), run_time=0.8)
        self.play_at(C(2, "formalised"), FadeIn(shows[1]), run_time=0.7)
        self.play_at(self.cue(3), FadeIn(shows[2]), run_time=0.7)
        self.play_at(C(4, "wrong"), FadeIn(rh), FadeIn(dont[0]), run_time=0.8)
        warn = label("OpenAI: some unformalized results may have issues", 20, MUTED, italic=True).next_to(dont, DOWN, buff=0.3).align_to(dont, LEFT)
        self.play_at(C(4, "warns"), FadeIn(warn), run_time=0.6)
        self.play_at(C(4, "guidance"), FadeIn(dont[1]), run_time=0.6)
        self.play_at(C(4, "compares"), FadeIn(dont[2]), run_time=0.6)

        # cue 5: 1950, 1961, 2026
        self.play_at(self.cue(5), FadeOut(VGroup(q, lh, rh, shows, dont, warn)), run_time=0.8)
        rule = maths(r"|xy| = 1 \Rightarrow c(x) \neq c(y)", 32, INK)
        sp = mini_spindle(0.75, colours={k: c for k, c in zip(["p", "a1", "b1", "t1", "a2", "b2", "t2"], [0, 1, 2, 0, 1, 2, 3])})
        rail = ProofRail(width=8, size=13).lit(7, 7)
        rail.halves.set_opacity(0)
        trio = VGroup(VGroup(rule, label("1950", 28, MUTED)).arrange(DOWN, buff=0.3),
                      VGroup(sp, label("1961", 28, MUTED)).arrange(DOWN, buff=0.3),
                      VGroup(rail.scale(0.5), label("2026", 28, MUTED)).arrange(DOWN, buff=0.3)).arrange(RIGHT, buff=0.9).move_to(UP * 0.4)
        self.play_at(C(5, "question"), FadeIn(trio[0]), run_time=0.8)
        self.play_at(C(5, "figure"), FadeIn(trio[1]), run_time=0.8)
        self.play_at(C(5, "proof"), FadeIn(trio[2]), run_time=0.8)

        # cue 6: six or seven
        bl = BoundsLine(6, 7, y=-2.4, width=9)
        fin = maths(r"6 \ \text{ or } \ 7\,?", 64, INK)
        self.play_at(self.cue(6), FadeOut(trio), FadeIn(bl), Write(fin), run_time=1.0)
        self.play_at(C(6, "still"), Indicate(fin, color=HOT, scale_factor=1.08), run_time=1.0)
        self.finish()


class Credits(Scene):
    """Silent end card: sources and production notes (not narrated)."""

    def construct(self):
        from components.style import BG
        self.camera.background_color = BG
        head = label("Sources", 40, INK).to_edge(UP, buff=0.6)
        src = VGroup(*[label(t, 22, INK) for t in (
            "OpenAI, \\emph{The Euclidean plane is not five-colorable}, preprint, September 23, 2026 (github.com/openai/math)",
            "openai/math: README, CONTENTS (family 158), lean/docs/158.md, Lean comparator statement, reasoning summary 017",
            "A. D. N. J. de Grey, \\emph{The chromatic number of the plane is at least 5}, Geombinatorics 2018",
            "M. J. H. Heule, \\emph{Computing small unit-distance graphs with chromatic number 5}, 2018",
            "J. Parts, 2020; G. Exoo and D. Ismailescu, 2020; L. and W. Moser, 1961; H. Hadwiger, 1961",
            "N. G. de Bruijn and P. Erd\\H{o}s, 1951; K. J. Falconer, 1981; M. S. Payne, 2009; S. P. Townsend, 1981/2005",
            "G. Sokolov and V. Voronov, 2025; A. Soifer, 2003",
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        src.scale_to_fit_width(min(src.width, 12.8)).next_to(head, DOWN, buff=0.5)
        notes = VGroup(label("toy problems and analogies are this production's own; pictures of 5-colourings are schematic", 22, MUTED, italic=True),
                       label("narration: ElevenLabs eleven_v4 (voice: George) $\\cdot$ animation: Manim Community", 22, MUTED, italic=True),
                       label("full source list and claim-by-claim notes: research/brief.md", 22, MUTED, italic=True)).arrange(DOWN, buff=0.18)
        notes.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(head), FadeIn(src, lag_ratio=0.05), run_time=1.5)
        self.play(FadeIn(notes), run_time=1.0)
        self.wait(10)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
