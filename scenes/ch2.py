"""Chapter 2 · Geometry becomes a graph. Each scene renders independently:
    manim -ql scenes/ch2.py S2_3        (draft)     manim -qh scenes/ch2.py S2_3   (1080p60)
"""
import itertools
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.style import (BG, INK, MUTED, FAINT, HOT, HOT_RING, ORANGE, SKY, GREEN, YELLOW, glyph, blank_marker,
                              label, maths, colour, marker, tag, panel, stick)
from components.graph import UnitGraph, clash, DistanceIndicator
from components.narrated import NarratedScene

# ---------- geometry of the spindle (world units; unit distance = 1) ----------
THETA = np.arccos(5 / 6)          # rotation that brings the two far tips to distance 1 (paper: u = (5 + i√11)/6)
R3 = np.sqrt(3)


def axis(phi):
    """Unit vector at angle phi measured from 'up', counter-clockwise."""
    return np.array([-np.sin(phi), np.cos(phi), 0.0])


def rot(v, a):
    c, s = np.cos(a), np.sin(a)
    return np.array([c * v[0] - s * v[1], s * v[0] + c * v[1], 0.0])


def rhombus(phi):
    """Pin at origin; middle vertices at ±30° from the axis; far tip at √3 along the axis."""
    d = axis(phi)
    return {"m1": rot(d, PI / 6), "m2": rot(d, -PI / 6), "t": R3 * d}


def spindle_points():
    r1, r2 = rhombus(-THETA / 2), rhombus(THETA / 2)
    return {"p": np.zeros(3), "a1": r1["m1"], "b1": r1["m2"], "t1": r1["t"],
            "a2": r2["m1"], "b2": r2["m2"], "t2": r2["t"]}


SPINDLE_EDGES = [("p", "a1"), ("p", "b1"), ("a1", "b1"), ("a1", "t1"), ("b1", "t1"),
                 ("p", "a2"), ("p", "b2"), ("a2", "b2"), ("a2", "t2"), ("b2", "t2"), ("t1", "t2")]


class S2_3(NarratedScene):
    """The spindle (pilot scene)."""
    scene_id = "s2_3"

    def construct(self):
        S = 2.5                                   # manim units per world unit
        PIN = np.array([0.0, -2.6, 0.0])          # screen position of the shared pin
        P = spindle_points()
        to_screen = lambda w: PIN + S * np.asarray(w)
        W = self.word

        # sanity: geometry really is a unit-distance graph with exactly 11 unit edges
        unit_pairs = [(a, b) for a, b in itertools.combinations(P, 2) if abs(np.linalg.norm(P[a] - P[b]) - 1) < 1e-9]
        assert sorted(map(sorted, unit_pairs)) == sorted(map(sorted, SPINDLE_EDGES)), unit_pairs

        # ---------- first rhombus ----------
        r1 = {"p": P["p"], "a1": P["a1"], "b1": P["b1"], "t1": P["t1"]}
        g1 = UnitGraph(r1, scale=S, origin=PIN)
        tri_a = [g1.st[e] for e in g1.edge_keys if "t1" not in e]
        tri_b = [g1.st[e] for e in g1.edge_keys if "t1" in e]

        # cue 1: "Glue two triangles along an edge … a diamond … rhombus with four vertices … three colours."
        self.play_at(self.cue(1), *[Create(s) for s in tri_a],
                     *[GrowFromCenter(g1.mk[k]) for k in ("p", "a1", "b1")], run_time=1.1)
        self.play_at(W("along"), *[Create(s) for s in tri_b], GrowFromCenter(g1.mk["t1"]), run_time=1.1)
        outline = Polygon(*[to_screen(P[k]) for k in ("p", "a1", "t1", "b1")], stroke_width=0,
                          fill_color=INK, fill_opacity=0.0)
        self.add(outline)
        self.play_at(W("diamond"), outline.animate(rate_func=there_and_back, run_time=1.0).set_fill(opacity=0.12))
        cap = VGroup()

        legend = VGroup(*[marker(c, 0.42) for c in (ORANGE, SKY, GREEN)]).arrange(RIGHT, buff=0.35)
        legend_title = label("3 colours", 26, MUTED).next_to(legend, RIGHT, buff=0.35)
        legend_panel = VGroup(legend, legend_title).to_corner(UL, buff=0.6)
        self.play_at(W("colour", 1), LaggedStart(*[FadeIn(x, scale=0.5) for x in legend], lag_ratio=0.25),
                     FadeIn(legend_title), run_time=1.0)

        # cue 2: forcing argument
        mids = VGroup(g1.mk["a1"], g1.mk["b1"])
        self.play_at(W("shared"), Indicate(mids, color=INK, scale_factor=1.35), run_time=0.9)
        self.play_at(W("blue"), g1.colour_anim("a1", SKY, 0.4))
        self.play_at(W("green"), g1.colour_anim("b1", GREEN, 0.4))

        def forced(g, tip, nbrs, t_try, t_final, final=ORANGE):
            """Tip tries the two taken colours (each clashes with a neighbour), then settles on the third."""
            self.play_at(t_try[0], Indicate(g.mk[tip], color=INK, scale_factor=1.4), run_time=0.5)
            for c, nb, t in zip((SKY, GREEN), nbrs, t_try[1:]):
                self.until(t)
                self.play(g.colour_anim(tip, c, 0.2))
                a, z, ring = clash(g.live_pos(tip), g.live_pos(nb), run_time=0.45)
                self.play(a)
                self.remove(z, ring)
            self.play_at(t_final, g.colour_anim(tip, final, 0.4))

        forced(g1, "t1", ("a1", "b1"), (W("top"), W("both"), W("so", after=16.5)), W("orange", 1) - 0.3)
        forced(g1, "p", ("a1", "b1"), (W("bottom"), W("joined", 2) + 0.2, W("same", 1) + 0.5), W("orange", 2) - 0.3)

        # cue 3: forced equal, √3 apart
        dash1 = DashedLine(g1.pos("p"), g1.pos("t1"), dash_length=0.12, stroke_color=MUTED, stroke_width=3).set_z_index(-1)
        self.play_at(W("far"), Create(dash1), run_time=1.0)
        feq1_tag = maths(r"c(t_1) = c(p)", 30, INK).next_to(g1.mk["t1"], RIGHT, buff=0.3)
        feq1 = feq1_tag
        self.play_at(W("share"), FadeIn(feq1, shift=LEFT * 0.15), run_time=0.6)
        ind1 = maths(r"|p\,t_1| = \sqrt{3}", 28, MUTED).next_to(feq1_tag, DOWN, aligned_edge=LEFT, buff=0.25)
        sqrt3 = maths(r"\approx 1.732", 28, MUTED).next_to(ind1, RIGHT, buff=0.15)
        self.play_at(W("square"), FadeIn(ind1), run_time=0.6)
        self.play_at(W("about", after=33), FadeIn(sqrt3), run_time=0.5)
        self.play_at(W("not", after=35), Indicate(ind1, color=INK, scale_factor=1.15), run_time=0.8)

        # cue 4: the second rhombus, pinned at the same tip, starts far away to the left
        phi = ValueTracker(THETA / 2 + 55 * DEGREES)

        def r2_world():
            r = rhombus(phi.get_value())
            return {"a2": r["m1"], "b2": r["m2"], "t2": r["t"]}

        r2_edges = [("p", "a2"), ("p", "b2"), ("a2", "b2"), ("a2", "t2"), ("b2", "t2")]
        w0 = r2_world()
        sticks2 = {e: stick(to_screen(w0.get(e[0], P["p"])), to_screen(w0.get(e[1], P["p"]))) for e in r2_edges}
        mk2 = {k: marker(None, g1.marker_size).move_to(to_screen(w0[k])) for k in w0}
        colours2 = {k: None for k in mk2}
        dash2 = DashedLine(g1.pos("p"), to_screen(w0["t2"]), dash_length=0.12, stroke_color=MUTED, stroke_width=3).set_z_index(-1)
        feq2 = maths(r"c(t_2) = c(p)", 30, INK)

        def follow(_):
            w = r2_world()
            for (a, b), s in sticks2.items():
                s.put_start_and_end_on(to_screen(w.get(a, P["p"])), to_screen(w.get(b, P["p"])))
            for k, m in mk2.items():
                m.move_to(to_screen(w[k]))
            dash2.put_start_and_end_on(g1.pos("p"), to_screen(w["t2"]))
            feq2.next_to(mk2["t2"], LEFT, buff=0.3)

        holder = VGroup(*sticks2.values(), dash2, feq2, *mk2.values())
        self.play_at(W("second", 1), FadeOut(ind1), FadeOut(sqrt3),
                     *[Create(s) for s in sticks2.values()], *[GrowFromCenter(m) for m in mk2.values()],
                     run_time=1.3)
        self.bring_to_front(g1.mk["p"])
        self.play_at(W("pinned"), Indicate(g1.mk["p"], color=INK, scale_factor=1.5), run_time=0.8)

        def recolour2(k, c, rt=0.35):
            colours2[k] = c
            return Transform(mk2[k], marker(c, g1.marker_size).move_to(mk2[k]), run_time=rt)

        self.play_at(W("argument", 1), recolour2("a2", SKY), recolour2("b2", GREEN))
        self.play_at(W("match", 1), recolour2("t2", ORANGE, 0.45))
        follow(None)
        self.play_at(W("both", 2), Create(dash2), FadeIn(feq2), run_time=0.9)
        self.play_at(W("orange", 3) - 0.2, Indicate(VGroup(g1.mk["t1"], mk2["t2"]), color=INK, scale_factor=1.35),
                     run_time=0.9)

        # cue 5–7: rotate; live distance between far tips; exact 1.000 at "one"
        tipdash = DashedLine(g1.pos("t1"), mk2["t2"].get_center(), dash_length=0.1, stroke_color=INK,
                             stroke_width=2.5, stroke_opacity=0.7)
        tipdash.add_updater(lambda m: m.put_start_and_end_on(g1.pos("t1"), mk2["t2"].get_center()))
        ind2 = DistanceIndicator(lambda: mk2["t2"].get_center(), lambda: g1.pos("t1"), per_unit=S, offset=0.5,
                                 side=1, show_line=True, font_size=36)
        holder.add_updater(follow)
        self.add(holder)
        self.play_at(W("trick"), Create(tipdash), FadeIn(ind2), run_time=0.9)
        circ = DashedVMobject(Arc(radius=S * R3, start_angle=35 * DEGREES, angle=110 * DEGREES, arc_center=PIN,
                                  stroke_color=MUTED, stroke_width=2), num_dashes=60).set_z_index(-1)
        self.until(W("rotate"))
        phase1_end = W("until") - 0.05
        self.play(phi.animate(rate_func=rate_functions.ease_in_sine).set_value(THETA / 2 + 32 * DEGREES),
                  run_time=W("both", 3) - self.now)
        self.play(Create(circ, rate_func=linear), phi.animate(rate_func=linear).set_value(THETA / 2 + 15 * DEGREES),
                  run_time=1.6)
        self.play(phi.animate(rate_func=linear).set_value(THETA / 2 + 8 * DEGREES), run_time=phase1_end - self.now)
        self.play(phi.animate(rate_func=rate_functions.ease_out_cubic).set_value(THETA / 2),
                  run_time=W("one", after=63) + 0.15 - self.now)
        holder.clear_updaters()
        new_edge = stick(g1.pos("t1"), mk2["t2"].get_center())
        self.play(FadeOut(tipdash), Create(new_edge), run_time=0.6)
        self.bring_to_front(g1.mk["t1"], mk2["t2"])

        # cue 8: clash; both were forced equal to the pin
        self.play_at(W("joined", 3), Indicate(new_edge, color=INK, scale_factor=1.05), run_time=0.8)
        a, z, ring = clash(g1.pos("t1"), mk2["t2"].get_center(), run_time=1.0)
        self.play_at(W("different"), a)
        self.remove(ring)
        self.play_at(W("forced", 3), Indicate(VGroup(dash1, feq1), color=INK), Indicate(VGroup(dash2, feq2), color=INK),
                     run_time=1.4)

        # cue 9: impossible
        verdict = label("3 colours: impossible", 34, INK).to_corner(UR, buff=0.6)
        cross = Line(legend_panel.get_left() + LEFT * 0.1, legend_panel.get_right() + RIGHT * 0.1, stroke_color=HOT,
                     stroke_width=3)
        self.play_at(W("impossible") - 0.4, FadeIn(verdict, shift=DOWN * 0.15),
                     Create(cross), run_time=0.8)

        # cue 10: tidy into the standard spindle drawing; name it
        spindle = UnitGraph(P, scale=S, origin=PIN)
        assert len(spindle.edge_keys) == 11
        self.play_at(W("this", after=76), FadeOut(VGroup(dash1, feq1, dash2, feq2, circ, ind2, z, verdict, cross,
                                                         legend_panel)), run_time=0.8)
        self.clear_stage()
        self.add(spindle)
        self.play(*[spindle.colour_anim(k, None, 0.4) for k in spindle.world], run_time=0.5)
        nv = label("7 vertices", 32, INK)
        ne = label("11 edges", 32, INK)
        stats = VGroup(nv, ne).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=1.1).shift(UP * 0.2)
        self.play_at(W("seven", 1), FadeIn(nv, shift=LEFT * 0.2), Indicate(spindle.markers, color=INK, scale_factor=1.3),
                     run_time=0.8)
        self.play_at(W("eleven"), FadeIn(ne, shift=LEFT * 0.2),
                     LaggedStart(*[Indicate(s, color=INK, scale_factor=1.0) for s in spindle.sticks], lag_ratio=0.08),
                     run_time=1.0)
        title = label("The Moser spindle", 44, INK).to_edge(UP, buff=0.5)
        sub = label("L. & W. Moser, 1961", 26, MUTED).next_to(title, DOWN, buff=0.15)
        self.play_at(W("moser", 1), FadeIn(title, shift=DOWN * 0.15), run_time=0.7)
        self.play_at(W("leo"), FadeIn(sub), run_time=0.7)

        # cue 11: brute force 3^7 = 2187, all fail; 4 colours works
        all_cols = list(itertools.product(range(3), repeat=7))
        keys = list(P)
        idx = {k: i for i, k in enumerate(keys)}
        bad_edge = []
        for c in all_cols:
            e = next(((a, b) for a, b in SPINDLE_EDGES if c[idx[a]] == c[idx[b]]), None)
            assert e is not None, "found a proper 3-colouring: impossible"
            bad_edge.append(e)
        assert len(all_cols) == 2187

        left_group = VGroup(spindle, nv, ne, title, sub)
        self.play_at(W("trust"), FadeOut(VGroup(nv, ne, sub)), title.animate.to_corner(UL, buff=0.5).scale(0.8),
                     spindle.animate.scale(0.55).move_to(LEFT * 4.9 + DOWN * 0.3), run_time=1.0)
        formula = maths(r"3^7 = 2187", 46).move_to(RIGHT * 2.6 + UP * 3.2)
        self.play_at(W("three", after=90), Write(formula), run_time=0.9)

        cols_n, rows_n, ts = 6, 3, 0.62
        cell = np.array([1.42, 1.78, 0])
        grid_origin = np.array([-1.55, 1.05, 0])

        def thumb(c, e):
            pts = {k: grid_origin + 0 + ts * P[k] for k in P}
            g = VGroup()
            for a, b in SPINDLE_EDGES:
                hot = (a, b) == e
                if hot:
                    g.add(Line(pts[a], pts[b], stroke_color=HOT_RING, stroke_width=14, stroke_opacity=0.3))
                g.add(Line(pts[a], pts[b], stroke_color=HOT if hot else MUTED, stroke_width=4.5 if hot else 1.8))
            for k in P:
                g.add(glyph([ORANGE, SKY, GREEN][c[idx[k]]], 0.17, stroke_width=1.2).move_to(pts[k]))
            return g

        def batch(start):
            g = VGroup()
            for j in range(cols_n * rows_n):
                n = start + j
                if n >= len(all_cols):
                    break
                t = thumb(all_cols[n], bad_edge[n])
                t.shift(np.array([(j % cols_n) * cell[0], -(j // cols_n) * cell[1], 0]))
                g.add(t)
            return g

        count = ValueTracker(0)
        tail = label("of 2187 checked, every one breaks an edge", 26, MUTED)
        counter = always_redraw(lambda: VGroup(Integer(int(count.get_value()), font_size=44, color=INK, group_with_commas=False), tail.copy())
                                .arrange(RIGHT, buff=0.25).move_to(RIGHT * 2.45 + DOWN * 3.35))
        starts = [0, 700, 1400, 2169]
        b = batch(starts[0])
        self.play_at(W("2187") + 0.4, FadeIn(b, lag_ratio=0.01), FadeIn(counter), run_time=1.2)
        t0, t1 = W("ways"), W("edge", after=98) + 0.4
        self.play(count.animate(rate_func=linear).set_value(starts[1]), run_time=(t0 - self.now))
        span = (t1 - self.now) / 3
        for s_next, v in zip(starts[1:], (1400, 2169, 2187)):
            nb = batch(s_next)
            self.play(FadeOut(b, run_time=0.15), FadeIn(nb, run_time=0.15))
            b = nb
            self.play(count.animate(rate_func=linear).set_value(v), run_time=max(span - 0.15, 0.2))

        # four colours: a proper colouring exists
        four = {"p": ORANGE, "a1": SKY, "b1": GREEN, "t1": ORANGE, "a2": SKY, "b2": GREEN, "t2": YELLOW}
        assert all(four[a] != four[b] for a, b in SPINDLE_EDGES)
        self.play_at(W("four", after=99), FadeOut(b), counter.animate.set_opacity(0.4),
                     spindle.animate.scale(1 / 0.55).move_to(PIN + S * np.array([0, R3 / 2, 0]) + LEFT * 1.0),
                     run_time=0.6)
        self.play(*[spindle.colour_anim(k, c, 0.4) for k, c in four.items()], run_time=0.5)
        ok = label("4 colours: it works", 34, INK).next_to(spindle, RIGHT, buff=0.9)
        self.play_at(W("works"), FadeIn(ok, scale=1.2), run_time=0.5)
        err = spindle.misalignment()
        assert err < 1e-3, f"vertex markers misaligned by {err:.4f} units"
        self.finish()


# ======================================================================================================
from components.style import burning, backed
from components.widgets import WildPlane, hex_tiling

TRI = {"a": (-0.5, -np.sqrt(3) / 6), "b": (0.5, -np.sqrt(3) / 6), "c": (0, np.sqrt(3) / 3)}
RHOMB = {"a": (-0.5, 0), "b": (0.5, 0), "c": (0, np.sqrt(3) / 2), "d": (0, -np.sqrt(3) / 2)}


def fan(center, S, n=24, opacity=1.0, phase=0.0, width=2.0):
    """Unit sticks from one point to n points of its unit circle."""
    c = np.asarray(center, float)
    g = VGroup()
    for k in range(n):
        a = phase + TAU * k / n
        q = c + S * np.array([np.cos(a), np.sin(a), 0])
        g.add(Line(c, q, stroke_color=INK, stroke_width=width, stroke_opacity=opacity))
    return g


class S2_1(NarratedScene):
    """Dots and sticks: the plane as a graph."""
    scene_id = "s2_1"

    def construct(self):
        W = self.word
        S = 1.7
        # cue 1: a pair at distance one
        pair = UnitGraph({"x": (-0.5, 0), "y": (0.5, 0)}, scale=S, origin=UP * 0.3)
        self.play_at(W("pairs"), FadeIn(pair.markers, scale=0.5), run_time=0.7)
        self.play_at(W("distance", 1), Create(pair.sticks), run_time=0.7)
        one = maths("1", 32, MUTED).next_to(pair.sticks, UP, buff=0.2)
        self.play_at(W("draw"), FadeIn(one), run_time=0.5)

        # cue 2: one point and its unit circle
        c0 = ORIGIN + UP * 0.3
        dot0 = marker(None, 0.38).move_to(c0)
        ring = DashedVMobject(Circle(radius=S, stroke_color=MUTED, stroke_width=1.5).move_to(c0), num_dashes=60)
        f0 = fan(c0, S, 24)
        ends = VGroup(*[Dot(l.get_end(), radius=0.04, color=INK) for l in f0])
        self.play_at(W("every", 1), FadeOut(VGroup(pair, one)), FadeIn(dot0), run_time=0.6)
        self.play_at(W("every", 2), Create(ring), run_time=0.9)
        self.play_at(W("joined"), LaggedStart(*[Create(l) for l in f0], lag_ratio=0.05), FadeIn(ends, lag_ratio=0.05),
                     run_time=1.4)

        # cue 3: do it for every point: a dense web
        rng = np.random.default_rng(4)
        pts = [np.array([rng.uniform(-6.4, 6.4), rng.uniform(-3.4, 3.6), 0]) for _ in range(40)]
        web = VGroup(*[fan(p, S, 14, opacity=0.18, phase=rng.uniform(0, TAU), width=1.5) for p in pts])
        wdots = VGroup(*[Dot(p, radius=0.045, color=INK) for p in pts])
        self.play_at(W("all", 1), FadeOut(ends), f0.animate.set_stroke(opacity=0.35), ring.animate.set_stroke(opacity=0.4),
                     LaggedStart(*[FadeIn(VGroup(w, d)) for w, d in zip(web, wdots)], lag_ratio=0.03), run_time=2.4)
        full = Circle(radius=S, stroke_color=INK, stroke_width=3).move_to(c0)
        self.play_at(W("entire"), Create(full), run_time=1.0)

        # cue 4: a graph: vertices and edges
        g = UnitGraph(RHOMB, scale=S, origin=c0)
        self.play_at(W("structure"), FadeOut(VGroup(web, wdots, f0, ring, full, dot0)), FadeIn(g), run_time=1.0)
        name = label("a graph", 40, INK).to_edge(UP, buff=0.7)
        self.play_at(W("graph"), Write(name), run_time=0.8)
        vlab = label("vertex", 30, MUTED).next_to(g.mk["b"], RIGHT, buff=0.5)
        varr = Arrow(vlab.get_left(), g.mk["b"].get_center(), buff=0.25, stroke_width=2, color=MUTED,
                     max_tip_length_to_length_ratio=0.15)
        self.play_at(W("vertices"), FadeIn(vlab), GrowArrow(varr), run_time=0.7)
        e = g.st[("a", "d")] if ("a", "d") in g.st else g.st[("d", "a")]
        elab = label("edge", 30, MUTED).next_to(e.get_center(), LEFT, buff=0.9)
        earr = Arrow(elab.get_right(), e.get_center(), buff=0.15, stroke_width=2, color=MUTED,
                     max_tip_length_to_length_ratio=0.15)
        self.play_at(W("edges"), FadeIn(elab), GrowArrow(earr), run_time=0.7)

        # cue 5: proper colouring, chromatic number
        self.play_at(W("coloring", 1), FadeOut(VGroup(vlab, varr, elab, earr)),
                     *[g.colour_anim(k, c, 0.4) for k, c in (("a", SKY), ("b", GREEN), ("c", ORANGE), ("d", SKY))])
        bad = burning(g.pos("a"), g.pos("d"))
        self.play_at(W("edge", 1), FadeIn(bad), run_time=0.4)
        self.play_at(W("proper", 1), FadeOut(bad), g.colour_anim("d", ORANGE, 0.4))
        rule = maths(r"\text{proper:}\quad c(x) \neq c(y)\ \text{for every edge } xy", 34, INK).to_edge(DOWN, buff=0.8)
        self.play_at(W("coloring", 2) + 0.2, Write(rule), run_time=1.2)
        chi_g = maths(r"\chi(G) = \text{fewest colours} = 3", 36, INK).next_to(rule, UP, buff=0.35)
        self.play_at(W("chromatic", 1), Write(chi_g), run_time=1.2)

        # cue 6: the chromatic number of the plane
        chi = maths(r"\chi(\mathbb{R}^2) = \ ?", 64, INK)
        self.play_at(W("chromatic", 2), FadeOut(VGroup(g, rule, chi_g, name)), Write(chi), run_time=1.2)
        self.play_at(W("chi"), Indicate(chi[0][0], color=colour(ORANGE), scale_factor=1.4), run_time=1.0)

        # cue 7: same problem, new view: small pieces
        web_dim = VGroup(web, wdots).copy().fade(0.75)
        self.play_at(W("notice"), chi.animate.scale(0.6).to_corner(UL, buff=0.6), FadeIn(web_dim), run_time=1.2)
        lens = Circle(radius=1.3, stroke_color=INK, stroke_width=3).move_to(LEFT * 3 + DOWN * 0.5)
        self.play_at(W("study"), FadeIn(lens, scale=0.8), run_time=0.6)
        self.play(lens.animate.move_to(RIGHT * 2.5 + UP * 0.6), run_time=self.left(self.audio_duration - 0.3),
                  rate_func=smooth)
        self.finish()


class S2_2(NarratedScene):
    """The triangle, renamed: chi(R^2) >= 3."""
    scene_id = "s2_2"

    def construct(self):
        W = self.word
        S = 2.4
        g = UnitGraph(TRI, scale=S, origin=UP * 0.2)
        self.play_at(W("triangle", 1), FadeIn(g.markers, scale=0.5), LaggedStart(*[Create(s) for s in g.sticks],
                                                                                  lag_ratio=0.3), run_time=1.2)
        self.play_at(W("pair"), Indicate(g.sticks, color=colour(SKY), scale_factor=1.0), run_time=0.8)
        # cue 2: a colouring of the plane restricts to the triangle
        plane = WildPlane(cell=0.2, seed=21, dim=0.3)
        self.play_at(W("whole"), FadeIn(plane.image), run_time=1.0)
        self.bring_to_front(g)
        cols = {"a": ORANGE, "b": SKY, "c": GREEN}
        self.play_at(W("these"), *[g.colour_anim(k, c, 0.5) for k, c in cols.items()])
        self.play_at(W("least", 1), FadeOut(plane.image), run_time=0.8)
        # cue 3
        f1 = maths(r"\chi(\triangle) = 3", 44, INK).to_edge(UP, buff=0.8).shift(LEFT * 2.6)
        f2 = maths(r"\Rightarrow\quad \chi(\mathbb{R}^2) \ge 3", 44, INK).next_to(f1, RIGHT, buff=0.5)
        self.play_at(W("chromatic", 1), Write(f1), run_time=1.0)
        self.play_at(W("chromatic", 2), Write(f2), run_time=1.0)
        # cue 4: glue a second triangle: a hint of what comes next
        r = UnitGraph(RHOMB, scale=S, origin=UP * 0.2 + DOWN * S * (np.sqrt(3) / 2 - np.sqrt(3) / 3) * 0)
        ghost = Polygon(g.pos("a"), g.pos("b"), g.pos("a") + S * np.array([0.5, -np.sqrt(3) / 2, 0]),
                        stroke_color=INK, stroke_width=3, stroke_opacity=0.5).set_fill(opacity=0)
        self.play_at(W("bigger"), Create(ghost), run_time=1.0)
        self.finish()


class S2_4(NarratedScene):
    """Stamping: any colouring of the plane restricts to a colouring of the spindle."""
    scene_id = "s2_4"

    def construct(self):
        W = self.word
        S = 1.7
        P = spindle_points()
        rng = np.random.default_rng(5)

        def stamp_at(centre, angle):
            pts = {k: rot(v, angle) for k, v in P.items()}
            off = np.asarray(centre) - S * np.mean([pts[k] for k in pts], axis=0)
            return UnitGraph(pts, scale=S, origin=off)

        sp = stamp_at(ORIGIN, 0)
        self.play_at(self.cue(1), FadeIn(sp), run_time=0.8)
        plane = WildPlane(cell=0.22, seed=31, dim=0.38)
        self.play_at(W("imagine"), FadeIn(plane.image), sp.animate.shift(UP * 4.5), run_time=1.2)

        def land(g, colour_at, t_drop, t_colour, t_burn):
            """Drop stamp g, colour its vertices from the plane, burn every clashing edge (there must be one)."""
            self.play_at(t_drop, FadeIn(g, shift=DOWN * 0.4), run_time=0.6)
            cols = {k: colour_at(g.pos(k)) for k in g.world}
            self.play_at(t_colour, *[g.colour_anim(k, c, 0.4) for k, c in cols.items()], lag_ratio=0.12, run_time=1.0)
            bad = [(a, b) for a, b in g.edge_keys if cols[a] == cols[b]]
            assert bad, "a proper 3-colouring of the spindle cannot exist"
            burns = VGroup(*[burning(g.pos(a), g.pos(b)) for a, b in bad])
            self.play_at(t_burn, FadeIn(burns), run_time=0.5)
            return burns

        g1 = stamp_at(LEFT * 0.5 + DOWN * 0.2, 0.3)
        self.remove(sp)
        self.play_at(W("spindle"), FadeIn(g1, shift=DOWN * 1.0), run_time=0.8)
        cols = {k: plane.colour_at(g1.pos(k)) for k in g1.world}
        self.play_at(W("each"), LaggedStart(*[g1.colour_anim(k, c, 0.4) for k, c in cols.items()], lag_ratio=0.5),
                     run_time=W("colour", 1) - W("each"))
        # cue 3: edges are unit edges; the rule applies to each of them
        self.play_at(W("edges"), Indicate(g1.sticks, color=INK, scale_factor=1.0), run_time=1.0)
        claim = backed(maths(r"\text{a proper 3-colouring of the spindle?}", 34, INK)).to_edge(UP, buff=0.6)
        self.play_at(W("hands"), FadeIn(claim), run_time=0.8)
        # cue 4: but none exists: the stamp always finds a broken edge
        bad = [(a, b) for a, b in g1.edge_keys if cols[a] == cols[b]]
        assert bad
        b1 = VGroup(*[burning(g1.pos(a), g1.pos(b)) for a, b in bad])
        self.play_at(W("exists"), FadeIn(b1), FadeOut(claim), run_time=0.6)
        prev = VGroup(g1, b1)
        for t, (cx, cy, ang) in zip((W("always"), W("wherever")), ((3.6, 1.0, 1.1), (-3.8, -0.6, 2.0))):
            g = stamp_at([cx, cy, 0], ang)
            self.play_at(t, FadeOut(prev), FadeIn(g), run_time=0.4)
            cols = {k: plane.colour_at(g.pos(k)) for k in g.world}
            self.play(*[g.colour_anim(k, c, 0.25) for k, c in cols.items()], run_time=0.3)
            bad = [(a, b) for a, b in g.edge_keys if cols[a] == cols[b]]
            assert bad
            bb = VGroup(*[burning(g.pos(a), g.pos(b)) for a, b in bad])
            self.play(FadeIn(bb), run_time=0.25)
            prev = VGroup(g, bb)
        # whatever the colouring: switch to a hexagonal 3-colouring
        hexes, cells = hex_tiling(0.4 * S, 3)
        centres = np.array([c[0] for c in cells])
        hex_at = lambda p: cells[int(np.argmin(np.linalg.norm(centres - p, axis=1)))][1]
        self.play_at(W("whatever"), FadeOut(plane.image), FadeOut(prev), FadeIn(hexes), run_time=0.8)
        g = stamp_at([0.3, -0.2, 0], 0.45)
        self.play(FadeIn(g), run_time=0.4)
        cols = {k: hex_at(g.pos(k)) for k in g.world}
        self.play(*[g.colour_anim(k, c, 0.3) for k, c in cols.items()], run_time=0.4)
        bad = [(a, b) for a, b in g.edge_keys if cols[a] == cols[b]]
        assert bad
        bb = VGroup(*[burning(g.pos(a), g.pos(b)) for a, b in bad])
        self.play(FadeIn(bb), run_time=0.3)
        verdict = backed(label("3 colours cannot work for the plane", 36, INK)).to_edge(UP, buff=0.6)
        self.play_at(W("three", 3), FadeIn(verdict), run_time=0.8)
        # cue 5: the logic to remember
        logic = maths(r"\chi(G) = N \;\;\Longrightarrow\;\; \chi(\mathbb{R}^2) \ge N", 48, INK)
        sub = label("for any finite graph G drawn with unit edges", 28, MUTED, italic=True).next_to(logic, DOWN, buff=0.4)
        self.play_at(W("logic"), FadeOut(VGroup(hexes, g, bb, verdict)), run_time=0.7)
        self.play_at(W("if"), Write(logic), run_time=1.6)
        self.play_at(W("whole"), FadeIn(sub), run_time=0.7)
        # cue 6
        res = maths(r"\chi(\mathbb{R}^2) \ge 4", 64, INK)
        self.play_at(W("chromatic"), FadeOut(sub), ReplacementTransform(logic, res), run_time=1.2)
        self.finish()


class S2_5(NarratedScene):
    """Is there a ceiling?"""
    scene_id = "s2_5"

    def construct(self):
        W = self.word
        seq = [maths(r"\chi(\mathbb{R}^2) \ge 4", 56, INK), maths(r"\chi(\mathbb{R}^2) \ge 5", 56, INK),
               maths(r"\chi(\mathbb{R}^2) \ge 6", 56, INK), maths(r"\chi(\mathbb{R}^2) \ge \;\cdots", 56, INK)]
        cur = seq[0]
        self.add(cur)
        for t, nxt in zip((W("five"), W("six"), W("more")), seq[1:]):
            self.play_at(t, TransformMatchingTex(cur, nxt), run_time=0.6)
            cur = nxt
        inf = maths(r"\chi(\mathbb{R}^2) = \infty\,?", 56, INK)
        self.play_at(W("infinitely"), TransformMatchingTex(cur, inf), run_time=0.8)
        ceil = Line(LEFT * 6, RIGHT * 6, stroke_color=INK, stroke_width=4).to_edge(UP, buff=1.2)
        no = maths(r"\chi(\mathbb{R}^2) \le \ ?", 56, INK)
        self.play_at(W("doesn't"), FadeOut(inf, shift=UP * 0.3), Create(ceil), run_time=0.9)
        self.play_at(W("ceiling"), Write(no), run_time=1.0)
        self.finish()
