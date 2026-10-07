# Outline: "Six Colours at Least" (working title)

Target runtime **≈ 44 min** (range 40–48 once narration is measured). Narration: English.
Concept IDs refer to `research/dependency-graph.md`; insights to `research/insight-map.md`;
claims to `research/brief.md`.

## Visual identity (original)

- **Ground:** deep slate `#16191F` with a faint dot lattice: "the plane" is always present as a texture.
- **Ink:** warm off-white `#ECE6DA` for lines and text; muted grey `#7C8290` for secondary elements.
- **Seven colours, colour-blind-safe (Okabe–Ito), each paired with a glyph** so no information is carried by hue alone:
  orange `#E69F00` ● circle · sky `#56B4E9` ▲ triangle · green `#009E73` ■ square · yellow `#F0E442` ◆ diamond · blue `#0072B2` ⬟ pentagon · vermillion `#D55E00` ⬢ hexagon · purple `#CC79A7` ★ star.
  The first five are the "five colours" of the main proof; all seven appear for the hexagon colouring.
- **Clash marker:** a monochromatic unit edge flashes as a white-hot jagged spark with a ringing outline (not red, which would collide with vermillion).
- **Signature object, the "unit stick":** a rod with two pin-heads and a tiny "1" tick. Every unit edge in the film is drawn as a thin stick in this style, so "this distance is exactly 1" is always readable.
- **Distance indicator:** a callipers glyph with a live numeric readout (3 decimals) that turns ink-white at exactly 1.000.
- **Proof map:** a horizontal "rail" of 7 stations (the paper's Figure 1, redrawn as a transit line). It returns as an overlay at each Act 5 transition, with the current station lit.
- **Type:** Inter (or Source Sans 3) for labels; LaTeX (Latin Modern) for formulas only.
- **Motion rules:** motion only when it carries meaning; ease-in-out 0.6–1.2 s; no idle wobble.
- **Labels for epistemic status:** small corner tags `ANALOGY`, `TOY PROBLEM`, `POSSIBLE RECONSTRUCTION, NOT CONFIRMED BY OPENAI`, `NOT PUBLIC`.

## Reusable components (to build in `components/`)
`UnitGraph` (points, unit sticks, colouring, clash detection) · `ColourTransition` (recolour with glyph morph) · `DistanceIndicator` · `ProofMap` (rail overlay) · `PaletteRing` (centre plus unit ring with per-direction colours) · `NumberLine` (bounds and history) · `StatusTag`.

---

## Chapter table

| # | Chapter | Duration | Belief stage |
|---|---|---|---|
| 0 | Cold open | 1:00 | — |
| 1 | The colouring game | 4:00 | S1 |
| 2 | Geometry becomes a graph | 6:00 | S2 → S3 |
| 3 | Hadwiger–Nelson: 68 years at 4–7, then 5 | 6:00 | S3 |
| 4 | Why 6 is harder | 5:30 | S4 |
| 5 | The new proof (5 sub-chapters) | 13:00 | S5 |
| 6 | What the AI did, and what we don't know | 3:30 | S5 |
| 7 | Checking it | 3:30 | S5 |
| 8 | Why it matters | 2:30 | S5 |
| | **Total** | **45:00** | |

---

### Ch 0. Cold open (1:00)
- **Objective:** Pose the puzzle with zero terminology; promise a story that ends with a 2026 proof.
- **Key question:** "How many colours do you need so that no two points exactly one unit apart match?"
- **Key insight:** none yet; curiosity.
- **Concepts:** C1 (informal).
- **Visual:** A dark plane; a single unit stick drifts in and lands; its two pins glow different colours. Hundreds of sticks rain down; some flash clashes. A number line silently shows "? colours".
- **Transition:** "Let's play."

### Ch 1. The colouring game (4:00)
- **Objective:** Viewer *tries* 2 and 3 colours and feels why they fail, before any answer or jargon.
- **Key question:** "Can you do it with two colours? With three?"
- **Key insight:** I1 (partially), I2 (felt, not named).
- **Concepts:** C1, C2; C6 felt.
- 1.1 *The rule* (0:50): unit stick dropped on a painted plane; only distance exactly 1 matters (0.999 is fine).
- 1.2 *Two colours* (1:10): stripes, checkerboards, rings all fail; then the reason: three points at mutual distance 1. **Pause beat: "Before I show you, try to find two colours that work."**
- 1.3 *Three colours* (1:40): the triangle is satisfied; try a hexagon tiling with 3 colours and find a clash anyway; a viewer-style prompt: "Pause and try to break three colours yourself." End without the answer.
- 1.4 *Too many to try* (0:20): there are infinitely many points, so we need a way to *reason* instead of paint.
- **Transition:** "To reason about it, we need to see the hidden structure: the sticks."

### Ch 2. Geometry becomes a graph (6:00)  ← **pilot scene chosen from here (2.3)**
- **Objective:** Introduce vertex, edge, colouring, chromatic number *after* the viewer needs them; prove ≥ 3 and ≥ 4; animate restriction (finite → plane).
- **Key question:** "Can a small drawing prove something about the whole infinite plane?"
- **Key insight:** I1, I2, I3.
- **Concepts:** C3, C4, C5, C6, C7, C8, C9.
- 2.1 *Dots and sticks* (1:10): paint fades; points and unit sticks remain. Name them: vertex, edge, proper colouring, chromatic number χ (notation appears here because we now need a name for "the fewest colours").
- 2.2 *The triangle* (0:40): 3 mutually adjacent points ⇒ χ ≥ 3.
- 2.3 *The spindle* (2:00): rhombus of two triangles; far tips forced equal (distance √3, no edge). Two rhombi share a tip; rotate one, with a live distance readout, until the far tips are 1 apart. Clash. 7 vertices, 11 edges ⇒ χ ≥ 4. Every possible 3-colouring tried in a fast-forward (3⁷ = 2187), all failing.
- 2.4 *Stamping* (1:30): any colouring of the plane, stamped by the spindle anywhere, gives a coloured spindle, so at least one clash. Several "attempted" 3-colourings of the plane all lose. Conclusion: plane needs ≥ 4.
- 2.5 *Bridge* (0:40): a bigger tricky drawing could force 5, or 6. Is there a ceiling?
- **Transition:** "Is there a ceiling? Yes, and it's beautiful."

### Ch 3. Hadwiger–Nelson: 68 years at 4–7, then 5 (6:00)
- **Objective:** Upper bound by hexagons; the long stall; compactness; computer-assisted 5; what a certificate is.
- **Key question:** "If the answer is 'some finite drawing', why did it take until 2018 to find one forcing 5?"
- **Key insight:** I4, I5.
- **Concepts:** C10, C11, C12, C13, C14.
- 3.1 *Seven hexagons* (1:30): hexagons of diameter < 1 (circumradius 2/5); 7-colour pattern; same colours are > 1 apart. Number line: 4 ≤ χ ≤ 7 (1950, Nelson and Isbell; published Hadwiger 1961; Moser spindle 1961).
- 3.2 *Every infinite answer has a finite witness* (1:10): compactness (de Bruijn–Erdős 1951), visualised as patches locking together. Hence "search for a finite graph" is a complete strategy in principle.
- 3.3 *2018* (2:20): de Grey (biologist, amateur mathematician): 20,425 vertices, custom checker → 1,581. Polymath16; Heule's SAT pipeline: colouring as yes/no constraints; solver output is a *refutation*, a list of 14,000–19,000 derived clauses that a small independent checker verifies; reduced to 553, Parts to 509, then a human-verifiable proof (2020). Number line: 5 ≤ χ ≤ 7.
- 3.4 *Then: silence* (1:00): no one found a graph forcing 6. Why is the next step so much harder?
- **Transition:** "To see why, compare finding a colouring with ruling one out."

### Ch 4. Why 6 is harder (5:30)
- **Objective:** Asymmetry of proof; size explosion; arbitrary colourings may not be picturable; regularity-assuming results.
- **Key question:** "Why not just search harder?" and "Why doesn't a picture-based argument settle it?"
- **Key insight:** I5 (deepened), I6.
- **Concepts:** C15, C16, C17, C18, C19.
- 4.1 *One example vs every possibility* (1:20): 5 colours on a 1,000-vertex graph is 5^1000 possibilities; the graph would also need to be *found*. **We only claim what's sourced:** the bound stayed at 5 from 2018 until this paper; no 6-forcing graph has been exhibited. [P §1; Cor 1.5]
- 4.2 *Colourings you can't draw* (2:20): **TOY PROBLEM:** the circle with an irrational forbidden step. With choice, 2 colours work; no colouring with honest "areas" (measurable) does. Introduce "measurable" informally: a set you can meaningfully assign an area to.
- 4.3 *What was known with nice colourings* (1:20): measurable ≥ 5 (Falconer 1981), map-type ≥ 6 (Townsend), polygonal ≥ 7 (Sokolov–Voronov 2025). Payne's warning: a plane graph with 2 vs ≥ 5. The number line gets a ghost track of "conditional" bounds.
- 4.4 *The gap* (0:30): to reach 6 for *all* colourings, you must either find a giant graph or tame wild colourings.
- **Transition:** "In September 2026, a 62-page preprint from OpenAI claimed to do the second."

### Ch 5. The new proof (13:00)
Proof map rail introduced at start and revisited at each sub-chapter. A one-line caveat appears on screen at the start: "Simplified; the paper's full argument is 62 pages."

**5.0 The map (0:50).** Two halves: *tame* (transfer), then *trap* (geometry). The rail of 7 stations. Concepts: overview only.

**5.1 Taming wild colourings: the transfer (2:40).** I7. C20, C21, C22.
- Intuition: average all shifted and rotated copies of a colouring.
- Small example: averaging a 1-D wild pattern into a smooth "probability of orange" curve.
- Visual construction: stack translucent copies; split into smooth + scrambled (`ANALOGY` tag); correlation dial at distance 1 reads 0 for both whole and smooth part.
- Statement (words then symbols): "A proper k-colouring exists if and only if a *weak measurable* k-colouring exists." Definition shown as: clashes allowed only on a set of total size zero.
- Black box: the rigidity theorem (rotation-symmetric "pure scramble" is perfectly uncorrelated). One sentence on the machinery (ergodic theory, number fields), no detail.
- Converse in 20 s: zoom in on "typical" points, where the exceptions vanish.
- Role: lets the rest of the proof use areas. Holds for every k.
- Bridge: "Now we can reason with honest regions. Suppose five colours worked."

**5.2 The ring around a point: palettes (2:20).** I8. C23, C24, C25, C26.
- Intuition: stand at a point and look at the circle of radius 1 around it.
- Small example: rhombus x + f = x + Rf + R⁻¹f snapping onto the ring at 60°.
- Statement: directions 60° apart share no colour; each direction carries at most 2 colours (Prop 5.6, proof sketched as "three colours there would force infinitely many too-close special centres").
- Two-colour alternation: six petals.
- Bridge: "That's local. To get a contradiction, we need to find a special point."

**5.3 Blur, loop, threads (2:50).** I9. C27, C28, C29, C30.
- Intuition: blur the 5-colouring; most points mix at most two colours, so they live on the edges of a pentagram-pentagon K₅.
- Small example (`TOY PROBLEM`): try to cover a floor with small tiles where at most two meet anywhere: impossible, triple points appear.
- Construction: hence a small loop around some special centre winds around a cycle of colours on K₅ (length 3, 4 or 5). Each edge of that cycle gives a connected thread through the centre.
- The straddle zone (paper Fig 2, redrawn): points < 1 from part of a thread and > 1 from another part are exactly 1 from some point of it, so both of the thread's colours are banned there.
- Bridge: "Three, four or five threads. Each case has to fail."

**5.4 Three cases (3:20).** I10. C31, C32, C33.
- **Five threads (1:00):** pentagon clock; six ±1 steps around the 60° ring; antipodes 3 steps apart must differ by 0 or ±2; arithmetic contradiction. Fully shown.
- **Four threads (0:40):** a parity bit that must stay the same nearby but flips under a 60° turn. Gist only; on screen: "geometric lemmas skipped".
- **Three threads (1:40):** the two outside colours alternate in six 60° sectors; the region where both are excluded (shaded); "only three colours here"; the Moser spindle (rotated by the 3-4-5-like 12-35-37 triangle) slides in; 7 points inside the region; clash. Mention: this placement is a 7-point rational certificate, checkable by hand, and we re-checked it.

**5.5 Assembly (1:00).** C34, C35.
- Rail lights end to end. Number line: 6 ≤ χ ≤ 7.
- Twist: compactness now guarantees a finite unit-distance graph that needs 6, yet the proof doesn't show it. Nobody has seen it. [P Cor 1.5 proof]
- What computation was used: only the 7-point certificate. No SAT, no search.
- **Transition:** "Who, or what, wrote this proof?"

### Ch 6. What the AI did, and what we don't know (3:30)
- **Objective:** Report FACT / INFERENCE / UNKNOWN faithfully; no narrated inner monologue; answer "reasoning or brute force?" in terms of the proof's content.
- **Key question:** "What do we actually know about how this was found?"
- **Key insight:** I11 (first half: origin).
- **Concepts:** C37.
- 6.1 *What OpenAI states* (1:00): internal OpenAI model (unreleased); ~4,000 problems posed; *average* ≈ 3 h ChatGPT Pro thinking compute per result; 722 manuscripts, 372 families; listed author "OpenAI". Each on screen with `FACT` and a source line.
- 6.2 *What's not public* (0:50): no reasoning summary for this result; prompt, attempts, tools, human steering, compute for this result: `NOT PUBLIC`. Inferences shown with the mandated label.
- 6.3 *What a summary looks like, from a different result* (0:50): the π irrationality-exponent summary (family 017): a few lines shown with a clear "different result" banner; it records abandoned attempts.
- 6.4 *Reasoning or brute force?* (0:50): this proof contains no large search: one 7-point certificate. Its content is conceptual (ergodic theory, topology, geometry), and it adapts known tools (Furstenberg–Zimmer, Falconer/Payne density points, Sokolov–Voronov interfaces, Townsend annuli), as the paper's own citations show. What that says about the *process* is unknown: the scale (4,000 problems, filtered for significance) is itself a kind of search.
- **Transition:** "Whoever wrote it, is it right? That's a separate question."

### Ch 7. Checking it (3:30)
- **Objective:** Explain proof assistants with a toy; state precisely what is formalised and what isn't.
- **Key question:** "Why isn't 'an AI produced it' enough, and what would be?"
- **Key insight:** I11 (second half: logic, community).
- **Concepts:** C36.
- 7.1 *A tiny Lean proof* (1:10): the triangle needs 3 colours, as a short Lean statement; the checker accepts; we alter one step and it rejects. Small trusted kernel vs large untrusted proof search.
- 7.2 *This result in Lean* (1:30): the 6-line statement on screen (all functions from ℂ to 5 colours, distance exactly 1, no measurability). Three standard axioms. ~30,000 lines of formal proof, same two-part architecture. Separately, the 7-colouring.
- 7.3 *Five words, five meanings* (0:50): AI-generated ✓ (per OpenAI) · computer-checked certificate ✓ (we re-checked the 7 points) · formally verified: OpenAI publishes a formalization; our scan found no gaps; **we did not rebuild it** (wording to be upgraded if we do) · independently reproduced: no public evidence · peer reviewed: no.
- **Transition:** "So what changed?"

### Ch 8. Why it matters (2:30)
- **Objective:** Calibrated close: before/after, what's open, what this release shows and doesn't.
- **Key question:** "What is now known, what is still open, and what did we learn about AI and mathematics?"
- **Concepts:** recap; C34, C35.
- Number line animation: 1950 [4,7] → 2018 [5,7] → 2026 [6,7] (with formal-verification marker).
- Open: 6 or 7? The unseen finite graph. The transfer works for any number of colours.
- What it shows (each tied to evidence): a model produced a long, citation-aware, conceptual proof whose statement is formalised; the method went around the finite-graph route rather than through it.
- What it doesn't show: how often the model is wrong (only selected results were released; the repo says unformalised results may have issues); how much human steering there was; how it compares to human research time. `NOT PUBLIC`.
- Final image: the Moser spindle, 1961, sitting inside the 2026 proof, then the open question mark between 6 and 7.

---

## Pilot (Phase 6) choice
**Scene 2.3, "The spindle" (~2:00).** It uses every core component (UnitGraph, DistanceIndicator, ColourTransition, clash marker), sets the visual identity, and contains the narration's key-insight beat ("a beat before the twist").

## Open production questions for Checkpoint A
1. **Voice:** no voice_id given. Proposal: I generate three ~2-sentence samples (≈ 300 characters total) with `eleven_v4` from three library voices that fit "calm, curious, documentary", and you pick one.
2. **Lean rebuild:** should I attempt a local build plus comparator run of the formal proof (several GB download, possibly hours)? It would let Act 7 say "we re-ran the check" instead of "OpenAI reports".
3. **Title:** working title "Six Colours at Least". Alternatives: "The Plane Needs Six", "Beyond Five".
