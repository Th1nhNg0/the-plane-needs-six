# Chapter 4 · Why 6 is harder (target 5:30)

## S4.1 · One example versus every possibility
`id: s4_1` · `target: 1:20` · `time: 14:38–15:39 (est.)`

**NARRATION**
> Think about what a proof of "six" needs. To show that five colours fail for a graph, you have to rule out every five-colouring. If the graph has a thousand vertices, that's five to the power one thousand candidate colourings. [beat] And before that, the graph itself has to be found, among unimaginably many ways to arrange unit distances in the plane. [beat] Compare that with the other direction. To show that a colouring works, you just show it: one example, and anyone can check it. [beat] Proving that something does not exist is a fundamentally different kind of task. Solvers can turn it into certificates, once a graph is given and small enough. But someone still has to find a graph rigid enough to force six colours, and small enough to check. [beat] From 2018 until the preprint we're about to discuss, the lower bound stayed at five.

**VISUAL**
1. Left panel "exists": one coloured graph and a single ✓. Right panel "none exists": the same graph with an exploding fan of colourings, counter $5^{1000}$. → cue 1
2. Behind the right panel, a haystack of random unit-distance configurations; a needle icon with "?". → cue 2
3. The left panel's ✓ stays crisp. → cue 3
4. The right panel compresses into a certificate scroll, but only after a "find the graph first" gate that stays closed. → cue 4
5. Number line [5, 7] with a calendar ticking 2018 → 2026. → cue 5

**ON-SCREEN**
- "one example ✓" vs "rule out all $5^{1000}$" · "first: find the graph"

**SOURCE**
- Asymmetry: standard; certificates: Heule2018 §3. Bound unchanged: P §1 para 3.

**MUST UNDERSTAND**
- Existence vs non-existence asymmetry; the bottleneck is finding the graph.

## S4.2 · Colourings you can't draw
`id: s4_2` · `target: 2:20` · `time: 15:39–17:50 (est.)`

**NARRATION**
> There's a second, deeper obstacle, and it's hiding in the word "any". [beat] Every colouring we've drawn so far is made of regions: hexagons, stripes, blobs with borders. You could measure the area of each colour. But the rule allows any assignment of colours to points, and most of those can't be drawn at all. [beat] Here's a toy problem that shows how strange this gets. Forget the plane; take a circle. Fix an angle that's an irrational fraction of a full turn, say root two over ten. The rule: any two points separated by exactly that angle must get different colours. [beat] Can two colours work? Start anywhere and hop around the circle by that angle: first point orange, next blue, next orange, and so on. Because the angle is irrational, you never land on the same point twice, and the hops spread out densely over the whole circle. [beat] Each chain of hops can be coloured by alternating, and the axiom of choice lets you pick a starting point for every chain at once. So yes: two colours work. [beat2] But try to draw that colouring. Alternating means that hopping twice brings you back to the same colour. So the colouring is unchanged when you rotate the whole circle by twice the angle, which is itself an irrational rotation. [beat] And any colouring with honest areas that's unchanged by an irrational rotation has to be, essentially, a single colour, which flatly contradicts alternating. [beat] So on this circle, two colours suffice if colourings can be arbitrary, but no colouring with well-defined areas works at all. [beat] Sets that do have a well-defined area are called measurable. And this gap, between what's possible arbitrarily and what's possible measurably, is exactly the gap a proof about the plane has to cross. Keep this toy in mind: a version of its trick shows up deep inside the new proof.

**VISUAL**
1. Gallery of drawn colourings (hexagons, stripes, blobs) each with an area bar chart per colour. → cue 1–2
2. `TOY PROBLEM` tag. A circle; an arc of angle α = √2/10 turn drawn as a chord-hop arrow; "differ by α ⇒ different colours". → cue 3
3. Hopping: points appear one by one, alternating orange ● / sky ▲, spiralling around; after ~200 hops the circle looks densely speckled in both colours. → cue 4
4. Several chains in different greys start at different points; each alternates; a hand-icon "choice" picks starting points for all. Caption "2 colours ✓ (arbitrary)". → cue 5
5. Attempt to render the full colouring: the circle becomes unresolvable static; a magnifier zooms in and the static never resolves into regions. → cue 6
6. Double-hop arrow 2α; the speckled circle rotates by 2α and looks identical ("unchanged"). → cue 6 (continued)
7. Measurable side: a circle with real coloured arcs is rotated by 2α repeatedly; the arcs smear; the time-average converges to a uniform blend: "invariant ⇒ constant". → cue 7
8. Two-column verdict: "arbitrary: 2 colours ✓" | "measurable: impossible ✗". → cue 8
9. Word "measurable = has a well-defined area" appears; the circle shrinks into a corner icon that will reappear in S5.4. → cue 9

**ON-SCREEN**
- `TOY PROBLEM` · $\alpha = \tfrac{\sqrt2}{10}$ turn · "$\theta$ and $\theta+\alpha$ get different colours"
- "arbitrary: 2 ✓ · measurable: ✗" · "measurable = has a well-defined area"

**SOURCE**
- Toy is ours (brief §11 T2). Mechanism (invariance under an irrational rotation forces a.e. constancy) is used in the paper at Lemma 6.4 (cos γ = 5/6, γ/π irrational).
- Choice-based construction: standard (selection of orbit representatives).

**MUST UNDERSTAND**
- "Can be coloured" and "can be coloured with measurable regions" are different questions.

## S4.3 · What was known for nice colourings
`id: s4_3` · `target: 1:20` · `time: 17:50–18:53 (est.)`

**NARRATION**
> This isn't just a toy worry. If you assume the colour regions are measurable, much more has been known for a long time. [beat] In 1981, Kenneth Falconer proved that measurable colourings of the plane need at least five colours, thirty-seven years before de Grey reached five for arbitrary ones. [beat] If the regions are like the countries of a map, with reasonable borders, Townsend showed that six are needed. And in 2025, Georgy Sokolov and Vsevolod Voronov showed that colourings by polygons need all seven. [beat] But none of these settle the real question, which allows any colouring. [beat] And there's a cautionary example, from Michael Payne in 2009. Take the points of the plane, but join only some of the unit-distance pairs. That graph can be properly coloured with just two colours if anything goes, yet needs at least five if the colour classes must be measurable. Similar-looking constraints, wildly different answers.

**VISUAL**
1. The number line splits into two tracks: top "any colouring", bottom (ghosted) "nice colourings". → cue 1
2. Bottom track: chip "measurable ≥ 5 (Falconer 1981)". A curved arrow to the top track's 2018 chip: "37 years later". → cue 2
3. Bottom track: "map-type ≥ 6 (Townsend)", "polygons ≥ 7 (Sokolov–Voronov 2025)" with tiny icons (map, polygon tiling). → cue 3
4. The top track stays at [5, 7]; a gap between tracks shimmers. → cue 4
5. Payne's example: a sparse sub-web (only some unit pairs) with a 2-colour "arbitrary" label ✓ and a "measurable ≥ 5" label. → cue 5

**ON-SCREEN**
- "measurable ≥ 5 (1981)" · "map-type ≥ 6" · "polygonal ≥ 7 (2025)" · "Payne 2009: 2 vs ≥ 5"

**SOURCE**
- P §1 paras 4–5 (Falconer1981; Woodall1973; Townsend1981/2005; SokolovVoronov2025; Payne2009).

**MUST UNDERSTAND**
- Strong bounds existed only under regularity assumptions; arbitrary ≠ measurable in general.

## S4.4 · Two roads
`id: s4_4` · `target: 0:30` · `time: 18:53–19:14 (est.)`

**NARRATION**
> So to reach six for all colourings, there seemed to be two roads. Find a much bigger finite graph, and certify it. Or find a way to tame arbitrary colourings, so that the strong tools for measurable ones apply. [beat] The preprint we're about to explore takes the second road.

**VISUAL**
1. A fork: left road "find a bigger graph" (fades into fog), right road "tame wild colourings" (lit). → cue 1
2. Camera walks down the right road into Chapter 5. → cue 2

**ON-SCREEN**
- "road 1: bigger finite graph" · "road 2: tame arbitrary colourings"

**SOURCE**
- P §1.1 opening ("The two parts of the proof address different obstacles…").

**MUST UNDERSTAND**
- The new proof's strategic choice.
