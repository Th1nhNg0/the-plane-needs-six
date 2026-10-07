# Chapter 5 · The new proof (target 13:00)

Persistent element: the **proof map rail**, 7 stations redrawn from the paper's Fig 1:
`proper 5-colouring → symmetric random colouring → smooth part → weak measurable colouring → palettes ≤ 2 → threads on a 3/4/5-cycle → three cases → contradiction`.
Corner caption for the whole chapter: "simplified · full argument: 62 pages".

## S5.0 · The map
`id: s5_0` · `target: 0:50` · `time: 19:14–20:04 (est.)`

**NARRATION**
> Before diving in, here's the map. The argument is a proof by contradiction: suppose a proper five-colouring of the plane exists, and derive something impossible. [beat] It runs in two halves. The first half tames: it shows that if any proper five-colouring existed, then a measurable one would exist too, in a slightly relaxed sense. The second half traps: it shows that no such measurable colouring can exist, using geometry and topology. [beat] We'll travel along this line, one station at a time. And a fair warning: the paper is sixty-two pages of dense mathematics. What follows keeps the logic of each step but simplifies the path, and I'll say clearly where I'm only describing an idea rather than showing it.

**VISUAL**
1. "Assume: a proper 5-colouring exists" card; the rail draws itself left to right. → cue 1
2. The first four stations tint "TAME"; the last four tint "TRAP". → cue 2
3. A small train token sits at station 1. The "simplified" corner caption fades in. → cue 3

**ON-SCREEN**
- Rail station labels (as above); "TAME" bracket, "TRAP" bracket.

**SOURCE**
- P Fig 1 (proof-flow), P §1 ("The proof has two parts…").

**MUST UNDERSTAND**
- Proof by contradiction; two halves.

## S5.1 · Taming wild colourings: the transfer
`id: s5_1` · `target: 2:40` · `time: 20:04–22:42 (est.)`

**NARRATION**
> Start with an arbitrary proper five-colouring, as wild as the circle toy. [beat] The first move is averaging. Take the colouring, and also every shifted copy and every rotated copy of it, and blend them together. [beat] Any single wild colouring may have no sensible structure. But the blend is symmetric: it looks the same everywhere and in every direction. Technically, it becomes a random colouring whose statistics don't care where you stand or which way you face. And since every copy obeyed the rule, the random colouring obeys it too. [beat] Next, split each colour's pattern into two parts. One part is smooth: shifting it a tiny bit changes it only a tiny bit. The other part is everything else. [beat2] Here the most technical theorem of the paper enters: a rigidity theorem, built with tools from ergodic theory and number theory. A loose analogy, not the theorem itself: think of a signal with static on top. Because the random colouring is symmetric under all those rotations, the "everything else" part is forced to behave like perfect static. It has zero correlation with any shifted copy of itself. [beat] That's exactly what's needed. The rule "points one apart differ" can be written as a correlation that equals zero. Removing perfect static doesn't change correlations at distance one, so the smooth part still obeys the rule, on average. And from the smooth part, one can pick out an ordinary colouring with genuine areas. [beat] This is exactly where the full rotational symmetry of the plane matters. Payne's example is a reminder that a step like this can't be taken for granted. [beat] What comes out is what the paper calls a weak measurable colouring: every colour region has a well-defined area, and same-colour pairs at distance one are allowed only on a negligible set, of total size zero. [beat] It works backwards too. Keep only the typical points, those surrounded, at every small scale, almost entirely by their own colour, and the exceptions vanish. Compactness then rebuilds a proper colouring. [beat] So the transfer theorem says: a proper colouring with k colours exists if and only if a weak measurable one does, for every number of colours, not just five. [beat] That's half of the proof. From here on, we're allowed to talk about areas.

**VISUAL**
1. Rail: train at station 1. A static-like "wild" 5-colouring fills a framed window. → cue 1
2. Copies of the window slide out, shifted and rotated, stacking translucently; the stack blends into a soft colour field. → cue 2
3. The blended field: moving a small "you are here" compass across it and rotating it doesn't change a statistics panel (five bars). → cue 3
4. 1-D cross-section strip of one colour's pattern (orange indicator): splits into "smooth" (a gentle curve) + "everything else" (jagged). → cue 4
5. `ANALOGY` tag. Signal + static audio-style waveform. A correlation dial labelled "correlation with shifted copy" for the static part reads 0 at every shift (a shift slider moves, dial stays at 0). → cue 5
6. Correlation dial at "distance 1": whole pattern 0, smooth part 0, static 0. → cue 6
7. Small Payne icon from S4.3 pops in with "rotations matter". → cue 7
8. Definition card for the weak measurable colouring; a heat-map of rare "clash pairs" collapses to a thin dust labelled "total size 0". → cue 8
9. Zoom on a point inside an orange region; nested circles show ~100% orange: "typical point". Dust pairs disappear among typical points. → cue 9
10. Theorem card (transfer). Rail: train moves to station 4; stations 1–4 lit. → cue 10–11

**ON-SCREEN**
- `ANALOGY` on the signal/static panel.
- Definition: "weak measurable colouring: measurable colour regions; same-colour unit pairs only on a set of size 0"
- Theorem (words): "proper $k$-colouring exists ⟺ weak measurable $k$-colouring exists (every $k$)"
- Small: "rigidity theorem (ergodic theory, number fields): not shown"

**SOURCE**
- Averaging: P Prop 4.2 (invariant law via Følner averaging over E ⋊ K).
- Split and conditional expectation: P Lemma 4.1. Rigidity: P Thm 2.3 (§§2–3). Zero correlation of remainder: P Prop 4.2.
- Measurable sample: P Prop 4.2 "A measurable sample". Definition: P Def 1.2.
- Converse: P Lemma 4.3 and proof of Thm 1.3. "Every k": P Thm 1.3.
- Analogy limits: brief §10.

**MUST UNDERSTAND**
- The transfer converts any proper colouring into a measurable one with negligible violations (and back), so geometric/area arguments become legitimate.

## S5.2 · The ring around a point: palettes
`id: s5_2` · `target: 2:20` · `time: 22:42–24:21 (est.)`

**NARRATION**
> Now suppose a weak measurable five-colouring exists. Stand at a point, call it x, and look at the circle of radius one around it. [beat] In each direction, ask which colours appear at that spot on the ring. The paper calls this the palette in that direction. Technically, it's defined through limits, to cope with messy boundaries, but "the colours you see there" is the right picture. [beat] Now an old friend returns: the diamond. Take a direction, and the directions sixty degrees to either side of it. The point on the ring in our direction is exactly one unit from the points on the ring sixty degrees away: that's the diamond, with its tips at the centre and on the ring. [beat] With some care about those limits, the conclusion is: directions sixty degrees apart can never share a palette colour. [beat2] From there, the paper proves something much stronger. In almost every direction, the palette holds at most two colours. [beat] Roughly: if three colours crowded into one direction, the ring around that spot would be left with only the other two. The paper shows that such two-colour centres must keep a fixed distance from each other, yet this situation would pack infinitely many of them onto one circle. [beat] And when only two colours are available around a centre, the sixty-degree rule forces them to swap at every sixty-degree step: six petals, alternating. Keep that flower in mind.

**VISUAL**
1. Rail: train at station 5. A smooth-ish 5-coloured measurable map; a centre x with a unit ring (the PaletteRing component). → cue 1
2. A direction arrow sweeps; at each angle a small chip on the ring shows the colour(s) present. A footnote chip: "defined by limits". → cue 2
3. The unit rhombus snaps in: vertices x, x + R f, x + f, x + R⁻¹f (two unit triangles), showing x + f is 1 from x + Rf and from x + R⁻¹f. → cue 3
4. Palette chips at f and f ± 60° show disjoint colour sets; a "≠" glyph between them. → cue 4
5. Counter on the palette chip: "≤ 2". → cue 5
6. Sketch of the "three colours in one direction" scenario: around x + e, a second ring sees only two colours; several such centres pack onto the circle x + S¹ and a "too close" warning spark fires between neighbours. → cue 6
7. A ring with only two colours (orange, sky) alternating in six 60° petals. → cue 7

**ON-SCREEN**
- "palette $P_x(e)$ = colours seen at $x+e$ (in a limiting sense)"
- $x+f = x+R f + R^{-1} f$ with $R$ = rotate 60°
- "palettes 60° apart are disjoint" · "palette size ≤ 2"

**SOURCE**
- Palettes: P Def 5.1. Palette transfer: P Lemma 5.2. Sixty-degree exclusion: P Cor 5.4.
- Binary-centre separation: P Lemma 5.5. Size ≤ 2: P Prop 5.6. Alternation: P §5.3.

**MUST UNDERSTAND**
- At each direction at most two colours; 60° neighbours disjoint; two-colour rings alternate in six sectors.

## S5.3 · Blur, loop, threads
`id: s5_3` · `target: 2:50` · `time: 24:21–27:05 (est.)`

**NARRATION**
> Palettes are local. To get a contradiction, we need to find a special point, and for that the paper turns to topology. [beat] First, blur the colouring slightly: replace each point's colour by the mix of colours in a tiny disk around it. Now every point carries a recipe, like sixty percent orange and forty percent blue. Small amounts get trimmed away. [beat] Draw the five colours as the corners of a pentagon, and join every pair: ten edges. A pure orange point sits at the orange corner. A point mixing orange and blue sits somewhere along the orange–blue edge. [beat] The paper shows that, apart from tiny holes that can be patched, and a few special points, no point mixes more than two colours. So the blurred plane maps continuously onto this network of edges. [beat2] Now a fact about flat space. Try to cover a big floor with small tiles so that nowhere do three tiles meet. With squares, four meet at the corners. With hexagons, three. You can't avoid it: in two dimensions, small pieces covering a region always meet in threes somewhere. [beat] The paper uses a precise version of this. Each colour region of the blurred map has to be small, roughly less than one across, because of the unit-distance rule, and only two can overlap at any point. On a large square, that's impossible. [beat] The way out is the special points. Somewhere there must be a special point where, if you walk a small loop around it, your recipe travels around a genuine cycle of colours on the network, through three colours, or four, or five, and back to the start. [beat] Each edge of that cycle leaves a trace: a connected thread, running out from the special point, along which two colours meet half and half. [beat] And here's why threads are powerful. Take any point that is less than one unit from part of a thread and more than one unit from another part. The thread is connected, so somewhere along it, the distance is exactly one. The paper shows this excludes both of the thread's colours from that whole region. [beat] So now we have a special point, with three, four or five threads coming out of it, each banning two colours just inside and just outside the unit circle around it. [beat] Three cases. Each one has to fail.

**VISUAL**
1. Rail: train moves to station 6. → cue 1
2. A 5-coloured measurable map; a small disk cursor blurs it into a soft field; a hover readout shows a recipe "60% ● · 40% ▲". → cue 2
3. Five corner dots (with glyphs) as a pentagon; all 10 edges drawn (pentagon + pentagram), labelled "K₅" only in small type. → cue 3
4. Live mapping: dots sampled from the blurred plane fly to positions on edges/corners of the K₅ diagram; a few tiny holes on the map get circular patches. → cue 4
5. `TOY PROBLEM` tag. Floor tiling montage: square tiles (4-point corners glow), hexagonal tiles (3-point corners glow), a brick wall (3-point T-junctions glow); an attempt with "only 2 meet" fails with a highlighted triple point. → cue 5
6. Statement card: "colour regions < ~1 across, at most 2 overlapping: impossible on a big square". → cue 6
7. A special point (small ring marker); a loop is walked around it; on the K₅ diagram a tracer runs around a triangle (then, as alternatives, a 4-cycle and a 5-cycle shown faintly). → cue 7
8. From the special point, three threads (irregular connected curves, deliberately not straight, matching the paper's caveat) grow outward, each labelled with its two colours. → cue 8
9. Straddle zone (redrawn Fig 2): a thread K, a test point z, a compass of radius 1 around z crosses K; the distance readout along K sweeps from < 1 to > 1 and hits 1.000 at a point p. Region shading "both colours banned". → cue 9
10. Final composite: special point, 3–5 threads, banned bands just inside and outside the unit circle. → cue 10–11

**ON-SCREEN**
- "recipe = mix of colours in a tiny disk" · "at most 2 colours mixed (away from a few special points)"
- $\Delta(K)=\{z:\ \min_{q\in K}|z-q|<1<\max_{q\in K}|z-q|\}$ (shown briefly, in words underneath: "too close to part of the thread, too far from another part")
- Caption under threads: "shape schematic"

**SOURCE**
- Disk averages: P §7.1, Lemma 7.2. Graph-valued map, holes: P eq (7.3), Lemmas 7.3–7.4. Cyclic centres locally finite: P Thm 6.5.
- Cover obstruction: P Lemma 7.5 (side-10 square, multiplicity ≤ 2, mesh ≤ 2). Non-null loop: P Lemma 7.6. Simple cycle: P Lemma 7.7. Threads: P Lemma 7.8, Prop 7.1.
- Straddle zone and exclusion: P eq (7.1), Fig 2, Prop 7.1(3). One-sided strips: P Lemma 8.1.
- Tiles analogy: brief §11 T4 (ours).

**MUST UNDERSTAND**
- There is a special centre with a cycle of 3, 4 or 5 colour-pair threads, and each thread bans its two colours in nearby zones.

## S5.4 · Three cases
`id: s5_4` · `target: 3:20` · `time: 27:05–31:06 (est.)`

**NARRATION**
> Five threads first. Here the paper shows that in every direction, the palette must be one of the pentagon's diagonal pairs: some colour together with the colour two steps along. Label these five diagonals zero to four, like the hours on a five-hour clock. [beat] Now walk around the ring in six steps of sixty degrees. Neighbouring directions need disjoint palettes, and two diagonals are disjoint exactly when their labels differ by one. So each step moves the clock hand by plus one or minus one. After six steps you're back where you started, so the steps must add up to a multiple of five. [beat] The threads add one more rule: opposite directions, three steps apart, must have labels that differ by zero or by two. But three steps of plus or minus one add up to three, one, minus one or minus three. On a five-hour clock, three is the same as minus two, and minus three is plus two. So only triples where all three steps go the same way are allowed. [beat] Every run of three steps points the same way, so all six steps do. And six equal steps add up to six, or minus six, neither of which is a multiple of five. [beat] Contradiction. Five threads are impossible, and this step is essentially the paper's own argument, in full. [beat2] Four threads. Now each palette is either the fifth, unused colour, or one of two diagonal pairs of the four-cycle. Following six directions around the ring, the positions holding the fifth colour turn out to be all even, or all odd. That gives each starting direction a parity bit. [beat] Some geometric lemmas, which I'll skip, show that this bit can't change as you turn the starting direction slowly. But turning by exactly sixty degrees shifts every position by one, and flips the parity. A bit that can never change, and must flip. Contradiction. [beat2] Three threads is the last case, and the most satisfying. Call the three colours on the cycle the triangle colours; two colours are left over. [beat] Near the unit circle around the special point, the threads ban the triangle colours from thin strips, and the leftover colours take over. The paper shows that the two leftovers alternate in six sectors of exactly sixty degrees: the flower again. [beat] Now combine. A point near the centre can be reached as the sum of two unit steps. If those two steps land in sectors with different leftover colours, then the point is exactly one unit from a spot of each leftover colour, so neither leftover can be used near it. Only the three triangle colours remain. [beat] The paper pins down exactly where this happens, a region described by one polynomial inequality, shaded here. So near the special point, there's an open region where the colouring uses only three colours. [beat2] And we know a figure that cannot be coloured with three colours. [beat] Take the Moser spindle from 1961. Rotate it by an angle whose cosine is thirty-five over thirty-seven, shift it, and set it down. All seven vertices land inside the three-colour region. [beat] The paper checks this with exact fractions, in a short table you can verify by hand. I re-checked it with exact arithmetic: every vertex is strictly inside. [beat] So the region would contain a properly three-coloured Moser spindle, which is impossible. The three-thread case collapses, and the little figure that proved "at least four", sixty-five years earlier, delivers the final blow.

**VISUAL**
1. Rail: train at station 7, first sub-light "5". Pentagon of colours; five diagonals highlighted one by one, labelled 0–4 on a 5-hour clock face. → cue 1
2. A hexagonal ring of 6 slots (directions at 60° steps). A token moves slot to slot; the clock hand steps ±1 each time; a running sum counter. → cue 2
3. Opposite slots connected by a dashed chord with the rule "difference ∈ {0, ±2}". A table of three-step sums: +3, +1, −1, −3 → mod 5: 3≡−2 ✓, 1 ✗, −1 ✗, −3≡2 ✓. → cue 3
4. All six arrows forced to the same direction; sum 6 shows "6 mod 5 = 1 ≠ 0" ✗. → cue 4
5. "5: ✗" stamped on the rail. → cue 5
6. Four threads: ring of 6 slots; states shown as X (the fifth colour) or one of two diagonals U, V; X positions highlighted all on even slots; a parity lamp "even". → cue 6
7. Starting direction rotates slowly: lamp stays "even" (a small "geometric lemmas skipped" tag). Rotate by exactly 60°: slots shift by one, lamp flips to "odd": clash spark. "4: ✗". → cue 7
8. Three threads: the special point with three threads; the triangle colours (orange ●, sky ▲, green ■) and leftovers (yellow ◆, blue ⬟). Thin bands just inside/outside the unit circle fill with yellow/blue. → cue 8–9
9. Six 60° sectors alternate yellow/blue around the centre: the flower. → cue 9 (continued)
10. A point z near the centre; two unit vectors from the centre summing to z, endpoints landing in a yellow sector and a blue sector; both leftover colours greyed out near z. → cue 10
11. The polynomial region (shaded, derived from P < P′) appears; caption "only 3 colours here". → cue 11
12. The Moser spindle from Ch 2 flies in (same styling), rotates by arccos(35/37) ≈ 18.9°, translates; its 7 vertices settle inside the shaded region (each gets a small ✓). → cue 12–13
13. A small "exact check ✓" badge links to the certificate table (ghosted fractions). → cue 14
14. The vertices attempt a 3-colouring with triangle colours; a clash spark on the edge $z_T z_{uT}$. "3: ✗". Ch 2 thumbnail flashes beside it: "1961 → 2026". → cue 15

**ON-SCREEN**
- Five threads: "$D_i=\{i,\,i+2\}$ (mod 5)" · "steps $\pm1$" · "$\sum$ of 6 steps $\equiv 0 \pmod 5$" · "opposite: difference $\in\{0,\pm2\}$"
- Four threads: "parity of the fifth colour's positions" · "geometric lemmas skipped"
- Three threads: "leftover colours alternate in six 60° sectors" · region: $y^2(3x^2-y^2)^2 < r^6\,(1-\tfrac{r^2}{4})(r^2-1)^2,\ r^2=x^2+y^2$ (small) · "placement: rotate by $\tfrac{35+12i}{37}$, shift by $\tfrac{-290+149i}{250}$"
- "exact check: all 7 vertices strictly inside ✓"

**SOURCE**
- Five-cycle: P Prop 8.2 (verified by brute force over all 2⁶ step words: no valid closing word; production note).
- Four-cycle: P Lemmas 8.3–8.4, Prop 8.5.
- Three-cycle: P Lemma 8.1 (strips), Lemma 8.6 (local binary rigidity), Lemma 8.7 (one orbit, six sectors), Lemma 8.8 (polynomial region), Lemma 8.9 (certificate), Prop 8.10.
- Re-check: `tools/verify_moser_certificate.py` (brief §6). 1961 → 2026 = 65 years.

**MUST UNDERSTAND**
- Each of the three cases ends in a contradiction; the three-thread case reuses the Moser spindle.

## S5.5 · Assembly
`id: s5_5` · `target: 1:00` · `time: 31:06–32:00 (est.)`

**NARRATION**
> Put it together. If a proper five-colouring of the plane existed, the transfer would turn it into a weak measurable one. That would force palettes of at most two colours, then a special point with a cycle of three, four or five threads, and each case is impossible. [beat] So no five-colouring of the plane exists. Together with Isbell's seven hexagons, the chromatic number of the plane is six or seven. [beat2] And here's a twist. By the compactness theorem, there must now exist a finite unit-distance graph that needs six colours. The proof guarantees it, but doesn't show it. Nobody knows how big it is. [beat] Notice too what the proof didn't use: no SAT solver, no search over graphs. The only explicit calculation is that seven-point check.

**VISUAL**
1. The rail lights up end to end; the train reaches "contradiction". → cue 1
2. Number line: left marker 5 → 6; bracket [6, 7]. → cue 2
3. The glowing finite graph with "?" size reappears, now labelled "must exist (χ = 6 or more)"; it stays out of focus. → cue 3
4. Toolbox panel with greyed icons "SAT solver ✗", "graph search ✗", and lit "7-point check ✓". → cue 4

**ON-SCREEN**
- $6 \le \chi(\mathbb{R}^2) \le 7$
- "a finite unit-distance graph needing 6 colours exists, but is not known"

**SOURCE**
- P Thm 1.1 and its deduction; P Cor 1.5 proof (existential graph); P §8.6 (only explicit computation); brief §6.

**MUST UNDERSTAND**
- The result, the unseen finite witness, and the role of computation.
