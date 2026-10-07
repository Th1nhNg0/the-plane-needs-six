# Insight map: the "aha" moments

Each insight is derived from the paper or a cited source (tag in brackets), and lists what the viewer
believes before, the idea that changes it, the best visual, and what it unlocks.
The video's five belief stages (from the brief) are marked S1–S5.

---

### I1. A rule about pairs turns the plane into a network (S1 → S2)
- **Before:** "Colour the plane" sounds like painting regions, like a map.
- **The shift:** The only rule is about *pairs of points exactly 1 apart*. Nothing else matters: not regions, not borders. So the real object is a network whose nodes are all points and whose links are all unit-distance pairs. [P §1 para 1]
- **Visual:** The "unit stick", a rigid rod with two pins. We drop it at random on a painted plane, and a pulse fires whenever both pins land on the same colour. Then the paint fades and only the stick-positions remain, as a dense web of links.
- **Unlocks:** Vertex, edge, colouring and chromatic number as natural words; the idea that small drawings (finite graphs) can be stamped anywhere.

### I2. Rigid shapes force colours, and a twist breaks them (S2)
- **Before:** "Three colours are probably enough; the plane is huge and there's lots of room."
- **The shift:** An equilateral triangle forces 3 colours. Two triangles glued into a rhombus force the far tips to share a colour (they are √3 apart, with no edge between them). Make two such rhombi share a tip and rotate one until the other tips are exactly 1 apart: now two points that must be equal must also differ. That is the Moser spindle: 7 points, 11 sticks, at least 4 colours. [MoserMoser1961; P §8 eq. Moser vectors; our brute-force check]
- **Visual:** A hinged double rhombus. Rotate one rhombus about the shared tip while a live distance readout between the far tips counts down to exactly 1.000. A single red "clash" spark appears.
- **Unlocks:** "A small finite drawing can prove a lower bound for the whole plane" (S3). It also plants the spindle, which returns as the final blow in Act 5.

### I3. Restriction: any colouring of the plane colours every drawing in it (S3)
- **Before:** "The spindle is one little picture. Why does it say anything about the infinite plane?"
- **The shift:** Take *any* colouring of the plane, however wild, and place the spindle anywhere. Its 7 points inherit colours, and because the sticks are true unit distances, that is a proper colouring of the spindle. So if the spindle needs 4 colours, the plane does too. [P §1; standard]
- **Visual:** A stamp. The spindle slides across a 3-coloured plane (randomly painted, hexagonally painted, striped); wherever it lands, at least one stick lights up red.
- **Unlocks:** The finite-graph strategy, and the question of whether it can go all the way.

### I4. Compactness: the plane's answer is always witnessed by some finite drawing (S3)
- **Before:** "Maybe the plane needs more colours for some infinite reason no finite drawing can capture."
- **The shift:** (de Bruijn–Erdős) If every finite piece can be k-coloured, so can the whole plane (in ZFC). So if the plane needs 6, *some finite* unit-distance graph needs 6. [P §1 para 3; deBruijnErdos1951]
- **Visual:** A zoom-out of nested finite patches, each with a valid colouring, that "lock together" in the limit.
- **Unlocks:** Why everyone searched for big finite graphs (de Grey 2018) and why SAT solvers fit. It also sets up the twist: the 2026 proof guarantees a 6-forcing finite graph exists without showing one. [P Cor 1.5 proof]

### I5. Finding a colouring is easy to check; ruling out all of them needs a certificate (S3 → S4)
- **Before:** "A computer just tries everything."
- **The shift:** Showing a colouring *exists* takes one example. Showing *none* exists means covering 4^1581 possibilities. Solvers don't list them: they produce a *refutation*, a chain of short deductions (Heule: 14,000–19,000 clause steps) that a separate small checker can verify, even a formally verified checker. [Heule2018 §3; deGrey2018]
- **Visual:** A branching tree of partial colourings, pruned by "clashes", collapsing into a thin certificate scroll handed to a separate little checker machine.
- **Unlocks:** The vocabulary of trust (generated vs checked) used again in Act 7; and why going to 6 by search stalls (the bound sat at 5 from 2018 to 2026).

### I6. Arbitrary colourings can be wilder than any picture (S4)
- **Before:** "Every colouring looks like some regions with borders, maybe very wiggly."
- **The shift:** Toy T2, the circle with a forbidden irrational step α. With the axiom of choice there is a 2-colouring: alternate along each orbit. But no colouring you could ever draw (no measurable one) works: alternating means repeating every 2α, and a pattern that repeats under an irrational rotation is constant. So "can be coloured" and "can be coloured with sets that have an area" are different questions. The paper's own plane-level warning is Payne's graph: 2 colours for arbitrary colourings, at least 5 for measurable ones. [toy T2 (mine); mechanism = P Lemma 6.4; Payne2009 via P §1]
- **Visual:** The circle with arcs hopping by α, dots filling in densely. The alternating colouring becomes an unrenderable "static" (we show that it can't be drawn, rather than fake a picture of it).
- **Unlocks:** Why earlier 6- and 7-colour results needed regularity assumptions (measurable ≥ 5 in 1981; map-type ≥ 6; polygonal ≥ 7), and why those don't settle the real question.

### I7. The transfer: wildness can be averaged away without losing the rule (S4 → S5)
- **Before:** "If arbitrary colourings are that wild, no geometric argument can touch them."
- **The shift:** Thm 1.3: a proper k-colouring exists *if and only if* a "weak measurable" one does, meaning one with honest areas whose clashes have total size zero. Averaging all translated and rotated copies gives a random but symmetric colouring; its "perfectly scrambled" part has zero self-correlation at every shift (rigidity, Thm 2.3), so discarding it keeps the unit-distance rule. Conversely, zooming in on "typical" points removes the zero-size exceptions, and compactness rebuilds an honest colouring. [P Thm 1.3, Prop 4.2, Thm 2.3, Lemma 4.3]
- **Visual:** Many translucent rotated copies of a "static" colouring stacked and averaged into a soft field; a signal-plus-noise split (labelled ANALOGY); a correlation dial at distance 1 stuck at 0 before and after.
- **Unlocks:** Permission to use geometry and area: the second half can reason with pictures that mean something. It holds for every k, which matters for 6 vs 7.

### I8. Stand at a point and look at the unit ring: 60° apart, the colours must differ (S5)
- **Before:** "Even with areas, a 5-colouring could be messy everywhere."
- **The shift:** Around any centre x, read the colours on the ring of radius 1 (the "palette" in each direction). The rhombus from I2 returns: x + f = x + Rf + R⁻¹f, so directions 60° apart cannot share a colour. Hence at most 2 colours per direction (Prop 5.6), and if only two are around, they flip every 60°. [P Cor 5.4, Prop 5.6, §5.3]
- **Visual:** The "compass ring" HUD around a point, with the rhombus snapping onto the ring at 60°, and a 6-petal alternation pattern.
- **Unlocks:** The local "alphabet": every direction carries one or two colours, and 60° steps are constrained.

### I9. Blur, and topology forces a cycle (S5)
- **Before:** "Even so, where would a contradiction come from?"
- **The shift:** Blur the colouring slightly: each point becomes a mix of colours, and (away from a few special points) at most two are mixed, so each point sits on an *edge* of a pentagon-with-diagonals (K₅). A flat region cannot be covered by small patches with only two ever overlapping (tiles have triple points), so somewhere a little loop around a special centre must wind around a cycle of colours of length 3, 4 or 5. Each edge of that cycle leaves a connected "border thread" through the centre, and any point at distance < 1 from part of a thread and > 1 from another part is exactly 1 from some point on it, so both border colours are banned there. [P Lemma 7.5, 7.6, 7.7, 7.8, Prop 7.1; Fig 2]
- **Visual:** A plane coloured in five colours, blurred; points mapped live onto a K₅ diagram; a small loop drawn around a centre traces a triangle/square/pentagon on K₅; threads emerge from the centre; the "straddle zone" shown as a sweeping unit compass.
- **Unlocks:** A single centre with 3, 4 or 5 threads and banned zones. Three cases to kill.

### I10. Three cases, three different weapons (S5)
- **Before:** "That's just a reduction; something hard must remain."
- **The shift:**
  - 5 threads: a clock-arithmetic puzzle (±1 steps mod 5 around a 6-step ring cannot satisfy the antipodal rule). [P Prop 8.2]
  - 4 threads: a parity bit that must be constant yet flip under a 60° turn. [P Prop 8.5]
  - 3 threads: six alternating 60° sectors force a region near the centre that can use only 3 colours, and the 1961 Moser spindle fits inside it (a 7-point rational certificate). It needs 4. [P Props 8.10, Lemma 8.8, 8.9; our exact check]
- **Visual:** For 5, a pentagon "clock" with a token taking six ±1 steps. For 4, a two-colour parity lamp. For 3, a hexagonal flower of sectors, a shaded three-colour region, and the spindle sliding in and lighting a red clash.
- **Unlocks:** χ ≥ 6. The bookend: the same small drawing from Act 2 finishes a 62-page proof.

### I11. "An AI produced it" is a claim about origin; "Lean checked it" is a claim about logic (S5)
- **Before:** "Either the AI is right or it isn't; trust it or don't."
- **The shift:** Separate the questions. *Who or what found it* (internal OpenAI model, process facts plus many unknowns). *Is it correct* (a ~6-line formal statement anyone can read; a ~30,000-line formal proof a small trusted kernel checks; three standard axioms). *Has anyone else reproduced or reviewed it* (not yet publicly). [README; lean/*; brief §§7–8]
- **Visual:** Three separate "trust dials" (Origin / Logic / Community) instead of a single verdict. Lean toy: a 3-line proof that the triangle needs 3 colours, with the kernel accepting and then rejecting a deliberately broken step.
- **Unlocks:** A calibrated ending: what changed on the number line, what is still open (6 vs 7; the unseen finite graph), and what this release does and does not show.
