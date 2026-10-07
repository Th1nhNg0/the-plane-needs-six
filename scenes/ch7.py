"""Chapter 7 · Checking it.   manim -qh scenes/ch7.py S7_1 S7_2 S7_3

Lean toy verified 2026-10-07 with Lean 4.34.1 (tools/lean_toy/Accepted.lean accepted; Rejected.lean rejected with the
error text shown on screen). The comparator statement is reproduced verbatim from
openai/math lean/ComparatorChallenges/EuclideanFiveColor.lean.
"""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.style import INK, MUTED, SOFT, EDGE, HOT, ORANGE, SKY, GREEN, PAL, colour, label, maths, backed
from components.widgets import status, source_line, verdict_row
from components.narrated import NarratedScene

MONO = "DejaVu Sans Mono"


def code(src, size=24, max_width=12.6):
    """Monospace panel. Leading spaces are kept as real characters (rendered with a visible-width placeholder)
    so indentation is exact; the whole panel is scaled down if wider than max_width."""
    lines = src.strip("\n").split("\n")
    ref = Text("M" * 10, font=MONO, font_size=size)
    cw = ref.width / 10
    g = VGroup()
    for i, l in enumerate(lines):
        lead = len(l) - len(l.lstrip(" "))
        t = Text(l.strip() if l.strip() else ".", font=MONO, font_size=size, color=INK)
        if not l.strip():
            t.set_opacity(0)
        t.move_to(np.array([0, -i * size * 0.0165, 0]), aligned_edge=LEFT).shift(RIGHT * lead * cw)
        g.add(t)
    if g.width > max_width:
        g.scale(max_width / g.width)
    frame = SurroundingRectangle(g, buff=0.35, color=MUTED, stroke_width=1.5, corner_radius=0.08)
    return VGroup(frame, g)


def box(text, w=3.2, h=1.1):
    r = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=INK, stroke_width=2.5)
    return VGroup(r, label(text, 30, INK).move_to(r))


class S7_1(NarratedScene):
    scene_id = "s7_1"

    def construct(self):
        W, C = self.word, self.wc
        stack = VGroup(*[RoundedRectangle(corner_radius=0.05, width=2.4, height=3.1).set_fill("#E9E4DA", 1).set_stroke("#B8B3AA", 1)
                         .shift(np.array([0.06 * i, -0.06 * i, 0])) for i in range(6)]).move_to(UP * 0.4)
        pages = label("62 pages", 26, MUTED).next_to(stack, DOWN, buff=0.3)
        self.play_at(C(1, "page"), FadeIn(stack, lag_ratio=0.1), FadeIn(pages), run_time=1.0)
        q1 = label("who wrote it?", 34, INK).move_to(LEFT * 4.2 + UP * 0.4)
        q2 = label("is it right?", 34, INK).move_to(RIGHT * 4.2 + UP * 0.4)
        self.play_at(C(1, "produced"), FadeIn(q1, shift=RIGHT * 0.2), run_time=0.7)
        self.play_at(C(1, "correct"), FadeIn(q2, shift=LEFT * 0.2), run_time=0.7)

        # cue 2: proof assistants: untrusted proof, small trusted kernel
        self.play_at(self.cue(2), FadeOut(VGroup(stack, pages, q1, q2)), run_time=0.6)
        b1 = box("proof (any author)", 3.8)
        b2 = box("kernel", 2.2)
        out = maths(r"\checkmark \ / \ \times", 44, INK)
        diag = VGroup(b1, b2, out).arrange(RIGHT, buff=1.0).move_to(UP * 0.6)
        a1 = Arrow(b1.get_right(), b2.get_left(), buff=0.12, color=MUTED, stroke_width=2.5)
        a2 = Arrow(b2.get_right(), out.get_left(), buff=0.12, color=MUTED, stroke_width=2.5)
        self.play_at(C(2, "lean"), FadeIn(b1), run_time=0.7)
        small = label("small, trusted", 24, MUTED, italic=True).next_to(b2, DOWN, buff=0.2)
        self.play_at(C(2, "small"), GrowArrow(a1), FadeIn(b2), FadeIn(small), run_time=0.9)
        self.play_at(C(2, "checks"), GrowArrow(a2), FadeIn(out), run_time=0.7)

        # cue 3: the toy
        self.play_at(self.cue(3), diag.animate.scale(0.55).to_edge(UP, buff=0.6), FadeOut(VGroup(a1, a2, small)), run_time=0.7)
        ok_src = """theorem triangle_two_colours :
    ∀ a b c : Bool, a ≠ b → b ≠ c → a ≠ c → False := by
  decide"""
        c1 = code(ok_src, 26).move_to(DOWN * 0.3)
        gloss = label("corners $a, b, c$ get colours from 2 options $\\Rightarrow$ some two corners match", 26, MUTED, italic=True).next_to(c1, DOWN, buff=0.35)
        self.play_at(C(3, "statement"), FadeIn(c1), FadeIn(gloss), run_time=1.0)
        acc = VGroup(maths(r"\checkmark", 48, colour(GREEN)), label("accepted", 30, INK)).arrange(RIGHT, buff=0.2).next_to(c1, UP, buff=0.3)
        self.play_at(C(3, "accepts"), FadeIn(acc, scale=1.2), run_time=0.6)

        # cue 4: change Bool to Fin 3: false claim, refused
        bad_src = """theorem triangle_three_colours :
    ∀ a b c : Fin 3, a ≠ b → b ≠ c → a ≠ c → False := by
  decide"""
        c2 = code(bad_src, 26).move_to(c1)
        self.play_at(C(4, "change"), FadeOut(acc), FadeOut(gloss), Transform(c1, c2), run_time=1.0)
        err = Text("error: Tactic `decide` proved that the proposition\n  ∀ (a b c : Fin 3), a ≠ b → b ≠ c → a ≠ c → False\nis false",
                   font=MONO, font_size=20, color=HOT, line_spacing=0.9).next_to(c1, DOWN, buff=0.35)
        rej = VGroup(maths(r"\times", 48, HOT), label("refused", 30, INK)).arrange(RIGHT, buff=0.2).next_to(c1, UP, buff=0.3)
        self.play_at(C(4, "refuses"), FadeIn(rej, scale=1.2), FadeIn(err), run_time=0.8)
        ver = label("verified with Lean 4.34.1", 20, MUTED, italic=True).to_corner(DR, buff=0.35)
        self.play(FadeIn(ver), run_time=0.4)

        # cue 5: trust = kernel + reading the statement
        self.play_at(self.cue(5), FadeOut(VGroup(c1, err, rej, ver)), diag.animate.scale(1 / 0.55).move_to(UP * 0.6), run_time=0.9)
        read = label("the statement: read it carefully", 30, INK).next_to(diag, DOWN, buff=0.7)
        self.play_at(C(5, "trust"), Indicate(diag[1], color=colour(SKY), scale_factor=1.15), run_time=0.9)
        self.play_at(C(5, "statement"), FadeIn(read), Indicate(diag[0], color=colour(ORANGE), scale_factor=1.05), run_time=0.9)
        self.finish()


class S7_2(NarratedScene):
    scene_id = "s7_2"

    def construct(self):
        W, C = self.word, self.wc
        stmt = """def ProperColoring (colorCount : ℕ) (coloring : ℂ → Fin colorCount) : Prop :=
  ∀ point otherPoint : ℂ, ‖point - otherPoint‖ = 1 →
    coloring point ≠ coloring otherPoint

theorem no_proper_five_coloring :
    ¬ ∃ coloring : ℂ → Fin 5, ProperColoring 5 coloring"""
        c = code(stmt, 22).move_to(UP * 1.2)
        src = label("verbatim from openai/math: lean/ComparatorChallenges/EuclideanFiveColor.lean (statement only)", 20, MUTED)
        src.scale_to_fit_width(min(src.width, 12)).to_edge(DOWN, buff=0.3)
        self.play_at(C(1, "statement"), FadeIn(c), FadeIn(src), run_time=1.2)
        lines = c[1]
        gl = [(lines[0], "any function: plane $\\to$ 5 colours", C(2, "function")),
              (lines[1], "distance exactly 1", C(2, "distance")),
              (lines[2], "different colours", C(2, "different")),
              (lines[5], "no such colouring exists", C(2, "theorem"))]
        notes = VGroup()
        for i, (ln, txt, t) in enumerate(gl):
            n = label(txt, 26, colour(SKY), italic=True)
            if i < 3:
                n.next_to(c, DOWN, buff=0.35 + 0.42 * i).align_to(c, LEFT)
            else:
                n.next_to(c, DOWN, buff=0.35 + 0.42 * 3).align_to(c, LEFT)
            notes.add(n)
            self.play_at(t, Indicate(ln, color=colour(SKY), scale_factor=1.03), FadeIn(n), run_time=0.8)

        # cue 3: no measurability assumption
        miss = VGroup(label("measurable?", 32, MUTED), label("not assumed", 30, INK)).arrange(RIGHT, buff=0.4).next_to(c, DOWN, buff=0.6)
        strike = Line(miss[0].get_left(), miss[0].get_right(), stroke_color=HOT, stroke_width=3)
        self.play_at(C(3, "assumption"), FadeOut(notes), FadeIn(miss[0]), run_time=0.6)
        self.play_at(C(3, "measurable"), Create(strike), FadeIn(miss[1]), run_time=0.7)
        unr = label("the unrestricted problem", 30, INK, italic=True).next_to(miss, DOWN, buff=0.3)
        self.play_at(C(3, "unrestricted"), FadeIn(unr), run_time=0.6)

        # cue 4: axioms, size, structure, the 7-colouring
        self.play_at(self.cue(4), FadeOut(VGroup(miss, strike, unr)), c.animate.scale(0.75).to_edge(UP, buff=0.4), run_time=0.8)
        facts = VGroup(
            VGroup(status("FACT", 18), maths(r"\text{permitted axioms: \texttt{propext}, \texttt{Quot.sound}, \texttt{Classical.choice}}", 28, INK)),
            VGroup(status("FACT", 18), maths(r"\approx 30{,}000 \text{ lines of Lean, built on Mathlib}", 28, INK)),
            VGroup(status("FACT", 18), label("two halves, as in the paper: proper $\\to$ weak measurable;\\\\ no weak measurable 5-colouring", 26, INK)),
            VGroup(status("FACT", 18), label("the 7-colouring is formalized separately", 26, INK)),
        )
        for f in facts:
            f.arrange(RIGHT, buff=0.3)
        facts.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(DOWN * 0.9)
        for f, t in zip(facts, (C(4, "axioms"), C(4, "30"), C(4, "follows"), C(4, "separate"))):
            self.play_at(t, FadeIn(f, shift=RIGHT * 0.15), run_time=0.6)

        # cue 5: accurate summary + what this production checked
        self.play_at(self.cue(5), FadeOut(facts), run_time=0.5)
        summ = VGroup(status("FACT", 22), label("OpenAI reports a formal verification of the full, unrestricted statement", 32, INK)).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.3)
        self.play_at(C(5, "openai"), FadeIn(summ), run_time=0.9)
        mine = VGroup(label("this production: static scan of the files found no \\texttt{sorry} and no extra axioms", 26, MUTED, italic=True),
                      label("not rebuilt by us", 26, INK, italic=True)).arrange(DOWN, buff=0.2).next_to(summ, DOWN, buff=0.5)
        self.play_at(C(5, "scanned"), FadeIn(mine[0]), run_time=0.7)
        self.play_at(C(5, "rebuild"), FadeIn(mine[1]), run_time=0.6)
        self.finish()


class S7_3(NarratedScene):
    scene_id = "s7_3"

    def construct(self):
        W, C = self.word, self.wc
        head = label("five words, five meanings", 38, INK).to_edge(UP, buff=0.7)
        self.play_at(self.cue(1), FadeIn(head), run_time=0.6)
        rows = VGroup(verdict_row("AI-generated", "yes", "per OpenAI"),
                      verdict_row("computer-checked (7-point certificate)", "yes", "re-checked here"),
                      verdict_row("formally verified (Lean)", "reported", "reported by OpenAI"),
                      verdict_row("independently reproduced", "no", "no public evidence"),
                      verdict_row("peer reviewed", "no", "no; preprint")).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(DOWN * 0.3)
        for k, r in enumerate(rows):
            self.play_at(self.cue(k + 2), FadeIn(r, shift=RIGHT * 0.2), run_time=0.6)
        chip = label("catalogue of formalizations, review status (catalogue-wide): \\emph{unchecked}", 24, MUTED, italic=True).next_to(rows, DOWN, buff=0.4)
        self.play_at(C(6, "unchecked"), FadeIn(chip), run_time=0.7)
        self.play_at(self.cue(7), Indicate(rows, color=INK, scale_factor=1.02), run_time=1.2)
        self.finish()
