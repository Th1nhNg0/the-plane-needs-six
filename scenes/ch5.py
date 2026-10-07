"""Chapter 5 · The new proof.   manim -qh scenes/ch5.py S5_0 S5_1 S5_2 S5_3 S5_4 S5_5

All pictures of a 5-colouring in this chapter are schematic: the proof is by contradiction, and the paper shows
no such colouring exists. Each such picture carries a small 'schematic' note.
"""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.style import (BG, INK, MUTED, SOFT, EDGE, HOT, ORANGE, SKY, GREEN, YELLOW, BLUE, PAL, colour, label,
                              maths, tag, marker, stick, burning, region, backed)
from components.widgets import ProofRail, WildPlane, RegionPlane, unit_stick
from components.narrated import NarratedScene

S = 2.2  # manim units per unit distance in this chapter


def schematic():
    return label("schematic", 22, MUTED, italic=True).to_corner(DR, buff=0.35)


def mini_rail(lit, active):
    r = ProofRail(width=12.6, y=3.35, size=14)
    t = r.lit(lit, active)
    t.halves.set_opacity(0)
    return t.scale(0.85).to_edge(UP, buff=0.15)


def blurred_field(seed=0, res=0.06, blob=0.6, dim=0.45, colours=(ORANGE, SKY, GREEN, YELLOW, BLUE)):
    """Soft probability field: per-point colour mix of a blurred random 5-colouring (rendered as an image)."""
    rng = np.random.default_rng(seed)
    w, h = config.frame_width, config.frame_height
    nx, ny = int(w / res), int(h / res)
    f = rng.random((len(colours), ny, nx))
    k = max(1, int(blob / res))
    for _ in range(3):
        for ax in (1, 2):
            c = np.cumsum(f, axis=ax)
            c = np.concatenate([np.zeros_like(np.take(c, [0], axis=ax)), c], axis=ax)
            hi = np.clip(np.arange(f.shape[ax]) + k, 0, f.shape[ax])
            lo = np.clip(np.arange(f.shape[ax]) - k, 0, f.shape[ax])
            f = (np.take(c, hi, axis=ax) - np.take(c, lo, axis=ax)) / (hi - lo).reshape([-1 if i == ax else 1 for i in range(3)])
    f = f ** 6
    f = f / f.sum(axis=0, keepdims=True)
    rgb = np.zeros((ny, nx, 3))
    for i, cid in enumerate(colours):
        col = np.array([int(PAL[cid].to_hex()[j:j + 2], 16) for j in (1, 3, 5)], float)
        rgb += f[i][..., None] * col
    bg = np.array([0x0F, 0x10, 0x13], float)
    rgb = (bg + (rgb - bg) * dim).astype(np.uint8)
    img = ImageMobject(rgb).stretch_to_fit_width(w).stretch_to_fit_height(h)
    return img.set_z_index(-50)


class S5_0(NarratedScene):
    scene_id = "s5_0"

    def construct(self):
        W = self.word
        assume = maths(r"\text{Suppose a proper 5-colouring of the plane exists.}", 40, INK).move_to(UP * 0.8)
        self.play_at(W("suppose"), Write(assume), run_time=1.6)
        contra = maths(r"\Longrightarrow\ \text{something impossible} \quad (\bot)", 40, INK).next_to(assume, DOWN, buff=0.5)
        self.play_at(W("something"), Write(contra), run_time=1.2)

        rail = ProofRail()
        rail.move_to(UP * 0.6)
        self.play_at(W("runs"), FadeOut(VGroup(assume, contra)), Create(rail.track), FadeIn(rail.dots), run_time=1.2)
        self.play(FadeIn(rail.names, lag_ratio=0.1), run_time=1.0)
        self.play_at(W("tames"), FadeIn(rail.halves[0]), Indicate(VGroup(*rail.names[:4]), color=INK, scale_factor=1.05), run_time=1.0)
        meas = label("arbitrary $\\to$ measurable (in a relaxed sense)", 28, MUTED, italic=True).next_to(rail, DOWN, buff=0.7).shift(LEFT * 3.2)
        self.play_at(W("measurable", 1), FadeIn(meas), run_time=0.8)
        self.play_at(W("traps"), FadeIn(rail.halves[1]), Indicate(VGroup(*rail.names[4:]), color=INK, scale_factor=1.05), run_time=1.0)
        geo = label("geometry and topology", 28, MUTED, italic=True).next_to(rail, DOWN, buff=0.7).shift(RIGHT * 3.2)
        self.play_at(W("geometry"), FadeIn(geo), run_time=0.8)

        tok = rail.token(0)
        self.play_at(W("travel"), Transform(rail, rail.lit(0, 0)), FadeIn(tok, scale=1.5), run_time=0.8)
        warn = label("simplified: the paper is 62 pages", 30, INK, italic=True).to_edge(DOWN, buff=1.0)
        self.play_at(W("62"), FadeOut(VGroup(meas, geo)), Write(warn), run_time=1.2)
        warn2 = label("I'll say when I'm only describing an idea", 26, MUTED, italic=True).next_to(warn, DOWN, buff=0.25)
        self.play_at(W("only"), FadeIn(warn2), run_time=0.8)
        self.finish()


class S5_1(NarratedScene):
    """Taming wild colourings: the transfer theorem (paper Thm 1.3, §§2–4)."""
    scene_id = "s5_1"

    def construct(self):
        W = self.word
        rail = mini_rail(0, 0)
        self.add(rail)
        five = (ORANGE, SKY, GREEN, YELLOW, BLUE)
        frame = Rectangle(width=6.0, height=3.6, stroke_color=MUTED, stroke_width=2).move_to(DOWN * 0.4)
        wild = WildPlane(cell=0.08, colours=five, seed=12, dim=0.55)
        wild.image.stretch_to_fit_width(6.0).stretch_to_fit_height(3.6).move_to(frame)
        self.play_at(self.cue(1), FadeIn(wild.image), Create(frame), run_time=1.0)

        # cue 2: averaging copies (shifted and rotated)
        copies = Group()
        rng = np.random.default_rng(1)
        for i in range(7):
            w = WildPlane(cell=0.08, colours=five, seed=100 + i, dim=0.55).image
            w.stretch_to_fit_width(6.0).stretch_to_fit_height(3.6).move_to(frame).set_opacity(0.0)
            copies.add(w)
        self.play_at(W("shifted"), *[c.animate.set_opacity(0.35).shift(np.array([rng.normal(0, 0.25), rng.normal(0, 0.15), 0]))
                                     for c in copies[:4]], run_time=1.2)
        self.play_at(W("rotated"), *[c.animate.set_opacity(0.35).rotate(rng.uniform(-0.3, 0.3)).shift(np.array([rng.normal(0, 0.2), 0, 0]))
                                     for c in copies[4:]], run_time=1.2)
        soft = blurred_field(seed=5, blob=0.9, dim=0.45)
        soft.stretch_to_fit_width(6.0).stretch_to_fit_height(3.6).move_to(frame)
        self.play_at(W("blend"), FadeOut(copies), FadeOut(wild.image), FadeIn(soft), run_time=1.4)

        # cue 3: symmetric statistics; the rule survives
        bars = VGroup(*[Rectangle(width=0.35, height=1.2, stroke_width=0).set_fill(PAL[c], 0.85) for c in five]).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
        stats = VGroup(bars, label("colour frequencies", 22, MUTED, italic=True).next_to(bars, DOWN, buff=0.15)).next_to(frame, RIGHT, buff=0.6)
        compass = VGroup(Circle(radius=0.35, stroke_color=INK, stroke_width=2.5), Arrow(ORIGIN, UP * 0.32, buff=0, color=INK, stroke_width=3,
                                                                                     max_tip_length_to_length_ratio=0.35)).move_to(frame.get_center() + LEFT * 1.8)
        self.play_at(W("symmetric"), FadeIn(compass), FadeIn(stats), run_time=0.8)
        self.play_at(W("everywhere"), compass.animate.shift(RIGHT * 3.4 + UP * 0.6).rotate(-2.2), run_time=self.cue_end(3) - W("everywhere") - 6.5)
        rule = backed(maths(r"\Pr\big[\,c(x) = c(x+u)\,\big] = 0 \quad (|u| = 1)", 34, INK)).next_to(frame, DOWN, buff=0.35)
        self.play_at(W("obeyed"), FadeOut(compass), Write(rule), run_time=1.4)

        # cue 4: split into smooth part + everything else (1-D cross-section)
        self.play_at(self.cue(4), FadeOut(Group(soft, frame, stats, rule)), run_time=0.8)
        ax = [Axes(x_range=[0, 10, 1], y_range=[-0.2, 1.2, 1], x_length=9, y_length=1.3, tips=False,
                   axis_config={"stroke_color": MUTED, "stroke_width": 1.5, "include_ticks": False}) for _ in range(3)]
        xs = np.linspace(0, 10, 600)
        smooth = 0.5 + 0.28 * np.sin(1.3 * xs) * np.cos(0.4 * xs)
        noise = np.clip(np.random.default_rng(4).normal(0, 0.28, xs.size), -0.5, 0.5)
        total = np.clip(smooth + noise, 0, 1)
        def curve(a, ys, col):
            return VMobject(stroke_color=col, stroke_width=2.2).set_points_as_corners([a.c2p(x, y) for x, y in zip(xs, ys)])
        rows = VGroup()
        for a, ys, col, name in ((ax[0], total, PAL[ORANGE], r"\mathbf{1}_{\text{orange}}"), (ax[1], smooth, INK, r"\text{smooth part}"),
                                 (ax[2], noise + 0.5, MUTED, r"\text{everything else}")):
            rows.add(VGroup(a, curve(a, ys, col), maths(name, 30, INK).next_to(a, LEFT, buff=0.3)))
        rows.arrange(DOWN, buff=0.45).move_to(DOWN * 0.3).shift(RIGHT * 0.8)
        eq = VGroup(maths("=", 40, INK).move_to((rows[0].get_bottom() + rows[1].get_top()) / 2 + LEFT * 5.6),
                    maths("+", 40, INK).move_to((rows[1].get_bottom() + rows[2].get_top()) / 2 + LEFT * 5.6))
        self.play_at(W("split"), Create(rows[0][0]), Create(rows[0][1]), Write(rows[0][2]), run_time=1.4)
        self.play_at(W("smooth", 1), FadeIn(eq[0]), Create(rows[1][0]), Create(rows[1][1]), Write(rows[1][2]), run_time=1.4)
        self.play_at(W("everything", 1), FadeIn(eq[1]), Create(rows[2][0]), Create(rows[2][1]), Write(rows[2][2]), run_time=1.4)

        # cue 5: rigidity (black box) and the static analogy
        thm = VGroup(label("rigidity theorem (paper, Thm 2.3)", 32, INK),
                     label("ergodic theory and number theory; not shown here", 24, MUTED, italic=True)).arrange(DOWN, buff=0.15)
        thm.to_edge(UP, buff=1.45)
        self.play_at(W("technical"), FadeOut(rows), FadeOut(eq), Write(thm[0]), run_time=1.2)
        self.play_at(W("ergodic"), FadeIn(thm[1]), run_time=0.7)
        an = label("analogy, not the theorem", 26, MUTED, italic=True).next_to(thm, DOWN, buff=0.4)
        self.play_at(W("analogy"), FadeIn(an), run_time=0.6)
        sig_ax = Axes(x_range=[0, 10], y_range=[-1, 1.5], x_length=8, y_length=1.6, tips=False,
                      axis_config={"stroke_color": MUTED, "stroke_width": 1.2, "include_ticks": False}).move_to(DOWN * 0.4)
        sig = sig_ax.plot(lambda x: 0.6 * np.sin(1.1 * x), color=INK, stroke_width=2.5)
        stat_pts = np.random.default_rng(8).normal(0, 0.25, 400)
        noisy = VMobject(stroke_color=MUTED, stroke_width=1.5).set_points_as_corners(
            [sig_ax.c2p(x, 0.6 * np.sin(1.1 * x) + n) for x, n in zip(np.linspace(0, 10, 400), stat_pts)])
        self.play_at(W("signal"), Create(sig_ax), Create(sig), run_time=1.0)
        self.play_at(W("static", 1), Create(noisy), run_time=1.0)
        corr_ax = Axes(x_range=[-5, 5, 1], y_range=[-0.2, 1.1, 1], x_length=6, y_length=1.6, tips=False,
                       axis_config={"stroke_color": MUTED, "stroke_width": 1.2, "include_ticks": False}).move_to(DOWN * 2.6)
        spike = VGroup(corr_ax.plot(lambda x: 0, x_range=[-5, -0.05], color=colour(SKY), stroke_width=3),
                       Line(corr_ax.c2p(0, 0), corr_ax.c2p(0, 1), color=colour(SKY), stroke_width=3),
                       corr_ax.plot(lambda x: 0, x_range=[0.05, 5], color=colour(SKY), stroke_width=3))
        clab = maths(r"\text{correlation of the static with its shifted copy}", 26, MUTED).next_to(corr_ax, UP, buff=0.1)
        self.play_at(W("perfect", 1), Create(corr_ax), FadeIn(clab), run_time=0.8)
        self.play_at(W("zero", 1), Create(spike), run_time=1.2)

        # cue 6: the rule is a correlation; removing static keeps it; pick a genuine colouring
        self.play_at(self.cue(6), FadeOut(VGroup(sig_ax, sig, noisy, corr_ax, spike, clab, an)), run_time=0.7)
        c1 = maths(r"\mathbb{E}\big[\,\mathbf{1}_i(x)\,\mathbf{1}_i(x+u)\,\big] = 0 \qquad (|u| = 1)", 40, INK).move_to(UP * 0.4)
        self.play_at(W("correlation", 2), Write(c1), run_time=1.6)
        c2 = maths(r"\mathbb{E}\big[\,p_i(x)\,p_i(x+u)\,\big] = 0 \qquad p_i = \text{smooth part}", 40, INK).next_to(c1, DOWN, buff=0.5)
        self.play_at(W("removing"), Write(c2), run_time=1.6)
        regions = RegionPlane(seed=21, dim=0.45)
        self.play_at(W("pick"), FadeOut(VGroup(c1, c2, thm)), FadeIn(regions.image), run_time=1.4)
        sch = schematic()
        self.play(FadeIn(sch), run_time=0.4)

        # cue 7: rotations matter; Payne's warning
        rot_icon = VGroup(*[Arc(radius=0.6, start_angle=a, angle=1.6, stroke_color=INK, stroke_width=3).add_tip(tip_length=0.15)
                            for a in (0, PI)]).move_to(LEFT * 4.6 + UP * 1.6)
        rot_l = backed(label("uses every rotation of the plane", 28, INK)).next_to(rot_icon, RIGHT, buff=0.3)
        self.play_at(W("rotational"), FadeIn(rot_icon), FadeIn(rot_l), run_time=0.8)
        pay = backed(label("Payne (2009): without that, a step like this can fail", 26, MUTED, italic=True)).next_to(rot_l, DOWN, aligned_edge=LEFT, buff=0.25)
        self.play_at(W("payne's"), FadeIn(pay), run_time=0.8)

        # cue 8: weak measurable colouring
        self.play_at(self.cue(8), FadeOut(VGroup(rot_icon, rot_l, pay)), run_time=0.5)
        dfn = backed(VGroup(label("weak measurable colouring", 34, INK),
                            maths(r"\text{measurable colour regions, and}\quad \big|\{(x,u) : |u| = 1,\ c(x) = c(x+u)\}\big| = 0", 30, INK)
                            ).arrange(DOWN, buff=0.25), 0.85).to_edge(UP, buff=1.45)
        self.play_at(W("weak"), Write(dfn[1][0]) if False else FadeIn(dfn), run_time=1.2)
        rng = np.random.default_rng(5)
        dust = VGroup(*[Dot([rng.uniform(-6, 6), rng.uniform(-3.2, 1.2), 0], radius=0.025, color=HOT) for _ in range(70)])
        self.play_at(W("negligible"), FadeIn(dust, lag_ratio=0.02), run_time=1.2)

        # cue 9: typical points; exceptions vanish; compactness rebuilds a proper colouring
        p0 = np.array([1.0, -1.0, 0])
        cid = regions.colour_at(p0)
        rings = VGroup(*[Circle(radius=r, stroke_color=INK, stroke_width=2).move_to(p0) for r in (0.9, 0.5, 0.25)])
        typ = backed(label("a typical point: almost all its own colour at every small scale", 26, INK)).next_to(rings, DOWN, buff=0.3)
        self.play_at(W("typical"), LaggedStart(*[Create(r) for r in rings], lag_ratio=0.4), FadeIn(marker(cid, 0.36).move_to(p0)), run_time=1.4)
        self.play(FadeIn(typ), run_time=0.6)
        self.play_at(W("exceptions"), FadeOut(dust), run_time=1.0)
        comp = backed(label("compactness rebuilds a proper colouring", 28, MUTED, italic=True)).next_to(dfn, DOWN, buff=0.3)
        self.play_at(W("compactness"), FadeIn(comp), run_time=0.8)

        # cue 10: the transfer theorem
        thm2 = maths(r"\exists\ \text{proper } k\text{-colouring} \;\iff\; \exists\ \text{weak measurable } k\text{-colouring}", 40, INK)
        thm2_l = label("transfer theorem (paper, Thm 1.3)", 26, MUTED, italic=True).next_to(thm2, UP, buff=0.35)
        self.play_at(W("transfer"), FadeOut(Group(*[m for m in self.mobjects if m is not rail and m is not self.bg])), run_time=0.6)
        self.play(Write(thm2), FadeIn(thm2_l), run_time=1.6)
        every = label("for every number of colours $k$", 30, INK, italic=True).next_to(thm2, DOWN, buff=0.45)
        self.play_at(W("every", after=145), FadeIn(every), run_time=0.8)

        # cue 11: rail advances
        self.play_at(self.cue(11), Transform(rail, mini_rail(3, 3)), run_time=1.0)
        self.finish()


class S5_2(NarratedScene):
    """Palettes (paper §5): sixty-degree exclusion, at most two colours, alternation."""
    scene_id = "s5_2"

    def construct(self):
        W = self.word
        rail = mini_rail(3, 4)
        self.add(rail)
        regions = RegionPlane(seed=33, dim=0.38)
        X = DOWN * 0.45 + LEFT * 2.2
        self.play_at(self.cue(1), FadeIn(regions.image), FadeIn(schematic()), run_time=1.0)
        xdot = marker(None, 0.34).move_to(X)
        xl = backed(maths("x", 34, INK)).next_to(xdot, DL, buff=0.05)
        self.play_at(W("stand"), FadeIn(xdot), FadeIn(xl), run_time=0.6)
        ring = Circle(radius=S, stroke_color=INK, stroke_width=2.5).move_to(X)
        self.play_at(W("circle"), Create(ring), run_time=1.0)

        # cue 2: read the colours on the ring, direction by direction
        n = 180
        segs = VGroup()
        for k in range(n):
            th = TAU * k / n
            p = X + S * np.array([np.cos(th), np.sin(th), 0])
            segs.add(AnnularSector(inner_radius=S - 0.09, outer_radius=S + 0.09, start_angle=th, angle=TAU / n * 1.05,
                                   fill_color=PAL[regions.colour_at(p)], fill_opacity=1, stroke_width=0).shift(X))
        e = ValueTracker(0.0)
        arrow = always_redraw(lambda: Arrow(X, X + (S - 0.15) * np.array([np.cos(e.get_value()), np.sin(e.get_value()), 0]), buff=0.1,
                                            color=INK, stroke_width=3, max_tip_length_to_length_ratio=0.08))
        self.play_at(W("each"), FadeIn(arrow), run_time=0.4)
        self.play(e.animate.set_value(TAU), ShowIncreasingSubsets(segs), run_time=W("ring", 1) + 0.6 - self.now, rate_func=linear)
        pal = backed(maths(r"\text{palette } P_x(e) = \text{colours seen at } x + e", 32, INK)).to_corner(UR, buff=0.6).shift(DOWN * 0.7)
        self.play_at(W("palette", 1), Write(pal), run_time=1.2)
        lim = backed(label("(defined through limits, to handle messy boundaries)", 24, MUTED, italic=True)).next_to(pal, DOWN, buff=0.2)
        self.play_at(W("technically"), FadeIn(lim), run_time=0.6)

        # cue 3: the diamond inside the ring
        f = PI / 6
        dirn = lambda a: np.array([np.cos(a), np.sin(a), 0])
        R60 = PI / 3
        A, B, F = X + S * dirn(f + R60), X + S * dirn(f - R60), X + S * dirn(f)
        dia = VGroup(*[Line(p, q, stroke_color=INK, stroke_width=3.2) for p, q in ((X, A), (X, B), (A, F), (B, F))])
        dmarks = VGroup(*[marker(None, 0.3).move_to(p) for p in (A, B, F)])
        self.play_at(W("diamond", 1), FadeOut(arrow), segs.animate.set_opacity(0.45), FadeOut(lim), Create(dia), FadeIn(dmarks), run_time=1.2)
        lbl = VGroup(backed(maths("f", 30, INK)).next_to(F, RIGHT, buff=0.15), backed(maths("Rf", 30, INK)).next_to(A, UP, buff=0.12),
                     backed(maths("R^{-1}f", 30, INK)).next_to(B, DOWN, buff=0.12))
        self.play_at(W("60", 1), FadeIn(lbl), run_time=0.7)
        hl = VGroup(Line(F, A, stroke_color=colour(SKY), stroke_width=6), Line(F, B, stroke_color=colour(SKY), stroke_width=6))
        self.play_at(self.wc(3, "exactly"), Create(hl), run_time=0.9)
        sumf = backed(VGroup(maths(r"x + f = x + Rf + R^{-1}f", 34, INK),
                             label("$R$ = rotation by $60^\\circ$", 24, MUTED, italic=True)).arrange(DOWN, buff=0.12)).next_to(pal, DOWN, buff=0.35)
        self.play_at(W("diamond", 2), Write(sumf), run_time=1.4)

        # cue 4: sixty-degree exclusion
        ex = backed(maths(r"P_x(f) \cap P_x(Rf) = \varnothing", 40, INK)).next_to(sumf, DOWN, buff=0.4)
        self.play_at(W("directions", 2), Write(ex), run_time=1.2)
        cor = label("paper, Cor. 5.4", 22, MUTED, italic=True).next_to(ex, DOWN, buff=0.1)
        self.play(FadeIn(cor), run_time=0.4)

        # cue 5: at most two colours
        two = backed(maths(r"|P_x(e)| \le 2 \quad \text{for almost every } e", 40, INK)).next_to(cor, DOWN, buff=0.4)
        self.play_at(W("stronger"), FadeOut(VGroup(dia, dmarks, lbl, hl)), Write(two), run_time=1.4)

        # cue 6: why: binary centres are separated, yet would pile up on a circle
        self.play_at(self.cue(6), FadeOut(VGroup(pal, sumf, ex, cor, two)), run_time=0.6)
        e0 = 0.9
        Y = X + S * dirn(e0)
        small = VGroup(*[AnnularSector(inner_radius=0.55, outer_radius=0.68, start_angle=k * R60, angle=R60,
                                       fill_color=PAL[[YELLOW, BLUE][k % 2]], fill_opacity=0.95, stroke_width=0).shift(Y) for k in range(6)])
        self.play_at(W("crowded"), FadeIn(marker(None, 0.3).move_to(Y)), run_time=0.5)
        self.play_at(W("ring", after=66), FadeIn(small), run_time=0.8)
        note = backed(label("a two-colour centre", 26, INK)).next_to(small, RIGHT, buff=0.25)
        self.play_at(W("other", 1), FadeIn(note), run_time=0.6)
        sep = backed(maths(r"\text{two-colour centres for the same pair are} \ge \delta_* \text{ apart}", 30, INK)).to_edge(DOWN, buff=0.5)
        self.play_at(W("fixed"), Write(sep), run_time=1.4)
        crowd = VGroup(*[marker(None, 0.22).move_to(X + S * dirn(e0 + 0.06 * j)) for j in range(-6, 7) if j])
        self.play_at(W("pack"), LaggedStart(*[FadeIn(c, scale=0.5) for c in crowd], lag_ratio=0.08), run_time=1.2)
        clash_pair = burning(X + S * dirn(e0), X + S * dirn(e0 + 0.06), w=4)
        self.play(FadeIn(clash_pair), run_time=0.5)

        # cue 7: alternation in six petals
        self.play_at(self.cue(7), FadeOut(VGroup(small, note, sep, crowd, clash_pair)), FadeOut(segs),
                     *[FadeOut(m) for m in self.mobjects if isinstance(m, VGroup) and m is not rail and m is not ring and m is not xdot
                       and m is not xl and m is not self.bg], run_time=0.8)
        petals = VGroup(*[AnnularSector(inner_radius=S - 0.12, outer_radius=S + 0.12, start_angle=k * R60 + 0.2, angle=R60,
                                        fill_color=PAL[[ORANGE, SKY][k % 2]], fill_opacity=1, stroke_width=0).shift(X) for k in range(6)])
        self.play_at(W("swap"), LaggedStart(*[FadeIn(p) for p in petals], lag_ratio=0.25), run_time=1.6)
        six = backed(label("six petals, alternating", 32, INK)).next_to(ring, RIGHT, buff=0.6)
        self.play_at(W("six"), Write(six), run_time=1.0)
        self.finish()


# ======================================================================================================
from components.widgets import BoundsLine
from scenes.ch3 import mini_spindle

FIVE = (ORANGE, SKY, GREEN, YELLOW, BLUE)


def k5(center, radius=1.6, size=0.4):
    """The five colours as a pentagon with all ten edges (the 'network' K5)."""
    pts = [center + radius * np.array([np.cos(PI / 2 + k * TAU / 5), np.sin(PI / 2 + k * TAU / 5), 0]) for k in range(5)]
    edges = VGroup(*[Line(pts[i], pts[j], stroke_color=MUTED, stroke_width=2) for i in range(5) for j in range(i + 1, 5)])
    verts = VGroup(*[marker(FIVE[k], size).move_to(pts[k]) for k in range(5)])
    return VGroup(edges, verts), pts


def thread_curve(origin, base, length, S, seed, wiggle=0.35):
    rng = np.random.default_rng(seed)
    a1, a2, f1 = rng.uniform(0.15, 0.35), rng.uniform(0.05, 0.15), rng.uniform(2, 4)
    ts = np.linspace(0, 1, 120)
    pts = [origin + S * (t * length) * np.array([np.cos(base + wiggle * (a1 * np.sin(f1 * t * 3) + a2 * np.sin(9 * t))),
                                                 np.sin(base + wiggle * (a1 * np.sin(f1 * t * 3) + a2 * np.sin(9 * t))), 0]) for t in ts]
    return pts


def two_tone(pts, c1, c2, width=5):
    """A thread where colours c1 and c2 meet half and half: drawn as two parallel strokes."""
    a = VMobject(stroke_color=PAL[c1], stroke_width=width).set_points_smoothly(pts)
    b = VMobject(stroke_color=PAL[c2], stroke_width=width).set_points_smoothly([p + np.array([0.035, -0.035, 0]) for p in pts])
    return VGroup(a, b)


class S5_3(NarratedScene):
    """Blur, loop, threads (paper §§6–7, Lemma 7.5, Prop. 7.1, Fig. 2)."""
    scene_id = "s5_3"

    def construct(self):
        W = self.word
        rail = mini_rail(4, 5)
        self.add(rail)
        q = maths(r"\text{find a special point}", 40, INK)
        self.play_at(W("special", 1), Write(q), run_time=1.0)
        topo = label("(topology)", 28, MUTED, italic=True).next_to(q, DOWN, buff=0.3)
        self.play_at(W("topology"), FadeIn(topo), run_time=0.6)

        # cue 2: blur; a recipe at every point
        regions = RegionPlane(seed=44, dim=0.42)
        self.play_at(W("first"), FadeOut(VGroup(q, topo)), FadeIn(regions.image), FadeIn(schematic()), run_time=0.8)
        soft = blurred_field(seed=44, blob=0.45, dim=0.42)
        self.play_at(W("blur"), FadeIn(soft), run_time=1.6)
        p0 = LEFT * 3.0 + DOWN * 0.6
        disk = Circle(radius=0.45, stroke_color=INK, stroke_width=2.5).move_to(p0)
        self.play_at(W("tiny"), Create(disk), run_time=0.7)
        rec = backed(maths(r"60\%\ \text{orange},\ \ 40\%\ \text{blue}", 34, INK)).next_to(disk, UP, buff=0.3)
        self.play_at(W("recipe"), Write(rec), run_time=1.0)

        # cue 3: the K5 network
        net, P = k5(RIGHT * 4.0 + DOWN * 0.4, radius=1.7)
        self.play_at(W("draw"), FadeIn(net[1], lag_ratio=0.2), run_time=1.0)
        self.play_at(W("join"), Create(net[0], lag_ratio=0.08), run_time=1.2)
        tracer = Dot(P[0], radius=0.09, color=INK)
        self.play_at(W("pure"), FadeIn(tracer, scale=2), Indicate(net[1][0], color=INK, scale_factor=1.4), run_time=0.8)
        self.play_at(W("mixing"), tracer.animate.move_to(0.6 * P[0] + 0.4 * P[1]), run_time=1.2)

        # cue 4: at most two colours mixed; continuous map onto the network
        two = backed(maths(r"\text{at most two colours mixed}\ \ (\text{away from tiny holes and a few special points})", 28, INK)).to_edge(DOWN, buff=0.4)
        self.play_at(W("no", 1), Write(two), run_time=1.6)
        arrows = VGroup()
        rng = np.random.default_rng(2)
        for _ in range(5):
            s = np.array([rng.uniform(-6, 0.5), rng.uniform(-2.6, 2.2), 0])
            k = int(rng.integers(5)); j = (k + 1 + int(rng.integers(4))) % 5; t = rng.uniform(0.2, 0.8)
            arrows.add(CurvedArrow(s, (1 - t) * P[k] + t * P[j], angle=-0.4, color=MUTED, stroke_width=1.5, tip_length=0.15))
        self.play_at(W("maps"), LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.15), run_time=1.4)

        # cue 5: tiles meet in threes
        self.play_at(self.cue(5), FadeOut(Group(regions.image, soft, disk, rec, two, arrows, tracer, net)), run_time=0.8)
        fact = label("a fact about flat space", 30, MUTED, italic=True).to_edge(UP, buff=1.2)
        self.play_at(W("fact"), FadeIn(fact), run_time=0.6)
        sq = VGroup(*[Square(0.9).set_stroke(EDGE, 2).move_to([x, y, 0]) for x in np.arange(-6.3, -1.2, 0.9) for y in np.arange(-2.2, 1.4, 0.9)])
        hx = VGroup(*[RegularPolygon(6, radius=0.5, start_angle=PI / 2).set_stroke(EDGE, 2).move_to([1.2 + 0.866 * (q2 + r2 / 2), -0.6 + 0.75 * r2, 0])
                      for q2 in range(-1, 5) for r2 in range(-2, 3)])
        self.play_at(W("cover"), Create(sq), run_time=1.4)
        corners = VGroup(*[Dot([x, y, 0], radius=0.07, color=colour(ORANGE)) for x in np.arange(-5.85, -1.6, 0.9) for y in np.arange(-1.75, 1.0, 0.9)])
        self.play_at(W("four", 1), FadeIn(corners, lag_ratio=0.02), run_time=0.8)
        self.play_at(W("hexagons"), Create(hx), run_time=1.0)
        tri = VGroup(*[Dot(v, radius=0.07, color=colour(SKY)) for h in hx for v in h.get_vertices()[::2]])
        self.play(FadeIn(tri, lag_ratio=0.01), run_time=0.7)
        threes = maths(r"\text{in 2D, small pieces covering a region must meet in threes somewhere}", 30, INK).to_edge(DOWN, buff=0.7)
        self.play_at(W("dimensions"), Write(threes), run_time=1.6)

        # cue 6: the precise version (paper, Lemma 7.5)
        self.play_at(self.cue(6), FadeOut(VGroup(sq, hx, corners, tri, threes, fact)), run_time=0.7)
        prec = VGroup(maths(r"\text{colour regions of the blurred map: diameter} \lesssim 1", 34, INK),
                      maths(r"\text{at most two overlap at any point}", 34, INK),
                      maths(r"\Longrightarrow\ \text{impossible on a large square}", 34, INK)).arrange(DOWN, buff=0.35)
        ref = label("paper, Lemma 7.5", 24, MUTED, italic=True).next_to(prec, DOWN, buff=0.35)
        self.play_at(self.wc(6, "region"), Write(prec[0]), run_time=1.4)
        self.play_at(W("overlap"), Write(prec[1]), run_time=1.0)
        self.play_at(W("impossible"), Write(prec[2]), FadeIn(ref), run_time=1.0)

        # cue 7: the special point and a loop that winds around a cycle of colours
        self.play_at(self.cue(7), FadeOut(VGroup(prec, ref)), FadeIn(soft), run_time=0.8)
        X = LEFT * 3.0 + DOWN * 0.3
        sp = marker(None, 0.36).move_to(X)
        self.play_at(self.wc(7, "special"), FadeIn(sp, scale=1.6), run_time=0.6)
        net, P = k5(RIGHT * 4.0 + DOWN * 0.3, radius=1.7)
        self.play(FadeIn(net), run_time=0.6)
        loop = Circle(radius=0.8, stroke_color=INK, stroke_width=2.5).move_to(X)
        cyc = [0, 1, 2, 0]
        path = VMobject(stroke_color=INK, stroke_width=4).set_points_as_corners([P[i] for i in cyc])
        walker = Dot(X + RIGHT * 0.8, radius=0.08, color=INK)
        tr = Dot(P[0], radius=0.1, color=INK)
        self.play_at(W("walk"), Create(loop), FadeIn(walker), FadeIn(tr), run_time=0.8)
        self.play(MoveAlongPath(walker, loop), MoveAlongPath(tr, path), Create(path), run_time=W("network", after=100) + 0.5 - self.now, rate_func=linear)
        c4 = VMobject(stroke_color=MUTED, stroke_width=2.5).set_points_as_corners([P[i] for i in (0, 1, 3, 2, 0)])
        c5 = VMobject(stroke_color=MUTED, stroke_width=2.5).set_points_as_corners([P[i] for i in (0, 2, 4, 1, 3, 0)])
        lens = VGroup(maths("3", 36, INK), maths("4", 36, MUTED), maths("5", 36, MUTED)).arrange(RIGHT, buff=0.6).next_to(net, DOWN, buff=0.4)
        self.play_at(self.wc(7, "three"), FadeIn(lens[0]), run_time=0.4)
        self.play_at(self.wc(7, "four"), FadeIn(lens[1]), Create(c4), run_time=0.5)
        self.play_at(self.wc(7, "five"), FadeIn(lens[2]), Create(c5), run_time=0.5)

        # cue 8: threads
        self.play_at(self.cue(8), FadeOut(VGroup(c4, c5, loop, walker)), run_time=0.5)
        pairs = [(ORANGE, SKY), (SKY, GREEN), (GREEN, ORANGE)]
        threads = VGroup(*[two_tone(thread_curve(X, b, 1.5, S * 0.9, seed=k), *pairs[k]) for k, b in enumerate((0.4, 2.5, 4.4))])
        self.play_at(W("trace"), LaggedStart(*[Create(t) for t in threads], lag_ratio=0.3), run_time=1.8)
        half = backed(label("along a thread, two colours meet half and half", 26, INK)).to_edge(DOWN, buff=0.5)
        self.play_at(W("half"), FadeIn(half), run_time=0.6)

        # cue 9: the straddle zone (paper Fig. 2), computed for a drawn thread
        self.play_at(self.cue(9), FadeOut(Group(soft, sp, threads, half, net, path, tr, lens)), run_time=0.7)
        Sz = 1.7
        X2 = LEFT * 2.8 + DOWN * 1.6
        kp = thread_curve(X2, 0.75, 1.15, Sz, seed=7, wiggle=0.5)
        K = VMobject(stroke_color=PAL[ORANGE], stroke_width=5).set_points_smoothly(kp)
        Kl = maths("K", 34, PAL[ORANGE]).next_to(kp[70], UL, buff=0.1)
        self.play_at(W("threads", 1), Create(K), FadeIn(Kl), FadeIn(marker(None, 0.3).move_to(X2)), run_time=1.0)
        kpts = np.array(kp)
        # z: a point with min distance < 1 < max distance to K (world units)
        z = X2 + Sz * np.array([1.55, 0.05, 0])
        d = np.linalg.norm(kpts - z, axis=1) / Sz
        assert d.min() < 1 < d.max()
        iq, ix, ip = int(np.argmin(d)), int(np.argmax(d)), int(np.argmin(np.abs(d - 1)))
        zd = marker(None, 0.3).move_to(z)
        zl = maths("z", 34, INK).next_to(z, RIGHT, buff=0.15)
        self.play_at(self.wc(9, "point"), FadeIn(zd), FadeIn(zl), run_time=0.5)
        near = DashedLine(z, kpts[iq], stroke_color=INK, stroke_width=2)
        nl = maths(r"< 1", 30, INK).next_to(near, UP, buff=0.05)
        self.play_at(self.wc(9, "less"), Create(near), FadeIn(nl), run_time=0.7)
        far = DashedLine(z, kpts[ix], stroke_color=INK, stroke_width=2)
        fl = maths(r"> 1", 30, INK).next_to(far.get_center(), DOWN, buff=0.1)
        self.play_at(self.wc(9, "more"), Create(far), FadeIn(fl), run_time=0.7)
        circ = Circle(radius=Sz, stroke_color=MUTED, stroke_width=2).move_to(z)
        exact = Line(z, kpts[ip], stroke_color=colour(SKY), stroke_width=4)
        el = maths("1", 30, colour(SKY)).next_to(exact.get_center(), LEFT, buff=0.1)
        self.play_at(self.wc(9, "connected"), Create(circ), run_time=1.0)
        self.play_at(W("exactly"), Create(exact), FadeIn(el), FadeIn(marker(None, 0.26).move_to(kpts[ip])), run_time=0.8)
        # shade the straddle region Δ(K) = {z : min|z-q| < 1 < max|z-q|}
        res = 0.05
        gx, gy = np.meshgrid(np.arange(-7.1, 7.1, res), np.arange(4.0, -4.0, -res))
        G = np.stack([gx, gy], -1)
        dmin = np.full(gx.shape, np.inf); dmax = np.zeros(gx.shape)
        for q2 in kpts[::3]:
            dd = np.hypot(G[..., 0] - q2[0], G[..., 1] - q2[1]) / Sz
            dmin = np.minimum(dmin, dd); dmax = np.maximum(dmax, dd)
        mask = (dmin < 1) & (dmax > 1)
        rgba = np.zeros(gx.shape + (4,), np.uint8)
        rgba[mask] = [255, 90, 60, 60]
        shade = ImageMobject(rgba).stretch_to_fit_width(gx.shape[1] * res).stretch_to_fit_height(gx.shape[0] * res).move_to([0, 0.05, 0])
        shade.set_z_index(-10)
        ban = backed(maths(r"\Delta(K) = \{\,z : \min_{q \in K}|z-q| < 1 < \max_{q \in K}|z-q|\,\}", 32, INK)).to_corner(UR, buff=0.6).shift(DOWN * 0.6)
        ban2 = backed(label("both colours of the thread are excluded here (paper, Prop. 7.1)", 24, MUTED, italic=True)).next_to(ban, DOWN, buff=0.2)
        self.play_at(W("excludes"), FadeIn(shade), Write(ban), run_time=1.4)
        self.play(FadeIn(ban2), run_time=0.5)

        # cue 10: summary picture
        self.play_at(self.cue(10), FadeOut(Group(shade, K, Kl, zd, zl, near, nl, far, fl, circ, exact, el, ban, ban2,
                                                  *[m for m in self.mobjects if isinstance(m, VGroup) and len(m) == 2 and m is not rail])), run_time=0.8)
        X3 = DOWN * 0.3
        uc = Circle(radius=S, stroke_color=INK, stroke_width=2).move_to(X3)
        th3 = VGroup(*[two_tone(thread_curve(X3, b, 0.5, S, seed=10 + k), *pairs[k], width=4) for k, b in enumerate((0.5, 2.6, 4.3))])
        bands = VGroup(*[AnnularSector(inner_radius=S - 0.22, outer_radius=S + 0.22, start_angle=a, angle=0.9, fill_color=SOFT,
                                       fill_opacity=0.35, stroke_width=0).shift(X3) for a in np.arange(0, TAU, 1.05)])
        self.play_at(self.wc(10, "special"), FadeIn(marker(None, 0.34).move_to(X3)), Create(uc), run_time=0.8)
        self.play_at(self.wc(10, "three"), LaggedStart(*[Create(t) for t in th3], lag_ratio=0.3), run_time=1.4)
        self.play_at(W("banning"), FadeIn(bands, lag_ratio=0.1), run_time=1.4)
        bl = backed(label("each thread bans its two colours just inside and outside the unit circle", 26, INK)).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(bl), run_time=0.6)

        # cue 11
        cases = backed(maths(r"3,\ 4 \text{ or } 5 \text{ threads: each case must fail}", 38, INK)).to_corner(UR, buff=0.6).shift(DOWN * 0.7)
        self.play_at(self.cue(11), Write(cases), run_time=1.2)
        self.finish()


def hex_slots(center, r=1.6, size=0.5):
    pts = [center + r * np.array([np.cos(PI / 2 - j * PI / 3), np.sin(PI / 2 - j * PI / 3), 0]) for j in range(6)]
    ring = VGroup(*[Line(pts[j], pts[(j + 1) % 6], stroke_color=MUTED, stroke_width=2) for j in range(6)])
    slots = VGroup(*[Circle(radius=size / 2, stroke_color=INK, stroke_width=2).set_fill(BG, 1).move_to(p) for p in pts])
    return VGroup(ring, slots), pts


# Moser spindle placement from the paper (eq. 8.x / Lemma 8.9): z_g = (35+12i)/37 * (g + (-290+149i)/250)
_A, _B, _T = (np.sqrt(3) + 1j) / 2, (np.sqrt(3) - 1j) / 2, np.sqrt(3) + 0j
_U = (5 + 1j * np.sqrt(11)) / 6
MOSER = {"0": 0j, "A": _A, "B": _B, "T": _T, "uA": _U * _A, "uB": _U * _B, "uT": _U * _T}
MOSER_E = [("0", "A"), ("0", "B"), ("A", "B"), ("A", "T"), ("B", "T"), ("0", "uA"), ("0", "uB"), ("uA", "uB"),
           ("uA", "uT"), ("uB", "uT"), ("T", "uT")]
PLACE = {k: (35 + 12j) / 37 * (g + (-290 + 149j) / 250) for k, g in MOSER.items()}


def in_three_region(z):
    xi, up = z.real, z.imag
    l = xi * xi + up * up
    P = up * up * (3 * xi * xi - up * up) ** 2
    Pp = l ** 3 * (1 - l / 4) * (l - 1) ** 2
    return 0 < l < 4 and P < Pp


class S5_4(NarratedScene):
    """The three cases (paper §8): five threads (Prop 8.2), four (Prop 8.5), three (Prop 8.10, Lemmas 8.8–8.9)."""
    scene_id = "s5_4"

    def construct(self):
        W = self.word
        rail = mini_rail(5, 6)
        self.add(rail)

        # ---------------- five threads ----------------
        head = label("five threads", 34, INK).to_corner(UL, buff=0.5).shift(DOWN * 0.7)
        self.play_at(self.cue(1), FadeIn(head), run_time=0.6)
        net, P = k5(LEFT * 4.2 + DOWN * 0.4, radius=1.5, size=0.38)
        self.play_at(W("direction", 1), FadeIn(net[1]), run_time=0.7)
        diag = VGroup(*[Line(P[i], P[(i + 2) % 5], stroke_color=INK, stroke_width=3) for i in range(5)])
        self.play_at(W("diagonal"), Create(diag, lag_ratio=0.2), run_time=1.4)
        dlab = backed(maths(r"D_i = \{\,i,\ i+2\,\} \pmod 5", 34, INK)).next_to(net, DOWN, buff=0.4)
        self.play_at(W("two", 1), Write(dlab), run_time=1.0)
        clock_c = RIGHT * 3.6 + UP * 0.9
        clock = VGroup(Circle(radius=1.0, stroke_color=INK, stroke_width=2.5).move_to(clock_c),
                       *[maths(str(k), 30, INK).move_to(clock_c + 1.3 * np.array([np.sin(k * TAU / 5), np.cos(k * TAU / 5), 0])) for k in range(5)])
        hand_t = ValueTracker(0)
        hand = always_redraw(lambda: Arrow(clock_c, clock_c + 0.85 * np.array([np.sin(hand_t.get_value() * TAU / 5), np.cos(hand_t.get_value() * TAU / 5), 0]),
                                           buff=0, color=colour(ORANGE), stroke_width=4, max_tip_length_to_length_ratio=0.25))
        self.play_at(W("label"), FadeIn(clock), FadeIn(hand), run_time=1.0)

        # cue 2: six steps of sixty degrees; steps of +-1; the walk must close
        slots, sp = hex_slots(LEFT * 3.6 + DOWN * 0.5, r=1.35, size=0.6)
        self.play_at(W("walk"), FadeOut(VGroup(net, diag, dlab)), FadeIn(slots), run_time=1.0)
        seq = [0, 1, 2, 1, 2, 1]                  # every step is +-1 and the walk closes (sum 0), as a candidate
        assert all((seq[(j + 1) % 6] - seq[j]) % 5 in (1, 4) for j in range(6))
        vals = VGroup(*[maths(str(v), 30, INK).move_to(sp[j]).set_z_index(6) for j, v in enumerate(seq)])
        col = RIGHT * 3.2
        step_rule = VGroup(maths(r"\text{neighbouring palettes disjoint}", 28, INK),
                           maths(r"\iff \text{labels differ by } \pm 1", 28, INK)).arrange(DOWN, buff=0.15).move_to(col + DOWN * 1.25)
        self.play_at(W("disjoint", 1), Write(step_rule), run_time=1.2)
        for j, t in enumerate(np.linspace(W("each", 1), W("one", after=33) + 0.3, 6)):
            self.until(t)
            self.play(FadeIn(vals[j], scale=1.4), hand_t.animate.set_value(seq[j]), run_time=0.35)
        close = maths(r"\varepsilon_1 + \cdots + \varepsilon_6 \equiv 0 \pmod 5, \quad \varepsilon_j = \pm 1", 30, INK).move_to(col + DOWN * 2.45)
        self.play_at(W("after"), Write(close), run_time=1.4)

        # cue 3: opposite directions differ by 0 or +-2; three steps sum to +-1 or +-3
        chords = VGroup(*[DashedLine(sp[j], sp[j + 3], stroke_color=MUTED, stroke_width=2) for j in range(3)]).set_z_index(-1)
        opp = maths(r"p_{j+3} - p_j \in \{0, \pm 2\} \pmod 5", 32, INK).move_to(col + UP * 1.4)
        self.play_at(W("opposite"), FadeOut(clock), FadeOut(hand), FadeOut(VGroup(step_rule, close)), Create(chords), Write(opp), run_time=1.4)
        bad = burning(sp[0], sp[3], w=4)
        self.play(FadeIn(bad), run_time=0.5)
        trows = VGroup(*[maths(t, 30, INK) for t in (r"+1+1+1 = +3 \equiv -2\ \checkmark", r"+1+1-1 = +1\ \times",
                                                     r"+1-1-1 = -1\ \times", r"-1-1-1 = -3 \equiv +2\ \checkmark")]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        trows.next_to(opp, DOWN, buff=0.45)
        self.play_at(W("three", 2), Write(trows[0]), run_time=1.0)
        for k, t in enumerate((W("one", after=53), W("minus", after=54), W("minus", after=55.3))):
            self.play_at(t, Write(trows[k + 1]), run_time=0.7)
        same = label("every run of three steps goes the same way", 26, INK, italic=True).next_to(trows, DOWN, buff=0.35)
        self.play_at(W("only"), FadeIn(same), run_time=0.8)

        # cue 4: all six steps equal: +-6, not a multiple of 5
        six = maths(r"\varepsilon_1 = \cdots = \varepsilon_6 \;\Rightarrow\; \textstyle\sum \varepsilon_j = \pm 6 \not\equiv 0 \pmod 5", 32, INK).move_to(RIGHT * 0.6 + DOWN * 3.15)
        self.play_at(W("all", 2), Write(six), run_time=1.6)

        # cue 5: contradiction
        bot = maths(r"\bot", 60, HOT).next_to(slots, LEFT, buff=0.4)
        self.play_at(W("contradiction", 1), FadeIn(bot, scale=1.5), run_time=0.6)
        done5 = backed(maths(r"5 \text{ threads: impossible}", 34, INK)).next_to(head, DOWN, aligned_edge=LEFT, buff=0.25)
        own = label("the paper's own argument (Prop. 8.2)", 22, MUTED, italic=True).next_to(done5, DOWN, aligned_edge=LEFT, buff=0.12)
        self.play_at(self.wc(5, "threads"), Write(done5), run_time=0.8)
        self.play_at(W("paper's"), FadeIn(own), run_time=0.6)

        # ---------------- four threads ----------------
        self.play_at(self.cue(6), FadeOut(VGroup(slots, vals, chords, bad, opp, trows, same, six, bot, head, own)),
                     done5.animate.scale(0.75).to_corner(UL, buff=0.5).shift(DOWN * 0.8), run_time=0.8)
        head4 = label("four threads", 34, INK).to_edge(UP, buff=1.2)
        self.play(FadeIn(head4), run_time=0.5)
        st_lab = backed(maths(r"\text{palette} \in \{\,X,\ U = \{0,2\},\ V = \{1,3\}\,\}", 30, INK)).next_to(head4, DOWN, buff=0.3)
        self.play_at(W("each", after=89), Write(st_lab), run_time=1.4)
        slots4, sp4 = hex_slots(LEFT * 2.6 + DOWN * 0.9, r=1.4, size=0.6)
        word = ["X", "U", "X", "V", "X", "U"]
        wv = VGroup(*[maths(c, 30, INK).move_to(sp4[j]) for j, c in enumerate(word)])
        self.play_at(W("following"), FadeIn(slots4), FadeIn(wv, lag_ratio=0.15), run_time=1.2)
        ev = VGroup(*[Circle(radius=0.36, stroke_color=colour(ORANGE), stroke_width=3).move_to(sp4[j]) for j in (0, 2, 4)])
        self.play_at(W("even"), Create(ev), run_time=0.8)
        lamp = VGroup(Circle(radius=0.3, stroke_color=INK, stroke_width=2.5).set_fill(colour(ORANGE), 0.9),
                      maths(r"\text{parity: even}", 32, INK)).arrange(RIGHT, buff=0.3).move_to(RIGHT * 3.0 + DOWN * 0.6)
        self.play_at(W("parity", 1), FadeIn(lamp), run_time=0.8)

        # cue 7: can't change slowly, but a 60-degree turn flips it
        skip = label("geometric lemmas skipped (paper, Lemmas 8.3--8.4)", 24, MUTED, italic=True).next_to(lamp, DOWN, buff=0.4)
        self.play_at(W("geometric"), FadeIn(skip), run_time=0.6)
        self.play_at(self.wc(7, "turn"), Rotate(VGroup(slots4, wv, ev), angle=-0.35, about_point=LEFT * 2.6 + DOWN * 0.9), run_time=1.2)
        self.play(Rotate(VGroup(slots4, wv, ev), angle=0.35, about_point=LEFT * 2.6 + DOWN * 0.9), run_time=0.8)
        word2 = word[1:] + word[:1]
        wv2 = VGroup(*[maths(c, 30, INK).move_to(sp4[j]) for j, c in enumerate(word2)])
        ev2 = VGroup(*[Circle(radius=0.36, stroke_color=colour(SKY), stroke_width=3).move_to(sp4[j]) for j in (1, 3, 5)])
        lamp2 = VGroup(Circle(radius=0.3, stroke_color=INK, stroke_width=2.5).set_fill(colour(SKY), 0.9),
                       maths(r"\text{parity: odd}", 32, INK)).arrange(RIGHT, buff=0.3).move_to(lamp)
        self.play_at(self.wc(7, "exactly"), Transform(wv, wv2), Transform(ev, ev2), Transform(lamp, lamp2), run_time=1.2)
        bot4 = maths(r"\bot", 64, HOT).next_to(lamp, RIGHT, buff=0.5)
        self.play_at(W("contradiction", 2), FadeIn(bot4, scale=1.5), run_time=0.6)
        done4 = backed(maths(r"4 \text{ threads: impossible}", 34 * 0.75, INK)).next_to(done5, DOWN, aligned_edge=LEFT, buff=0.15)
        self.play(Write(done4), run_time=0.7)

        # ---------------- three threads ----------------
        self.play_at(self.cue(8), FadeOut(VGroup(head4, st_lab, slots4, wv, ev, lamp, skip, bot4)), run_time=0.7)
        head3 = label("three threads", 34, INK).to_edge(UP, buff=1.2)
        tri_c = VGroup(*[marker(c, 0.4) for c in (ORANGE, SKY, GREEN)]).arrange(RIGHT, buff=0.3)
        left_c = VGroup(*[marker(c, 0.4) for c in (YELLOW, BLUE)]).arrange(RIGHT, buff=0.3)
        leg = VGroup(VGroup(tri_c, label("triangle colours", 26, INK)).arrange(RIGHT, buff=0.3),
                     VGroup(left_c, label("leftovers", 26, INK)).arrange(RIGHT, buff=0.3)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        leg.to_corner(UR, buff=0.5).shift(DOWN * 0.8)
        self.play_at(W("three", after=127), FadeIn(head3), run_time=0.6)
        self.play_at(W("triangle", 1), FadeIn(leg[0]), run_time=0.7)
        self.play_at(W("left"), FadeIn(leg[1]), run_time=0.7)

        # cue 9: leftovers alternate in six exact 60-degree sectors (sign of sin 3θ)
        Sx = 1.55
        X = DOWN * 0.55 + LEFT * 0.6
        uc = Circle(radius=Sx, stroke_color=INK, stroke_width=2).move_to(X)
        self.play_at(W("near"), FadeOut(head3), FadeIn(marker(None, 0.32).move_to(X)), Create(uc), run_time=0.8)
        outs = lambda th: YELLOW if np.sin(3 * th) > 0 else BLUE
        strips = VGroup(*[AnnularSector(inner_radius=Sx - 0.13, outer_radius=Sx + 0.13, start_angle=k * PI / 3, angle=PI / 3,
                                        fill_color=PAL[outs(k * PI / 3 + 0.1)], fill_opacity=0.9, stroke_width=0).shift(X) for k in range(6)])
        self.play_at(W("ban"), FadeIn(strips, lag_ratio=0.2), run_time=1.6)
        flower = backed(label("six sectors of exactly $60^\\circ$, alternating", 26, INK)).next_to(uc, DOWN, buff=0.3)
        self.play_at(W("alternate"), FadeIn(flower), run_time=0.8)

        # cue 10: a point z reached by two unit steps landing in different leftover sectors
        zc = PLACE["B"]                                   # a point of the region (a vertex of the placed spindle)
        z = complex(0.18, 0.52)
        assert in_three_region(z)
        r, phi = abs(z), np.angle(z)
        dlt = np.arccos(r / 2)
        e1, e2 = np.exp(1j * (phi - dlt)), np.exp(1j * (phi + dlt))
        assert outs(np.angle(e1)) != outs(np.angle(e2))
        to = lambda w: X + Sx * np.array([w.real, w.imag, 0])
        zm = marker(None, 0.28).move_to(to(z))
        steps = VGroup(Line(to(0), to(e1), stroke_color=INK, stroke_width=2.5), Line(to(0), to(e2), stroke_color=INK, stroke_width=2.5),
                       Line(to(e1), to(z), stroke_color=INK, stroke_width=2.5), Line(to(e2), to(z), stroke_color=INK, stroke_width=2.5))
        self.play_at(self.wc(10, "point"), FadeOut(flower), FadeIn(zm), run_time=0.5)
        self.play_at(W("sum"), Create(steps), FadeIn(VGroup(marker(None, 0.24).move_to(to(e1)), marker(None, 0.24).move_to(to(e2)))), run_time=1.2)
        self.play_at(W("different", 1), Indicate(VGroup(*[s for s in strips]), color=INK, scale_factor=1.0), run_time=0.9)
        hl = VGroup(Line(to(e1), to(z), stroke_color=PAL[outs(np.angle(e1))], stroke_width=6),
                    Line(to(e2), to(z), stroke_color=PAL[outs(np.angle(e2))], stroke_width=6))
        self.play_at(self.wc(10, "exactly"), Create(hl), run_time=0.9)
        only3 = backed(label("near $z$: neither leftover; only the triangle colours", 26, INK)).to_edge(DOWN, buff=0.4)
        self.play_at(self.wc(10, "neither"), FadeIn(only3), run_time=0.8)

        # cue 11: the region from the paper's polynomial inequality (Lemma 8.8), shaded
        res = 0.02
        xs = np.arange(-2.05, 2.05, res)
        gx, gy = np.meshgrid(xs, xs[::-1])
        l = gx ** 2 + gy ** 2
        Pv = gy ** 2 * (3 * gx ** 2 - gy ** 2) ** 2
        Ppv = l ** 3 * (1 - l / 4) * (l - 1) ** 2
        mask = (l > 0) & (l < 4) & (Pv < Ppv)
        rgba = np.zeros(gx.shape + (4,), np.uint8)
        rgba[mask] = [236, 234, 228, 46]
        reg = ImageMobject(rgba).stretch_to_fit_width(len(xs) * res * Sx).stretch_to_fit_height(len(xs) * res * Sx).move_to(X)
        reg.set_z_index(-10)
        poly = backed(maths(r"\upsilon^2(3\xi^2 - \upsilon^2)^2 < \ell^3\,(1 - \tfrac{\ell}{4})(\ell - 1)^2", 30, INK)).next_to(leg, DOWN, buff=0.4)
        polyref = label("paper, Lemma 8.8 ($\\ell = \\xi^2 + \\upsilon^2$)", 22, MUTED, italic=True).next_to(poly, DOWN, buff=0.12)
        self.play_at(W("pins"), FadeOut(VGroup(steps, hl, only3)), FadeIn(reg), Write(poly), FadeIn(polyref), run_time=1.6)
        three = backed(label("only three colours in the shaded region", 28, INK)).to_edge(DOWN, buff=0.4)
        self.play_at(W("open"), FadeIn(three), run_time=0.8)

        # cue 12: a figure that cannot be 3-coloured
        ms = mini_spindle(0.7).to_corner(DL, buff=0.7).shift(UP * 0.8)
        self.play_at(W("figure"), FadeIn(ms), run_time=0.8)

        # cue 13: the paper's placement; all seven vertices inside the region (asserted)
        for k, zg in PLACE.items():
            assert in_three_region(zg), k
        pts = {k: to(v) for k, v in PLACE.items()}
        placed = VGroup(*[Line(pts[a], pts[b], stroke_color=EDGE, stroke_width=2.5) for a, b in MOSER_E],
                        *[marker(None, 0.24).move_to(p) for p in pts.values()])
        self.play_at(self.wc(13, "take"), FadeOut(three), run_time=0.5)
        self.play_at(W("rotate"), ReplacementTransform(ms, placed), run_time=self.wc(13, "down") + 0.3 - W("rotate"))
        cosl = backed(maths(r"\text{rotate by } \cos^{-1}\tfrac{35}{37},\ \text{shift by } \tfrac{-290 + 149 i}{250}", 28, INK)).to_edge(DOWN, buff=0.4)
        self.play_at(self.wc(13, "set"), FadeIn(cosl), run_time=0.8)
        ticks = VGroup(*[maths(r"\checkmark", 24, colour(GREEN)).next_to(p, UR, buff=0.02) for p in pts.values()])
        self.play_at(W("all", 1, after=205), LaggedStart(*[FadeIn(t, scale=1.5) for t in ticks], lag_ratio=0.12), run_time=1.4)

        # cue 14: exact check
        chk = backed(label("paper: exact fractions (Lemma 8.9) · re-checked here with exact arithmetic", 24, MUTED, italic=True)).next_to(cosl, UP, buff=0.2)
        self.play_at(W("exact", 1), FadeIn(chk), run_time=0.8)

        # cue 15: a proper 3-colouring of the spindle would follow: impossible
        cols = {"0": ORANGE, "A": SKY, "B": GREEN, "T": ORANGE, "uA": GREEN, "uB": SKY, "uT": ORANGE}
        recol = [Transform(placed[11 + i], marker(cols[k], 0.24).move_to(pts[k])) for i, k in enumerate(PLACE)]
        self.play_at(W("contain"), FadeOut(ticks), *recol, run_time=0.8)
        b = burning(pts["T"], pts["uT"], w=4)
        self.play_at(self.wc(15, "impossible"), FadeIn(b), run_time=0.6)
        done3 = backed(maths(r"3 \text{ threads: impossible}", 34 * 0.75, INK)).next_to(done4, DOWN, aligned_edge=LEFT, buff=0.15)
        self.play_at(W("collapses"), Write(done3), run_time=0.8)
        yrs = backed(maths(r"1961 \;\to\; 2026", 34, MUTED)).next_to(poly, DOWN, buff=0.9)
        self.play_at(W("little"), FadeIn(yrs), run_time=0.8)
        self.finish()


class S5_5(NarratedScene):
    """Assembly: the result, the unseen finite graph, the role of computation."""
    scene_id = "s5_5"

    def construct(self):
        W = self.word
        rail = ProofRail().move_to(UP * 1.6)
        rail = rail.lit(0, 0)
        self.add(rail)
        for st, t in ((3, W("transfer")), (4, W("pallets")), (5, W("special")), (7, W("impossible"))):
            self.play_at(t, Transform(rail, rail.lit(st, st)), run_time=0.7)
        res = maths(r"\text{no proper 5-colouring of the plane exists}", 40, INK).move_to(DOWN * 0.4)
        self.play_at(W("so"), Write(res), run_time=1.2)
        bl = BoundsLine(5, 7, y=-2.6)
        self.play_at(W("together", 2), FadeIn(bl), run_time=0.8)
        self.play_at(W("six"), Transform(bl.bracket, bl.set_bounds(6, 7)), run_time=1.0)

        # cue 3: the unseen finite graph
        self.play_at(W("twist"), FadeOut(VGroup(rail, res)), run_time=0.7)
        blob = VGroup(*[mini_spindle(0.35, ang).shift(np.array([np.cos(ang) * 1.1, np.sin(ang) * 0.7, 0]))
                        for ang in np.linspace(0, TAU, 10)[:-1]]).move_to(UP * 1.0).fade(0.5)
        ex = backed(maths(r"\exists\ \text{finite unit-distance } G,\ \ \chi(G) \ge 6", 38, INK)).next_to(blob, DOWN, buff=0.35)
        self.play_at(W("compactness"), FadeIn(blob), Write(ex), run_time=1.6)
        hid = backed(label("guaranteed, but not exhibited", 28, MUTED, italic=True)).next_to(ex, DOWN, buff=0.2)
        self.play_at(W("doesn't", 1), blob.animate.fade(0.6), FadeIn(hid), run_time=0.8)
        size = backed(maths(r"|V(G)| = \ ?", 40, INK)).next_to(blob, RIGHT, buff=0.6)
        self.play_at(W("big"), Write(size), run_time=0.8)

        # cue 4: what computation was used
        self.play_at(W("notice"), FadeOut(VGroup(blob, ex, hid, size)), run_time=0.6)
        rows = VGroup(maths(r"\text{SAT solver}\quad \times", 36, MUTED), maths(r"\text{search over graphs}\quad \times", 36, MUTED),
                      maths(r"\text{one 7-point exact check}\quad \checkmark", 36, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(UP * 0.8)
        for row, t in zip(rows, (W("sat"), W("search"), W("seven", after=50))):
            self.play_at(t, FadeIn(row, shift=RIGHT * 0.2), run_time=0.6)
        self.finish()
