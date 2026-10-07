"""Chapter 6 · What the AI did, and what we don't know.   manim -qh scenes/ch6.py S6_1 S6_2 S6_3 S6_4

Every claim on screen carries a status: FACT (with source line), INFERENCE (possible reconstruction, not confirmed
by OpenAI) or NOT PUBLIC. No narrated inner monologue for the model.
"""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.style import INK, MUTED, SOFT, EDGE, HOT, ORANGE, SKY, GREEN, PAL, colour, label, maths, backed
from components.widgets import paper_card, status, source_line
from components.narrated import NarratedScene

README = "source: github.com/openai/math, README, “How the results were produced”"


def fact_row(text, size=32, src=None):
    t = label(text, size, INK)
    s = status("FACT")
    row = VGroup(s, t).arrange(RIGHT, buff=0.35)
    return row


class S6_1(NarratedScene):
    scene_id = "s6_1"

    def construct(self):
        W, C = self.word, self.wc
        q = label("Who wrote this?", 48, INK)
        self.play_at(C(1, "who"), Write(q), run_time=0.8)
        card = paper_card("The Euclidean plane is\nnot five-colorable", "OpenAI · September 23, 2026", w=3.4, h=4.0).scale(0.8)
        card.move_to(LEFT * 4.2 + DOWN * 0.3)
        self.play_at(C(1, "preprint"), q.animate.to_edge(UP, buff=0.6), FadeIn(card, shift=UP * 0.2), run_time=0.9)
        repo = VGroup(label("public repository", 30, INK),
                      maths(r"722 \text{ manuscripts} \;\cdot\; 372 \text{ families}", 34, INK)).arrange(DOWN, buff=0.2)
        repo.move_to(RIGHT * 2.2 + UP * 1.2)
        self.play_at(C(1, "722"), FadeIn(repo), run_time=0.8)
        prod = fact_row("produced by an internal, unreleased OpenAI model", 28).next_to(repo, DOWN, buff=0.5)
        src = source_line(README).to_edge(DOWN, buff=0.35)
        self.play_at(C(1, "produced"), FadeIn(prod), FadeIn(src), run_time=0.8)

        # cue 2: process facts
        rows = VGroup(fact_row("the vast majority: one standard procedure", 26),
                      fact_row("about 4,000 problems posed", 26),
                      fact_row("on average about 3 hours of ChatGPT Pro thinking compute per result", 26)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(prod, DOWN, buff=0.45).align_to(prod, LEFT)
        if rows.get_right()[0] > 6.8:
            rows.shift(LEFT * (rows.get_right()[0] - 6.8))
        self.play_at(C(2, "majority"), FadeIn(rows[0]), run_time=0.7)
        self.play_at(C(2, "posed"), FadeIn(rows[1]), run_time=0.7)
        self.play_at(C(2, "average"), FadeIn(rows[2]), run_time=0.7)
        quote = label("“On average, each result used three hours of ChatGPT Pro thinking compute with that model.”",
                      22, MUTED, italic=True).next_to(src, UP, buff=0.2)
        self.play(FadeIn(quote), run_time=0.6)

        # cue 3: the funnel
        self.play_at(self.cue(3), FadeOut(VGroup(card, rows, prod, quote)), repo.animate.set_opacity(0.0), run_time=0.6)
        steps = VGroup(maths(r"\approx 4{,}000 \text{ problems}", 36, INK), maths(r"\text{grouped into families}", 32, INK),
                       maths(r"\text{significance bar}", 32, INK), maths(r"722 \text{ manuscripts}", 36, INK)).arrange(DOWN, buff=0.45)
        arrows = VGroup(*[Arrow(steps[i].get_bottom(), steps[i + 1].get_top(), buff=0.08, color=MUTED, stroke_width=2.5)
                          for i in range(3)])
        funnel = VGroup(steps, arrows).move_to(DOWN * 0.2)
        self.play_at(C(3, "grouped"), FadeIn(steps[0]), GrowArrow(arrows[0]), FadeIn(steps[1]), run_time=1.0)
        self.play_at(C(3, "significance"), GrowArrow(arrows[1]), FadeIn(steps[2]), GrowArrow(arrows[2]), FadeIn(steps[3]), run_time=1.0)

        # cue 4: an average, not a figure for this proof
        avg = backed(label("3 hours: an average across results, not a figure for this proof", 30, INK)).next_to(funnel, DOWN, buff=0.5)
        self.play_at(C(4, "average"), FadeOut(funnel), FadeIn(avg.move_to(ORIGIN)), run_time=0.9)
        self.finish()


class S6_2(NarratedScene):
    scene_id = "s6_2"

    def construct(self):
        W, C = self.word, self.wc
        fams = ["007", "017", "087", "102", "159", "197", "221", "271", "287", "362"]
        head = label("published reasoning summaries (10 results)", 30, INK).to_edge(UP, buff=0.8)
        codes = VGroup(*[maths(f, 32, INK) for f in fams]).arrange(RIGHT, buff=0.45).next_to(head, DOWN, buff=0.4)
        self.play_at(C(1, "released"), FadeIn(head), FadeIn(codes, lag_ratio=0.08), run_time=1.0)
        ours = VGroup(maths("158", 36, HOT), label("this result: no summary", 28, INK)).arrange(RIGHT, buff=0.3).next_to(codes, DOWN, buff=0.5)
        self.play_at(C(1, "this"), FadeIn(ours), run_time=0.7)

        # cue 2: not public
        items = ["the exact prompt", "how many attempts", "which tools", "compute for this proof", "human steering",
                 "who wrote the Lean statement"]
        cards = VGroup(*[VGroup(status("NOT PUBLIC", 18), label(t, 28, INK)).arrange(DOWN, buff=0.12) for t in items])
        cards.arrange_in_grid(2, 3, buff=(0.8, 0.5)).move_to(DOWN * 1.4)
        times = [C(2, "prompt"), C(2, "attempts"), C(2, "tools"), C(2, "compute"), C(2, "steered"), C(2, "way") + 0.2]
        for c, t in zip(cards, times):
            self.play_at(t, FadeIn(c, shift=UP * 0.15), run_time=0.5)

        # cue 3: an inference, labelled as such
        self.play_at(self.cue(3), FadeOut(VGroup(head, codes, ours, cards)), run_time=0.6)
        inf = VGroup(status("INFERENCE", 22), label("this result probably followed the standard procedure", 32, INK),
                     label("(it is not listed among the README's named exceptions)", 26, MUTED, italic=True)).arrange(DOWN, buff=0.3)
        self.play_at(C(3, "result"), FadeIn(inf[1]), FadeIn(inf[2]), run_time=0.9)
        self.play_at(C(3, "inference"), FadeIn(inf[0], scale=1.1), run_time=0.7)
        self.finish()


class S6_3(NarratedScene):
    scene_id = "s6_3"

    def construct(self):
        W, C = self.word, self.wc
        banner = status("DIFFERENT RESULT", 24).to_edge(UP, buff=0.5)
        self.play_at(C(1, "different"), FadeIn(banner), run_time=0.6)
        page = RoundedRectangle(corner_radius=0.06, width=5.2, height=5.6).set_fill("#E9E4DA", 1).set_stroke(width=0).move_to(LEFT * 3.4 + DOWN * 0.5)
        title = Text("Summarized chain of thought\n(The irrationality exponent of π is 2)", font="Latin Modern Roman",
                     font_size=20, color="#22252B", line_spacing=0.8).move_to(page.get_top() + DOWN * 0.55)
        lines = VGroup(*[Line(LEFT, RIGHT, stroke_color="#B8B3AA", stroke_width=2).set_width(4.2 * (0.6 + 0.4 * ((i * 37) % 7) / 7))
                         for i in range(14)]).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(title, DOWN, buff=0.35).align_to(page, LEFT).shift(RIGHT * 0.4)
        doc = VGroup(page, title, lines)
        self.play_at(C(1, "pi"), FadeIn(doc, shift=UP * 0.2), run_time=1.0)
        ab = VGroup(*[label(t, 26, MUTED) for t in ("approach A $\\times$", "approach B $\\times$", "approach C $\\times$", "approach D")]
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(page, RIGHT, buff=0.6).shift(UP * 1.2)
        self.play_at(C(1, "attempts"), LaggedStart(*[FadeIn(a) for a in ab], lag_ratio=0.3), run_time=1.4)
        quote = VGroup(label("verbatim excerpt from that summary:", 24, MUTED, italic=True),
                       Text("“Polynomial log imposes finitely many parameters,\n eliminates arbitrary infinite path. Degree C huge\n but fixed; need theorem using its structure.”",
                            font="DejaVu Sans Mono", font_size=15, color=INK, line_spacing=0.9)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        quote.next_to(ab, DOWN, buff=0.5).align_to(ab, LEFT)
        src = label("source: openai/math, reasoning_traces/irrationality-exponent-of-pi.pdf, p. 1", 20, MUTED).to_edge(DOWN, buff=0.3)
        self.play_at(C(1, "verbatim"), FadeIn(quote), FadeIn(src), run_time=0.9)

        # cue 2: a different problem
        wall = VGroup(Line(UP * 3, DOWN * 3, stroke_color=HOT, stroke_width=3),
                      label("tells us nothing specific about the five-colour proof", 28, INK)).arrange(RIGHT, buff=0.4)
        self.play_at(C(2, "different"), FadeOut(VGroup(ab, quote)), doc.animate.scale(0.75).to_edge(LEFT, buff=0.6), run_time=0.8)
        wall.next_to(doc, RIGHT, buff=0.6)
        self.play_at(C(2, "nothing"), FadeIn(wall), run_time=0.8)
        self.finish()


class S6_4(NarratedScene):
    scene_id = "s6_4"

    def construct(self):
        W, C = self.word, self.wc
        q = label("Reasoning or brute force?", 46, INK).to_edge(UP, buff=0.7)
        self.play_at(C(1, "reasoning"), Write(q), run_time=0.9)
        lh = label("in the proof", 32, INK).move_to(UP * 1.6)
        self.play_at(C(1, "proof"), FadeIn(lh), run_time=0.5)
        comp = VGroup(label("computation", 28, MUTED), label("one 7-point exact check", 26, INK)).arrange(DOWN, buff=0.2).move_to(LEFT * 3.6 + UP * 0.4)
        conc = VGroup(label("concepts", 28, MUTED), label("averaging and symmetry", 26, INK), label("topology", 26, INK),
                      label("geometry", 26, INK)).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.0 + UP * 0.1)
        self.play_at(C(1, "seven"), FadeIn(comp), run_time=0.7)
        self.play_at(C(1, "averaging"), FadeIn(conc[0]), FadeIn(conc[1]), run_time=0.6)
        self.play_at(C(1, "topology"), FadeIn(conc[2]), run_time=0.5)
        self.play_at(C(1, "geometry"), FadeIn(conc[3]), run_time=0.5)
        cites = VGroup(*[label(t, 24, MUTED, italic=True) for t in ("Falconer 1981", "Payne 2009", "Furstenberg--Zimmer",
                                                                     "Townsend", "Sokolov--Voronov 2025")]).arrange(RIGHT, buff=0.45).move_to(DOWN * 1.7)
        cl = label("tools the paper credits", 24, MUTED).next_to(cites, UP, buff=0.2)
        self.play_at(C(1, "builds"), FadeIn(cl), LaggedStart(*[FadeIn(c) for c in cites], lag_ratio=0.25), run_time=1.6)

        # cue 2: the process
        self.play_at(self.cue(2), FadeOut(VGroup(lh, comp, conc, cites, cl)), run_time=0.6)
        ph = label("in the process", 32, INK).move_to(UP * 1.6)
        steps = VGroup(maths(r"\approx 4{,}000 \text{ problems}", 34, INK), maths(r"\text{selected results}", 34, INK)).arrange(RIGHT, buff=1.6).move_to(UP * 0.4)
        arr = Arrow(steps[0].get_right(), steps[1].get_left(), buff=0.2, color=MUTED, stroke_width=2.5)
        self.play_at(C(2, "process"), FadeIn(ph), run_time=0.5)
        self.play_at(C(2, "posing"), FadeIn(steps[0]), GrowArrow(arr), FadeIn(steps[1]), run_time=1.0)
        search = label("itself a kind of search, at a very large scale", 28, INK, italic=True).next_to(steps, DOWN, buff=0.5)
        self.play_at(C(2, "search"), FadeIn(search), run_time=0.7)
        unk = VGroup(*[VGroup(status("NOT PUBLIC", 18), label(t, 26, INK)).arrange(RIGHT, buff=0.25)
                       for t in ("how much selection was automatic", "how often the model was wrong")]).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        unk.next_to(search, DOWN, buff=0.5)
        self.play_at(C(2, "selection"), FadeIn(unk[0]), run_time=0.6)
        self.play_at(C(2, "wrong"), FadeIn(unk[1]), run_time=0.6)
        self.finish()
