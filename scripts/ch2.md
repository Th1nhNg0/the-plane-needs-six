# Chapter 2 · Geometry becomes a graph (target 6:00)

## S2.1 · Dots and sticks
`id: s2_1` · `target: 1:10` · `time: 4:12–5:28 (est.)`

**NARRATION**
> Here's the shift in perspective. The rule only ever talks about pairs of points at distance one, so let's draw exactly that. [beat] Every point is a dot. Every pair of dots at distance one gets joined by a stick. [beat] Do that for all the points of the plane at once, and you get an impossibly dense web: each dot is joined to an entire circle of others. [beat] A structure like this, dots and the links between them, is called a graph. The dots are its vertices. The sticks are its edges. [beat] A colouring that never puts the same colour on both ends of an edge is called a proper colouring. And the fewest colours that allow a proper colouring is the graph's chromatic number. [beat] So our question has a name: what is the chromatic number of the plane? It's usually written with the Greek letter chi. [beat] Notice that we haven't changed the problem at all, only how we look at it. And the new view has a big advantage: we can study small pieces of the web.

**VISUAL**
1. One dot; a unit circle of radius 1 is drawn around it; sticks fan out to ~24 points on the circle. → cue 1–2
2. More dots each get their own fan; the web densifies into a shimmering mesh (sampled, not all edges). → cue 3
3. A small 6-dot subgraph lifts out of the mesh; labels "vertex" and "edge" attach with leader lines. → cue 4
4. Its vertices get colours; one edge with equal ends flashes; recolour it to fix: "proper". → cue 5
5. Formula appears: χ(ℝ²). The ℝ² glyph briefly shows the plane icon. → cue 6
6. The subgraph slides back into the web; a magnifier ring roams over the web. → cue 7

**ON-SCREEN**
- "vertex" · "edge" · "proper colouring: no edge with equal ends" · "chromatic number = fewest colours"
- $\chi(\mathbb{R}^2)$, read as "chi of the plane"

**SOURCE**
- Graph formulation: P §1 para 1; brief §1.

**MUST UNDERSTAND**
- Vocabulary: vertex, edge, proper colouring, chromatic number, χ(ℝ²).

## S2.2 · The triangle, renamed
`id: s2_2` · `target: 0:40` · `time: 5:28–5:57 (est.)`

**NARRATION**
> The smallest interesting piece is the triangle from before: three vertices, every pair joined. [beat] Any proper colouring of the whole plane is, in particular, a proper colouring of these three points. So it uses at least three colours. [beat] In the new language: the triangle has chromatic number three, so the chromatic number of the plane is at least three. [beat] Can a slightly bigger drawing force four?

**VISUAL**
1. The triangle lifts out of the web with its 3 colours. → cue 1
2. The web behind it greys out; the triangle's colours "come from" the plane via short vertical leader lines. → cue 2
3. The number line appears at the bottom with a left marker at 3. → cue 3
4. A second triangle slides next to the first, sharing an edge. → cue 4

**ON-SCREEN**
- $\chi(\mathbb{R}^2) \ge 3$

**SOURCE**
- Standard.

**MUST UNDERSTAND**
- A finite subgraph's chromatic number is a lower bound (stated informally here; S2.4 makes it explicit).

## S2.3 · The spindle  ← PILOT SCENE
`id: s2_3` · `target: 2:00` · `time: 5:57–7:50 (est.)`

**NARRATION**
> Glue two triangles along an edge, and you get a diamond: a rhombus with four vertices. Let's colour it with three colours. [beat] The two shared vertices in the middle must differ: say blue and green. The top tip is joined to both of them, so it has to be the third colour, orange. The bottom tip is joined to the same two, so it must also be orange. [beat] So in every three-colouring, the far tips of this diamond are forced to share a colour. And they're allowed to: they're the square root of three apart, about one point seven three, not one. [beat2] Now take a second diamond, pinned at the same bottom tip. By the same argument, its far tip must also match the pin. So both far tips are forced to be orange. [beat] Here's the trick. Rotate the second diamond around the shared point. Both far tips stay root three from the pin, so as we turn, the distance between them changes. [beat] Watch it shrink, [beat] until it's exactly one. [beat2] Now those two tips are joined by an edge, so they must be different. Yet each one was forced to match the pin. [beat] With three colours, it's impossible. [beat] This figure, seven vertices and eleven edges, is called the Moser spindle, after the brothers Leo and William Moser, who published it in 1961. [beat] And you don't have to trust the argument. There are only three to the seventh, that's two thousand one hundred and eighty-seven, ways to three-colour seven points, and every single one breaks an edge. With four colours, it works.

**VISUAL**
1. Two unit triangles glue along an edge into a rhombus (pins labelled by position: top, middle-left, middle-right, bottom). → cue 1
2. Middle pins colour sky ▲ and green ■; the top pin cycles orange/sky/green, rejecting sky and green with small clash sparks, and settles on orange ●. Same for the bottom pin. → cue 2
3. A dashed line joins top and bottom tips; the distance indicator reads 1.732 = √3; the label "forced equal" appears. → cue 3
4. A second rhombus (dashed outline style, like the paper's figure but our palette) appears sharing the bottom pin, overlapping the first; its far tip turns orange by the same propagation (fast replay). → cue 4
5. The second rhombus rotates about the shared pin. A dashed segment between the two far tips carries a live distance indicator: 1.732 → … (the far tips trace a circle of radius √3 about the pin). → cue 5–6
6. The rotation eases to the exact angle where the readout reaches 1.000 (rotation angle arccos(5/6) ≈ 33.56°). The dashed segment becomes a solid unit stick. → cue 7
7. Both ends of the new stick are orange: clash spark; the two "forced equal" labels pulse. → cue 8–9
8. The figure tidies into the standard spindle drawing; counters "7 vertices · 11 edges"; label "Moser spindle (1961)". → cue 10
9. Fast-forward grid: 2187 tiny spindles in a 3-colour sweep, each flashing its clash; counter runs to 2187/2187 "all fail". Then one spindle recolours with a 4th colour (yellow ◆) and every edge is satisfied: ✓. → cue 11

**ON-SCREEN**
- "forced equal" · $|{\rm tip}-{\rm tip}| = \sqrt{3}\approx 1.732$ · live distance readout
- "Moser spindle · 7 vertices · 11 edges · L. & W. Moser, 1961"
- "$3^7 = 2187$ colourings, all fail" · "4 colours: ✓"
- Number-line left marker moves 3 → 4: $\chi(\mathbb{R}^2)\ge 4$ (shown at the end of S2.4, not here)

**SOURCE**
- Spindle construction and forcing argument: P §8.5 (text after eq. Moser vectors); MoserMoser1961.
- 7 vertices, 11 edges; brute force 3^7 all fail, 4-colourable: our check, `tools/verify_moser_certificate.py` (brief §6).
- Rotation angle with cosine 5/6 (u = (5 + i√11)/6): P §8.5.

**MUST UNDERSTAND**
- The rhombus forces its tips to match; rotating creates a unit edge between two forced-equal points; so 3 colours fail.

## S2.4 · Stamping
`id: s2_4` · `target: 1:30` · `time: 7:50–9:01 (est.)`

**NARRATION**
> Why does a little figure say anything about the infinite plane? [beat] Imagine any colouring of the plane with three colours, as wild as you like. Now set the spindle down on it, as a rigid stamp. Each of its seven vertices lands on a point of the plane and picks up that point's colour. [beat] Its edges really are distance one in the plane, so the plane's rule says every edge must get two different colours. In other words, the plane's colouring hands us a proper three-colouring of the spindle. [beat] But we just saw that no such thing exists. So the stamp always finds a broken edge, wherever we put it, whatever the colouring. Three colours can't work for the plane. [beat2] This is the logic to remember. If some finite drawing made of unit edges needs N colours, the whole plane needs at least N. [beat] One small certificate, placed anywhere, and the infinite plane inherits its stubbornness. The chromatic number of the plane is at least four.

**VISUAL**
1. The spindle (outline only) hovers over three different 3-coloured planes in turn: random noise, 3-colour hexagons, wavy bands. → cue 1
2. It drops onto the noise plane; vertical leader lines carry colours up into its 7 pins. → cue 2
3. Each edge evaluates; at least one flashes a clash. → cue 3
4. The stamp slides continuously over each plane; the clash marker jumps from edge to edge but never disappears. → cue 3 (continued)
5. Text logic: "finite unit graph needs N ⇒ plane needs ≥ N". → cue 4
6. Number line: marker moves from 3 to 4. → cue 5

**ON-SCREEN**
- "graph $G$ drawn with unit edges, $\chi(G)=N$ ⟹ $\chi(\mathbb{R}^2)\ge N$"
- $\chi(\mathbb{R}^2)\ge 4$

**SOURCE**
- Restriction argument: standard; P §1 (finite obstructions); brief insight I3.

**MUST UNDERSTAND**
- Any plane colouring restricts to a colouring of any placed unit-distance graph.

## S2.5 · Is there a ceiling?
`id: s2_5` · `target: 0:40` · `time: 9:01–9:18 (est.)`

**NARRATION**
> This suggests a strategy: find bigger, cleverer unit-distance graphs that need five colours, then six, then more. [beat] If that worked forever, the plane would need infinitely many colours. [beat] It doesn't. There's a ceiling, and it's beautiful.

**VISUAL**
1. Several spindles snap together into a larger, denser cluster; the number line's left marker hops hopefully toward 5, 6 … → cue 1
2. A wall drops onto the number line at 7. → cue 2–3

**ON-SCREEN**
- Number line with marker at 4 and a question mark sliding right; a wall at 7 labelled "ceiling?".

**SOURCE**
- Upper bound 7: P §1 (proof of Thm 1.1).

**MUST UNDERSTAND**
- There's an upper bound to come.
