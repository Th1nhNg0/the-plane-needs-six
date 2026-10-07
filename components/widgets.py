"""Reusable film widgets: bounds number line, proof-map rail, palette ring, status tags, code panel,
plane colourings (noise, hexagons, stripes), paper card, verdict rows."""
import numpy as np
from manim import (VGroup, VMobject, Line, DashedLine, Dot, Circle, Arc, AnnularSector, Polygon, RegularPolygon,
                   RoundedRectangle, Rectangle, Square, Text, MathTex, Triangle, Arrow, CurvedArrow, always_redraw,
                   UP, DOWN, LEFT, RIGHT, ORIGIN, PI, TAU, DEGREES, interpolate_color, ManimColor)

from .style import (BG, INK, MUTED, SOFT, FAINT, HOT, HOT_RING, PANEL, PANEL_EDGE, colour, glyph, label, maths, tag,
                    panel, region, FONT, ORANGE, SKY, GREEN, YELLOW, BLUE, VERMILLION, PURPLE)

MONO = "DejaVu Sans Mono"
STATUS = {
    "FACT": ("FACT", ManimColor("#9AD1A8")),
    "INFERENCE": ("INFERENCE · possible reconstruction, not confirmed by OpenAI", ManimColor("#F0C674")),
    "NOT PUBLIC": ("NOT PUBLIC", ManimColor("#E8A0A0")),
    "ANALOGY": ("ANALOGY", ManimColor("#B5C7F2")),
    "TOY PROBLEM": ("TOY PROBLEM", ManimColor("#B5C7F2")),
    "DIFFERENT RESULT": ("DIFFERENT RESULT · family 017 · not the five-colour proof", ManimColor("#F0C674")),
}


def status(kind, size=20):
    text, col = STATUS[kind]
    return tag(text, size, col, edge=col)


def source_line(text, size=18):
    return label(text, size, MUTED)


# ----------------------------------------------------------------------------------------------------------
class BoundsLine(VGroup):
    """Number line 1..8 with a highlighted bracket [lo, hi] for the chromatic number of the plane."""

    def __init__(self, lo=4, hi=7, width=9.0, y=-3.2, show_chi=True):
        super().__init__()
        self.x0, self.dx, self.y = -width / 2, width / 7, y
        axis = Line([self.x0 - 0.3, y, 0], [self.x0 + width + 0.3, y, 0], stroke_color=MUTED, stroke_width=2)
        ticks = VGroup(*[Line([self.x(n), y - 0.08, 0], [self.x(n), y + 0.08, 0], stroke_color=MUTED, stroke_width=2)
                         for n in range(1, 9)])
        nums = VGroup(*[label(str(n), 24, MUTED).next_to([self.x(n), y, 0], DOWN, buff=0.18) for n in range(1, 9)])
        self.axis = VGroup(axis, ticks, nums)
        self.lo, self.hi = lo, hi
        self.bracket = self._bracket(lo, hi)
        self.add(self.axis, self.bracket)
        if show_chi:
            self.chi = maths(r"\chi(\mathbb{R}^2)", 30, INK).next_to(axis, LEFT, buff=0.3)
            self.add(self.chi)

    def x(self, n):
        return self.x0 + (n - 1) * self.dx

    def _bracket(self, lo, hi):
        y = self.y
        bar = Line([self.x(lo), y, 0], [self.x(hi), y, 0], stroke_color=INK, stroke_width=8)
        ends = VGroup(*[Line([self.x(n), y - 0.22, 0], [self.x(n), y + 0.22, 0], stroke_color=INK, stroke_width=5)
                        for n in (lo, hi)])
        return VGroup(bar, ends)

    def set_bounds(self, lo, hi):
        """Animation target: use `self.play(Transform(bl.bracket, bl.bracket_for(lo, hi)))`."""
        self.lo, self.hi = lo, hi
        return self._bracket(lo, hi)

    def chip(self, text, n, up=True, size=20, color=MUTED):
        c = label(text, size, color)
        return c.next_to([self.x(n), self.y, 0], UP if up else DOWN, buff=0.45 if up else 0.65)


# ----------------------------------------------------------------------------------------------------------
RAIL_STATIONS = ["proper\n5-colouring", "symmetric\nrandom colouring", "smooth\npart", "weak measurable\ncolouring",
                 "palettes\n≤ 2 colours", "threads on a\n3/4/5-cycle", "three\ncases", "contradiction"]


class ProofRail(VGroup):
    """The proof map (redrawn from the paper's Fig. 1) as a transit line of 8 stations."""

    def __init__(self, width=12.6, y=2.9, size=17):
        super().__init__()
        n = len(RAIL_STATIONS)
        xs = np.linspace(-width / 2, width / 2, n)
        self.pts = [np.array([x, y, 0]) for x in xs]
        self.track = Line(self.pts[0], self.pts[-1], stroke_color=MUTED, stroke_width=4)
        self.dots = VGroup(*[Circle(radius=0.11).set_fill(BG, 1).set_stroke(MUTED, 3).move_to(p) for p in self.pts])
        self.names = VGroup(*[label(s.replace("\n", "\\\\"), size * 1.05, MUTED).next_to(p, DOWN, buff=0.2)
                              for s, p in zip(RAIL_STATIONS, self.pts)])
        tame = Line(self.pts[0] + UP * 0.35, self.pts[3] + UP * 0.35, stroke_color=MUTED, stroke_width=1.5)
        trap = Line(self.pts[4] + UP * 0.35, self.pts[7] + UP * 0.35, stroke_color=MUTED, stroke_width=1.5)
        self.halves = VGroup(VGroup(tame, label("tame", 20, MUTED, italic=True).next_to(tame, UP, buff=0.08)),
                             VGroup(trap, label("trap", 20, MUTED, italic=True).next_to(trap, UP, buff=0.08)))
        self.add(self.track, self.dots, self.names, self.halves)

    def lit(self, upto, active=None):
        """Target copy with stations 0..upto lit (ink) and `active` highlighted."""
        t = self.copy()
        for i in range(len(self.pts)):
            on = i <= upto
            t.dots[i].set_stroke(INK if on else MUTED).set_fill(INK if i == active else BG, 1)
            t.names[i].set_color(INK if on else MUTED)
        return t

    def token(self, i):
        return Circle(radius=0.17).set_stroke(HOT_RING, 3).move_to(self.dots[i].get_center())


# ----------------------------------------------------------------------------------------------------------
def palette_ring(center, radius, colour_at, n=180, width=0.16, base=MUTED):
    """Ring of radius `radius`; colour_at(theta) -> list of colour ids (1 or 2) shown in that direction."""
    g = VGroup(Circle(radius=radius, stroke_color=base, stroke_width=1.5).move_to(center))
    step = TAU / n
    for i in range(n):
        th = i * step
        cs = colour_at(th) or []
        for j, c in enumerate(cs):
            r_in = radius - width / 2 + j * width / max(len(cs), 1)
            seg = AnnularSector(inner_radius=r_in, outer_radius=r_in + width / max(len(cs), 1), angle=step * 1.02,
                                start_angle=th, fill_color=colour(c), fill_opacity=1, stroke_width=0).shift(center)
            g.add(seg)
    return g


# ----------------------------------------------------------------------------------------------------------
def code_panel(code, size=24, width=None):
    lines = code.strip("\n").split("\n")
    t = VGroup(*[Text(l if l.strip() else " ", font=MONO, font_size=size, color=INK) for l in lines])
    t.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    for l, m in zip(lines, t):          # keep indentation
        lead = len(l) - len(l.lstrip(" "))
        m.shift(RIGHT * lead * size * 0.0102)
    return panel(t, pad=0.35)


def paper_card(title, subtitle="", w=3.2, h=4.2):
    page = RoundedRectangle(corner_radius=0.06, width=w, height=h).set_fill("#E9E4DA", 1).set_stroke(width=0)
    t = Text(title, font="Latin Modern Roman", font_size=22, color="#22252B", line_spacing=0.8)
    if t.width > w - 0.5:
        t.scale_to_fit_width(w - 0.5)
    t.move_to(page.get_top() + DOWN * 0.7)
    s = Text(subtitle, font="Latin Modern Roman", font_size=15, color="#55595F").next_to(t, DOWN, buff=0.2) if subtitle else VGroup()
    rows = VGroup(*[Line(LEFT, RIGHT, stroke_color="#B8B3AA", stroke_width=2).set_width(w * (0.75 if i % 4 else 0.55))
                    for i in range(12)]).arrange(DOWN, buff=0.17, aligned_edge=LEFT).next_to(s if subtitle else t, DOWN, buff=0.4)
    rows.align_to(page, LEFT).shift(RIGHT * 0.35)
    return VGroup(page, t, s, rows)


# ----------------------------------------------------------------------------------------------------------
def noise_plane(width=14.4, height=8.2, cell=0.18, colours=(ORANGE, SKY, GREEN), seed=0, opacity=0.85):
    """A 'wild' colouring rendered as fine random cells (illustration: arbitrary colourings have no regions)."""
    rng = np.random.default_rng(seed)
    nx, ny = int(width / cell), int(height / cell)
    g = VGroup()
    for i in range(nx):
        for j in range(ny):
            c = colours[rng.integers(len(colours))]
            g.add(Square(side_length=cell).set_fill(colour(c), opacity).set_stroke(width=0)
                  .move_to([-width / 2 + (i + .5) * cell, -height / 2 + (j + .5) * cell, 0]))
    return g


def hex_tiling(R, ncol, extent=(15, 9), center=ORIGIN, opacity=0.9, stroke=BG):
    """Pointy-top hexagons of circumradius R; ncol = 3 or 7 colour pattern. Returns (group, list of (centre, colour))."""
    g, cells = VGroup(), []
    w = np.sqrt(3) * R
    rows = int(extent[1] / (1.5 * R)) + 3
    cols = int(extent[0] / w) + 3
    pal3 = [ORANGE, SKY, GREEN]
    pal7 = [ORANGE, SKY, GREEN, YELLOW, BLUE, VERMILLION, PURPLE]
    for r in range(-rows // 2, rows // 2 + 1):
        for q in range(-cols // 2 - abs(r) // 2 - 1, cols // 2 + abs(r) // 2 + 2):
            x = w * (q + r / 2)
            y = 1.5 * R * r
            if abs(x) > extent[0] / 2 + R or abs(y) > extent[1] / 2 + R:
                continue
            # axial (q, r): 3-colouring (q - r) mod 3 ; 7-colouring (q + 3r) mod 7  (sublattice 2 - ω, index 7)
            c = pal3[(q - r) % 3] if ncol == 3 else pal7[(q + 3 * r) % 7]
            h = region(RegularPolygon(6, radius=R, start_angle=PI / 2), c, opacity=min(opacity, 0.32))
            h.move_to(np.array(center) + np.array([x, y, 0]))
            g.add(h)
            cells.append((np.array(center) + np.array([x, y, 0]), c))
    return g, cells


def stripes(width=0.8, extent=(15, 9), colours=(ORANGE, SKY), vertical=True, opacity=0.9):
    g = VGroup()
    n = int(extent[0] / width) + 2
    for i in range(-n // 2, n // 2 + 1):
        r = region(Rectangle(width=width, height=extent[1] + 1), colours[i % len(colours)], opacity=min(opacity, 0.32))
        r.move_to([i * width, 0, 0])
        g.add(r)
    if not vertical:
        g.rotate(PI / 2)
    return g


def verdict_row(text, state, note="", width=9.5):
    """A row of the five-terms table: state in {'yes', 'no', 'reported'}."""
    lamp = {"yes": ("✓", ManimColor("#9AD1A8")), "reported": ("✓", ManimColor("#F0C674")),
            "no": ("○", MUTED)}[state]
    a = label(lamp[0], 30, lamp[1], weight="BOLD")
    b = label(text, 28, INK)
    c = label(note, 22, MUTED)
    row = VGroup(a, b, c)
    a.move_to([-width / 2, 0, 0])
    b.next_to(a, RIGHT, buff=0.3)
    c.move_to([width / 2 - c.width / 2, 0, 0])
    return row


# ----------------------------------------------------------------------------------------------------------
from manim import ImageMobject, config as _cfg  # noqa: E402
from manim.utils.images import get_full_raster_image_path  # noqa: F401,E402
from .style import marker, stick  # noqa: E402

_RGB = {i: np.array([int(str(colour(i).to_hex())[k:k + 2], 16) for k in (1, 3, 5)], np.uint8) for i in range(7)}


class WildPlane:
    """A 'wild' colouring of the visible plane: independent random colour per tiny cell, rendered as one image.
    colour_at(point) returns the colour id under a screen point, so clashes shown on screen are genuine."""

    def __init__(self, cell=0.06, colours=(ORANGE, SKY, GREEN), seed=0, dim=1.0):
        self.cell = cell
        self.w, self.h = _cfg.frame_width, _cfg.frame_height
        nx, ny = int(np.ceil(self.w / cell)), int(np.ceil(self.h / cell))
        rng = np.random.default_rng(seed)
        self.ids = np.array(colours)[rng.integers(len(colours), size=(ny, nx))]
        rgb = np.stack([_RGB[int(i)] for i in self.ids.ravel()]).reshape(ny, nx, 3).astype(float)
        bg = np.array([0x0F, 0x10, 0x13], float)
        rgb = (bg + (rgb - bg) * dim).astype(np.uint8)
        self.image = ImageMobject(rgb).set_resampling_algorithm(0)  # nearest
        self.image.stretch_to_fit_width(nx * cell).stretch_to_fit_height(ny * cell)
        self.image.move_to([(nx * cell - self.w) / 2, -(ny * cell - self.h) / 2, 0])
        self.image.set_z_index(-50)

    def colour_at(self, p):
        ix = int((p[0] + self.w / 2) / self.cell)
        iy = int((self.h / 2 - p[1]) / self.cell)
        return int(self.ids[min(max(iy, 0), self.ids.shape[0] - 1), min(max(ix, 0), self.ids.shape[1] - 1)])


def unit_stick(p, angle, S, c1=None, c2=None, size=0.3, width=5):
    """A unit stick: rod of world length 1 (= S manim units) from screen point p at `angle`, pins at both ends."""
    p = np.asarray(p, float)
    q = p + S * np.array([np.cos(angle), np.sin(angle), 0])
    under = Line(p, q, stroke_color=BG, stroke_width=width + 6).set_z_index(-1)   # keeps the rod legible on colour
    return VGroup(stick(p, q, width), marker(c1, size).move_to(p), marker(c2, size).move_to(q), under)


def stick_ends(s):
    return s[0].get_start(), s[0].get_end()


class RegionPlane:
    """A schematic *measurable* colouring: smooth random blobs (blurred noise, then argmax), as one image.
    colour_at(point) returns the colour id under a screen point."""

    def __init__(self, colours=(ORANGE, SKY, GREEN, YELLOW, BLUE), seed=0, res=0.04, blob=0.45, dim=0.42):
        rng = np.random.default_rng(seed)
        self.w, self.h, self.res = _cfg.frame_width, _cfg.frame_height, res
        nx, ny = int(np.ceil(self.w / res)), int(np.ceil(self.h / res))
        field = rng.random((len(colours), ny, nx))
        k = max(1, int(blob / res))
        for _ in range(3):  # box blur ×3 ≈ gaussian
            for ax in (1, 2):
                c = np.cumsum(field, axis=ax)
                c = np.concatenate([np.zeros_like(np.take(c, [0], axis=ax)), c], axis=ax)
                hi = np.clip(np.arange(field.shape[ax]) + k, 0, field.shape[ax])
                lo = np.clip(np.arange(field.shape[ax]) - k, 0, field.shape[ax])
                field = (np.take(c, hi, axis=ax) - np.take(c, lo, axis=ax)) / (hi - lo).reshape(
                    [-1 if i == ax else 1 for i in range(3)])
        self.ids = np.array(colours)[np.argmax(field, axis=0)]
        rgb = np.stack([_RGB[int(i)] for i in self.ids.ravel()]).reshape(ny, nx, 3).astype(float)
        bg = np.array([0x0F, 0x10, 0x13], float)
        rgb = (bg + (rgb - bg) * dim).astype(np.uint8)
        self.image = ImageMobject(rgb)
        self.image.stretch_to_fit_width(nx * res).stretch_to_fit_height(ny * res)
        self.image.move_to([(nx * res - self.w) / 2, -(ny * res - self.h) / 2, 0]).set_z_index(-50)

    def colour_at(self, p):
        ix = int((p[0] + self.w / 2) / self.res)
        iy = int((self.h / 2 - p[1]) / self.res)
        return int(self.ids[min(max(iy, 0), self.ids.shape[0] - 1), min(max(ix, 0), self.ids.shape[1] - 1)])
