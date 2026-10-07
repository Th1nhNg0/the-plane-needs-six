# Research brief: "The Euclidean plane is not five-colorable"

Status: Phase 1 deliverable, prepared 2026-10-07. Every claim below carries a source tag.
Paper references use the compiled PDF numbering (62 pages), for example [P §5.4, Prop 5.6].
Downloaded source copies are kept locally in `research/src/` and `research/background/`
and are excluded from the public repository. See the sources in §12.

---

## 0. Corrections to the task prompt's first-skim assumptions

| Prompt assumption | What the sources say | Source |
|---|---|---|
| Section order: introduction, transfer, palettes, interfaces, transitions, angular, spectral, rigidity | Actual order: Introduction, **Spectral (§2), Rigidity (§3)**, Transfer (§4), Palettes (§5), **Transitions (§6), Interfaces (§7)**, Angular (§8). Spectral + rigidity (≈ a third of the paper) are the engine of the transfer theorem, so the transfer is the deepest part, not a preliminary. | `build/main.tex` |
| "The route to the previous bound (de Grey 2018) used a large finite graph checked by a SAT solver" | Partly true. De Grey's own verification used a **custom program**: he started from a 20,425-vertex graph and shrank it to 1,581 vertices. Others then confirmed the 1,581-vertex graph with standard SAT solvers. Heule (2018) used SAT proof minimisation to reach 553 vertices; Parts reached 509 and also gave a **human-verifiable** proof. Exoo and Ismailescu gave an independent proof. So "≥ 5" does not depend on trusting one SAT run. | [deGrey2018 §§4–5], [Heule2018 abstract, §3], [P §1] |
| "Earlier results reaching 6 or 7 assumed well-behaved regions" | Correct, with specifics: Woodall 1973 (closed covers/regions); Townsend, map-type colourings ≥ 6 (announced 1981, details 2005); Sokolov–Voronov 2025, polygonal/locally finite map colourings ≥ 7. Also important: for **Lebesgue-measurable** colour classes, Falconer proved ≥ 5 back in **1981**, 37 years before de Grey's unrestricted 5. | [P §1, paras 4–5] |
| "The proof does not use a large finite graph checked by a SAT solver" | Confirmed. The only explicit numerical step is a **seven-point rational certificate** (Lemma 8.9): exact rational inequalities showing that seven placed points lie in an open region. It is short enough to check by hand. No SAT solver, no search, no large graph. | [P §8.6] |
| Final contradiction: "3 → Moser graph, 4 → parity, 5 → six-step words" | Confirmed, in exactly that form (proof-flow figure; Props 8.2, 8.5, 8.10). | [P Fig 1, §8] |
| Lean formalization exists | Confirmed, and it covers the **unrestricted** statement (arbitrary `ℂ → Fin 5`, no measurability), using only Lean's three standard axioms. The 7-colouring is also formalised. Details and caveats are in §8 below. | `lean/docs/158.md`, comparator JSON |

New facts the prompt did not anticipate, all useful for the script:
1. **A finite non-5-colourable unit-distance graph must exist, but nobody has seen one.** By de Bruijn–Erdős compactness, Theorem 1.1 implies such a finite graph exists; the paper calls it "existential" and does not exhibit it. [P Cor 1.5 proof; P §1 para 3]
2. **The transfer theorem holds for every number of colours k**, not just 5. The 6-versus-7 question is therefore equivalent to a question about weak measurable colourings. [P Thm 1.3; §1 after Thm 1.1]
3. **The Moser spindle (1961) delivers the final blow.** The last case of the 2026 proof ends by placing the same 7-vertex graph inside a region that can use only three colours. [P Prop 8.10, Fig 3]
4. **The paper criticises a competing claim.** A May 2026 manuscript (Reed) claimed χ = 7. This paper's footnote gives an explicit counterexample to one of its key bounds (a half-open arc of angle π/3). [P §1 footnote]
5. **A direct logical consequence (my observation, not stated separately in the paper):** a proper colouring with measurable classes is in particular a weak measurable colouring, so Theorem 1.4 also raises the *measurable* chromatic number bound from Falconer's 5 to 6. Mark as "follows directly from Thm 1.4" if used on screen.

---

## 1. Problem definition

- **Rule.** Colour every point of the plane so that any two points exactly 1 apart get different colours. The fewest colours that work is the *chromatic number of the plane*, χ(ℝ²). No regularity is required of the colour classes. [P §1 para 1]
- **Equivalent graph form.** Vertices = all points of the plane; edges = pairs at distance exactly 1. χ(ℝ²) is the chromatic number of this (uncountable) graph. Drawn edges may cross. [P §1 para 1]
- **Name.** Hadwiger–Nelson problem. [P §1]
- **Set theory.** The paper works in ZFC [P §1 before Thm 1.1]. This matters because Shelah–Soifer (2003) showed that chromatic numbers of some geometric graphs depend on whether the axiom of choice is assumed. In ZF + dependent choice + "every set is measurable", Falconer's theorem gives χ ≥ 5 regardless of finite graphs. [Shelah–Soifer 2003, JCTA 103(2):387–391]. Use only as a one-line aside in Act 4, if at all.

## 2. History and prior results (dated)

| Year | Result | Source |
|---|---|---|
| 1950 | Nelson poses the problem and observes χ ≥ 4; Isbell observes χ ≤ 7 via hexagons (both unpublished; record in Soifer) | [P §1; Soifer2003 pp. 15–19] |
| 1961 | Hadwiger publishes the formulation with bounds 4 and 7; L. & W. Moser give the 7-vertex, 11-edge "Moser spindle" (not 3-colourable) | [P §1; Hadwiger1961; MoserMoser1961] |
| 1951 | de Bruijn–Erdős compactness: an infinite graph is k-colourable iff every finite subgraph is (uses choice) | [deBruijnErdos1951 Thm 1] |
| 1973 | Woodall: distance-avoiding closed covers and region decompositions | [P §1] |
| 1981 | Falconer: measurable colour classes need ≥ 5 colours (density points + rotations) | [Falconer1981; P §1] |
| 1981/2005 | Townsend: map-type colourings need ≥ 6 (repairs Woodall; announcement 1981, details 2005) | [Townsend1981, 2005; P §1] |
| 2003 | Shelah–Soifer: axiom-dependence phenomena for related graphs | [Shelah–Soifer 2003] |
| 2009 | Payne: the graph on ℝ² with **rational** unit displacement vectors is 2-colourable, yet every measurable colouring of it needs ≥ 5. Lesson: measurable and arbitrary colourings can behave completely differently. | [Payne2009; P §1 para 4] |
| Apr 2018 | de Grey: finite unit-distance graphs that are not 4-colourable. First 20,425 vertices, checked by custom code; smallest found 1,581 vertices. **χ ≥ 5.** Polymath16 starts. | [deGrey2018 abstract, §4, §5.1] |
| May 2018 | Heule: SAT (Glucose) + DRAT clausal proofs; refutations of 14,000–19,000 steps, checked with DRAT-trim; "can be checked in roughly a second even with formally verified checkers". 553-vertex examples. | [Heule2018 §3] |
| 2020 | Exoo–Ismailescu: independent proof of ≥ 5. Parts: 509-vertex graph; human-verifiable proof of ≥ 5. | [P §1] |
| 2025 | Sokolov–Voronov: polygonal colourings in a locally finite map framework need ≥ 7 (interface argument) | [SokolovVoronov2025; P §1] |
| Sep 2026 | **This paper: χ ≥ 6 for arbitrary colourings, so χ ∈ {6, 7}.** | [P Thm 1.1] |

**Upper bound 7 (Isbell's hexagons, as the paper proves it):** hexagons of circumradius r = 2/5 on a triangular lattice, coloured by the 7 cosets of the sublattice generated by 2 − ω (|2 − ω|² = 7). Inside one hexagon, distances ≤ 2r = 0.8 < 1. Same-colour hexagons are separated by at least (√21 − 2)r ≈ 1.033 > 1. Boundaries can be assigned to any incident hexagon. [P §1, proof of Thm 1.1]

## 3. The new result

- **Theorem 1.1.** No proper 5-colouring of the plane exists, even with arbitrary colour classes. Hence 6 ≤ χ(ℝ²) ≤ 7. [P Thm 1.1]
- **6 versus 7 remains open.** [P §1 after Thm 1.1]
- **Corollary 1.5 (positive badness).** There is a δ > 0 such that every 5-colouring has at least a δ-fraction of monochromatic unit pairs, in several averaged senses (invariant means; periodic measurable colourings; convergent box frequencies). The constant comes from the existential finite graph H, with δ = 1/|E(H)|. [P Cor 1.5]

## 4. Proof architecture (the recurring "map")

Reproduces the paper's Figure 1, `figures/proof-flow.tex`. We redraw it in our own style.

```
Arbitrary proper 5-colouring
  → invariant probability on proper labellings        (§4, Prop 4.2: averaging)
  → continuous translation factor                     (§4, Lemma 4.1 + §§2–3, Thm 2.3 rigidity)
  → weak measurable 5-colouring                       (§4, Prop 4.2: a measurable sample)
  → angular palettes of size ≤ 2                      (§5, Prop 5.6)
  → common exclusion continua on a cycle of length 3, 4 or 5   (§6 Thm 6.5, §7 Prop 7.1)
  → case 3: Moser graph | case 4: parity | case 5: six-step words   (§8)
  → contradiction
```

Two halves [P §1, end of intro paragraph]:
- **Part A (Transfer, Thm 1.3, valid for every k):** a proper k-colouring exists ⇔ a weak measurable k-colouring exists.
- **Part B (Thm 1.4):** no weak measurable 5-colouring exists.

### 4A. Transfer (Thm 1.3) [P §§2–4]

**Definition 1.2 (weak measurable k-colouring).** A measurable colouring c in which the set of monochromatic unit pairs (x, x+u) has measure zero (Lebesgue in x × arc length in direction u). Exceptional pairs are allowed, as long as they are negligible. Changing c on a null set doesn't matter. [P Def 1.2]

Forward direction, proper ⇒ weak measurable (Prop 4.2):
1. Restrict the colouring to the countable "algebraic plane" E = points with real-algebraic coordinates. [P §1.1, §4]
2. Average its translates and rotations by algebraic rotations K over larger and larger finite sets (Følner averaging; the group E ⋊ K is amenable). This gives a **random colouring of E whose law is invariant** under translations and rotations, and which is proper with probability 1. [P Prop 4.2 "An invariant law…"]
3. Split each colour indicator f_i into a **continuous part** p_i (the part whose translates vary continuously in L²) and a **remainder** b_i. Projection onto the continuous part is a conditional expectation, so p_i ≥ 0 and Σ p_i = 1. [P Lemma 4.1]
4. **Rigidity (Thm 2.3):** any rotation-invariant probability law on characters that gives zero mass to the ordinary continuous characters must be Haar measure. Consequence: the remainder b_i has **zero correlation at every nonzero algebraic shift**. Removing it therefore keeps the zero unit-distance correlations: ∫ p_i · T_u p_i = 0. [P Thm 2.3, Prop 4.2]
   - The rigidity proof [P §§2–3] uses Furstenberg–Zimmer compact-extension towers, a relative singularity lemma (2.7), multiple ergodic averages (3.2), two algebraic identities giving a "difference inequality" w(|A−B|) ≤ w(A)+w(B) (3.3), and a number-field general-position argument (3.4–3.5). **Too technical for the video**: present it as a black box with an honest analogy (see toy T3).
5. The continuous part extends to all of ℝ², gives jointly measurable fields, and one sample of it yields a measurable colouring ("least label with positive weight") with only null-measure monochromatic unit pairs. [P Prop 4.2 "A measurable sample"]

Reverse direction, weak measurable ⇒ proper:
- **Density points (Lemma 4.3):** points where a colour class has density 1 ("typical points") contain no monochromatic unit pair, even though the weak definition allowed null exceptions.
- Any finite configuration can be translated so that all its points are typical, so every finite unit-distance graph is k-colourable. **Compactness** (de Bruijn–Erdős) then gives a proper colouring of the whole plane. [P proof of Thm 1.3]

### 4B. No weak measurable 5-colouring (Thm 1.4) [P §§5–8]

**Idea B1: Palettes (§5).** At a centre x and direction e, the *palette* P_x(e) is the set of colours that "appear" at the point x + e on the unit circle around x, in a limiting/essential sense (weak-* limits of circle samples at nearby centres and radii → 1). [P Def 5.1]
- **Palette transfer (Lemma 5.2):** for almost every pair of directions (e, v), the colour at x + e + v avoids both P_x(e) and P_x(v). Reason: x + e and x + e + v are exactly 1 apart.
- **Sixty-degree exclusion (Cor 5.4):** P_x(f) ∩ P_x(Rf) = ∅, where R is rotation by 60°. Reason: x + f = x + Rf + R⁻¹f, the equilateral rhombus. *Visual: unit rhombus.*
- **Binary alternation:** if only two colours are available around a centre, they alternate under every 60° step. [P §5.3]
- **Binary-centre separation (Lemma 5.5):** two distinct centres that are "binary" for the same colour pair are at least a fixed δ* apart. The proof is a circle-dynamics argument (Sullivan-type bounded distortion).
- **Proposition 5.6:** almost every palette has **1 or 2 colours**. If 3 colours sat in the palette at direction e, the circle around x + e would see only the other 2 colours, making x + e binary for that pair. That happens for a positive measure of directions e, giving infinitely many binary centres on a compact circle, which contradicts Lemma 5.5.

**Idea B2: Transitions and cyclic centres (§6).**
- **Transition graph Γ_x:** a graph on the 5 colours, with edge ij when colours i and j sit next to each other near x in a quantitatively thick way (area of i↔j transitions under a shift h is ≳ |h|). [P Def 6.1]
- An edge ij gives a circle sample avoiding both i and j (Lemma 6.2; uses the Fourier decay |σ̂(ξ)| ≲ |ξ|^(−1/2) of circle measure).
- **Singleton–pair alternation is impossible (Lemma 6.4):** uses the angle γ with cos γ = 5/6, which is an **irrational** multiple of π (else 2cos γ = 5/3 would be an algebraic integer), and a unit equilateral triangle. This uses the same "irrational rotation forces constancy" mechanism as toy T2 below.
- **Theorem 6.5:** the centres where Γ_x contains a cycle form a **closed, locally finite** set: finitely many in any bounded region. Each cycle length (3, 4, 5) is handled separately.

**Idea B3: Interfaces (§7).** Proposition 7.1 builds a common centre x, a simple cycle of colours of length ℓ ∈ {3, 4, 5}, and, for each edge of that cycle, a compact connected set K_j through x such that **both** endpoint colours are absent from the "straddle zone" Δ(K_j) = {z : min dist to K_j < 1 < max dist to K_j}. Connectedness means every z in Δ(K_j) is exactly distance 1 from some point of K_j. [P eq 7.1, Fig 2]

How it is built:
1. **Blur:** p_i^ε = average of colour i over a disk of radius ε. Continuous, sums to 1. Unit-distance inequality p_i(q) + p_i(z) ≤ 1 whenever |q − z| = 1. [Lemma 7.2]
2. **Threshold and renormalise** (α < 1/5) → a continuous map into the probability simplex on 5 colours. Away from small holes (total radii → 0) and away from cyclic centres, at most two coordinates are positive, so the map lands in the **complete graph K₅** drawn as the simplex's 1-skeleton. Holes away from cyclic centres can be filled because the local transition graph there is a forest (trees are contractible). [Eq 7.3, Lemmas 7.3–7.4]
3. **Planar cover obstruction (Lemma 7.5):** a closed square of side 10 has no open cover in which every point lies in at most 2 sets and every set has diameter at most 2 (Brouwer fixed-point argument). Same-colour connected regions of the blurred map have diameter ≈ ≤ 1 (otherwise the unit-distance inequality is violated), so if every loop around a cyclic centre were trivial we would get such a cover. **Hence some small loop around a cyclic centre is non-trivial in K₅** (Lemma 7.6). *Toy: you cannot tile a floor with small tiles so that only two meet at every point; triple points are forced (dimension 2).*
4. A non-trivial loop in a graph contains a **simple cycle** (length 3, 4 or 5 in K₅); each edge midpoint's preimage contains a connected piece crossing the annulus (Lemmas 7.7–7.8). Limits give the continua K_j.

**Idea B4: The three cases (§8).** Near x, just inside and just outside the unit circle, the sign of e · v_j for each continuum's limiting direction v_j decides which colours are allowed (Lemma 8.1: allowed sets O(e) outside, I(e) inside).
- **5-cycle (Prop 8.2): "six-step words".** Palettes must be "diagonals" D_i = {i, i+2} (indices mod 5), and antipodal directions have the same options. Around a 60° orbit of 6 directions, consecutive indices differ by ±1 (disjoint diagonals), and antipodal ones (3 steps apart) differ by 0 or ±2 mod 5. Three ±1 steps sum to ±1 or ±3, so all three must have the same sign; overlapping triples make all six steps equal, and ±6 ≢ 0 (mod 5). Contradiction. **This is fully explainable with high-school arithmetic.**
- **4-cycle (Prop 8.5): "parity obstruction".** States X (outsider), U = {0,2}, V = {1,3} alternate under 60° steps. Every 6-position word contains X, and all X positions share one parity h(t). The four limiting rays form two antipodal pairs, and the diagonal state is U on one projective arc and V on the other, one of length ≤ π/2 (Lemma 8.4). Nearby words must share parity, so h is constant, but a 60° shift flips parity. Contradiction. **Show only the gist: a parity bit that must be both constant and flip.**
- **3-cycle (Prop 8.10): Moser.** The two outsider colours X, Y appear as a binary state that alternates under 60° and is locally constant (Lemma 8.6; uses a 4-edge unit path). So the circle around x splits into **six 60° sectors alternating X, Y** (Lemma 8.7). For z with sin(3(φ−δ))·sin(3(φ+δ)) < 0, i.e. the polynomial region P < P′ of Lemma 8.8, the two unit directions summing to z land in sectors with opposite outsiders, so **both** outsiders are excluded near x + z: that region uses only the 3 triangle colours. The rotated and translated Moser spindle z_g = (35+12i)/37 · (g + (−290+149i)/250) puts all 7 vertices inside that region (Lemma 8.9), giving a proper 3-colouring of the Moser spindle. Impossible. [P Fig 3]

## 5. Key objects (glossary for the script)

| Object | Plain-language meaning | First use in video |
|---|---|---|
| Unit-distance graph | dots joined when exactly 1 apart | Act 2 |
| Proper colouring / chromatic number | no edge with equal colours / fewest colours | Act 2 |
| Moser spindle | 7 points, 11 unit sticks, needs 4 colours | Act 2 |
| Compactness (de Bruijn–Erdős) | "if every finite piece can be coloured, the whole can" | Act 3 |
| Certificate (DRAT refutation) | a checkable record that no colouring exists | Act 3 |
| Measurable set | a set you can meaningfully assign an area | Act 4 |
| Weak measurable colouring | measurable colouring where clashes have total "size" zero | Act 5.1 |
| Typical / density point | a point whose immediate neighbourhood is (in the limit) all its own colour | Act 5.1 |
| Palette P_x(e) | colours visible at x + e on the unit ring around x | Act 5.2 |
| Transition graph, cyclic centre | which colours border each other near x; a centre where they border in a cycle | Act 5.3 |
| Straddle zone Δ(K) | points that are < 1 from part of K and > 1 from another part, hence exactly 1 from some point | Act 5.3 |

## 6. Role of computation

- **In this proof:** one finite rational certificate (Lemma 8.9). It says that 7 explicit points lie strictly inside an explicit polynomial region, using only rational arithmetic on boxes around √3 and √11. The paper writes it out in full, a reader can check it by hand, and it is also formalised (`lean/OAI/Geometry/PlaneColoring/Moser.lean`, `ThreeLabelRegion`). [P §8.6]
- **Independent re-check (ours):** `tools/verify_moser_certificate.py` checks the 11 unit edges and rotation with symbolic arithmetic, evaluates the seven placement inequalities at 60-digit precision, and brute-forces all 3⁷ colourings to check that the spindle is not 3-colourable but is 4-colourable. The numerical placement checks do not implement the paper's exact rational-box certificate. **Result: all checks pass.** (Run 2026-10-07.)
- **No SAT solving, no graph search, no numerical optimisation** appears in the paper's argument. [P, whole text]
- **Contrast with the 2018 route:** finite graphs plus computer checking (custom code, later SAT with DRAT certificates). [deGrey2018; Heule2018]

## 7. How the AI was involved: FACT / INFERENCE / UNKNOWN

Primary process source: upstream repo `README.md` ("How the results were produced"). The announcement page returned HTTP 403 during script research, so **no claim in the script relies on it**. It was accessible during release preparation on 2026-10-07 and dates the release to 6 Oct 2026. [OpenAI announcement; upstream README]

| # | Claim | Tag | Source |
|---|---|---|---|
| F1 | The repository's manuscripts were "produced by an internal OpenAI model". | FACT | README §1 |
| F2 | The paper's listed author is "OpenAI"; date September 23, 2026. | FACT | preprint README, main.tex |
| F3 | "The vast majority of results were obtained with the same procedure using an unreleased internal OpenAI model. On average, each result used three hours of ChatGPT Pro thinking compute with that model." | FACT (average over results, not specific to this one) | README "How the results were produced" |
| F4 | "Over the course of the evaluation, the model was posed approximately 4,000 problems." Output was aggregated into 722 manuscripts / 372 families after "requiring an appropriate level of significance". | FACT | README |
| F5 | Named exceptions to the fixed procedure: a zeta zero-free region and Hodge for CM abelian varieties; the 11/12 zeta write-up was human-edited. **This result is not named as an exception.** | FACT | README |
| F6 | "Some outputs build upon earlier results produced by the models." | FACT (repo-wide) | README |
| F7 | Reasoning summaries were released for 10 families (007, 017, 087, 102, 159, 197, 221, 271, 287, 362). **Family 158 (this result) has none.** | FACT | README table |
| F8 | This result has a Lean formalization; comparator config `EuclideanFiveColor.json`. | FACT | lean/docs/158.md; formalization.yaml |
| F9 | Formalization catalogue fields (catalogue-wide): `automation: methods: [agent]`; `review: status: unchecked`; `status: scope: "Partial progress."` | FACT (as written; the fields are catalogue-level, not per entry) | lean/formalization.yaml |
| F10 | "Some of the unformalized results could have issues." (This one is formalized.) | FACT | README |
| I1 | This result was produced by the standard fixed procedure (not an exception). | INFERENCE (it is not in the README's exception list) | README |
| I2 | The paper's text was not human-edited for readability. | INFERENCE (only the zeta write-up is named as human-edited) | README |
| I3 | The Lean formalization of this result was produced by an AI agent. | INFERENCE (the catalogue-level field says "agent"; not stated per entry) | formalization.yaml |
| I4 | The problem was posed in a "prove or disprove" form. | INFERENCE (the published prompt excerpt for family 159 uses that form) | reasoning_traces/quasipolynomial…pdf p. 1 |
| U1 | The exact prompt for this problem, and whether earlier model outputs or literature were supplied. | UNKNOWN | — |
| U2 | Compute actually spent on *this* result; number of attempts or samples; wall-clock time. | UNKNOWN | — |
| U3 | Tools available to the model (code execution, search, Lean during generation). | UNKNOWN | — |
| U4 | Which ideas, if any, came from human steering or selection; who chose this problem. | UNKNOWN | — |
| U5 | Who wrote the Lean *statement* (the comparator challenge): a human or the model. | UNKNOWN | — |
| U6 | Whether any human mathematician has checked the informal proof end to end. | UNKNOWN (no public statement found) | — |
| U7 | Model name, size, training. | UNKNOWN | — |
| U8 | Failed or incorrect attempts on this problem before success. | UNKNOWN | — |

**What a published reasoning summary looks like (different result; usable on screen with a label).** Family 017, "The irrationality exponent of π is 2", 42 pages, titled "Summarized chain of thought". It alternates third-person summary ("The assistant sought…", "Derivative denominators defeated this") with short "VERBATIM EXCERPT" blocks, for example: *"Polynomial log imposes finitely many parameters, eliminates arbitrary infinite path. Degree C huge but fixed; need theorem using its structure."* It records many abandoned approaches. Family 159's summary shows an original prompt excerpt in "Prove or disprove…" form. [reasoning_traces PDFs, p. 1]

## 8. Verification status: keep the terms distinct

| Term | Status for this result | Evidence |
|---|---|---|
| **AI-generated** | Yes, per the repo (F1); the procedure for this specific result is inferred (I1). | README |
| **Computer-checked (small certificate)** | The paper's rational certificate is checkable by hand. Our code checks symbolic geometry and high-precision placement inequalities (pass). | §6 above |
| **Formally verified (Lean)** | OpenAI publishes a Lean 4 + Mathlib formalization. The comparator challenge states: `theorem no_proper_five_coloring : ¬ ∃ coloring : ℂ → Fin 5, ProperColoring 5 coloring`, where `ProperColoring` means ‖p − q‖ = 1 → different colours, for **all** points and **arbitrary** functions (no measurability or continuity). Permitted axioms: `propext`, `Quot.sound`, `Classical.choice` (Lean's standard classical axioms). `enable_nanoda: false` (no second independent kernel check configured). The top-level proof (`OAI/Geometry/PlaneColoring/Five.lean`) mirrors the paper's two halves: `proper_to_borel_weak`, then `no_measurable_weak_five_coloring`. Some internal choices differ in detail (e.g. a radius-5 disk instead of the paper's side-10 square). Size: about 30,850 lines across `PlaneColoring` (46 files, 14,661 lines), `PlaneSpectrum` (19 files, 8,466 lines) and `CompactFactors` (14 files, 7,728 lines), importing only Mathlib. **Our static scan found no `sorry`, no `axiom` declarations and no `native_decide`.** We have **not** built the project or run the comparator ourselves. The 7-colouring is formalised separately (`PlaneColoring.json`, `properColoring_seven`). | lean/docs/158.md; ComparatorChallenges/*.lean, *.json; scan 2026-10-07 |
| **Independently reproduced** | No public evidence of an independent reproduction of the proof or of the Lean build. | — |
| **Peer reviewed** | No. It is a preprint in a company repository; no journal or referee report is cited. | preprint README |
| **Formalization reviewed by humans** | The catalogue's `review: status: unchecked` (catalogue-wide field). | formalization.yaml |

What a successful Lean check would and would not establish:
- It **would** establish: that statement follows from Lean's kernel rules and those three axioms, assuming the Lean kernel and toolchain are correct. The statement is 6 lines and readable, so whether it says what we mean can be checked by eye. It does: all colourings ℂ → 5 colours, distance exactly 1.
- It **would not** establish: that the *paper's* informal argument is correct line by line (the formal proof is a separate artefact that follows the same architecture), or any claim about how the result was found.
- Optional at Checkpoint A: attempt a local build plus comparator run (needs elan, Mathlib cache of several GB, `comparator`, `landrun`, `lean4export`). This would upgrade our wording from "OpenAI reports a formalization" to "we re-ran the check".

## 9. Open questions

1. Is χ(ℝ²) equal to 6 or 7? Open. [P §1]
2. What is the smallest finite unit-distance graph that is not 5-colourable? Its existence is guaranteed (compactness); no example is known publicly; the paper's argument does not produce one. [P Cor 1.5 proof]
3. Does the transfer theorem plus a measurable-style argument reach 7? The paper says nothing about this. Do not speculate on screen beyond "the transfer holds for every number of colours". [P Thm 1.3]
4. Human verification of the informal proof, and community reproduction of the Lean build: status unknown.

## 10. Mathematical points I am unsure about (to flag in the final report)

- Exact phrasing of **density/"typical" points** for a lay audience: we simplify "density one" to "zooming in, the point's neighbourhood is essentially all its colour".
- The **palette** is defined via weak-* limits at nearby centres and radii tending to 1, not by literally reading the colour on the circle. On screen we show "reading the ring" and say "in a limiting sense" once.
- The **planar cover obstruction** (Lemma 7.5) is stated for open covers with multiplicity ≤ 2 and mesh ≤ 2 on a side-10 square. The "tiles must have triple points" toy is an analogy for this dimension-theory fact, not a restatement.
- The **4-cycle case** is the least intuitive. We will present only the parity contradiction and say that the geometric lemmas forcing it are skipped.
- The **rigidity theorem** is presented only through an analogy (signal plus "perfect noise": noise uncorrelated with itself at every nonzero shift). The analogy matches the conclusion used (zero correlation of the remainder at nonzero algebraic shifts, Prop 4.2), not the proof.

## 11. Toy problems for the hard ideas (mine; not from the paper unless stated)

- **T1. Unit stick.** A rigid stick of length 1 dropped anywhere on a coloured plane; its two ends must differ. (Act 1)
- **T2. Circle with a forbidden step** (for "wild versus measurable"). Points of a circle; join θ and θ + α for a fixed irrational angle α (in turns). With the axiom of choice, a 2-colouring exists: alternate along each orbit. No **measurable** 2-colouring exists: if c(θ + α) ≠ c(θ), then c(θ + 2α) = c(θ), so c is invariant under the irrational rotation 2α, so it is constant almost everywhere (Fourier/ergodicity), a contradiction. This mechanism is exactly the one the paper uses in Lemma 6.4 (cos γ = 5/6, γ/π irrational). Payne's rational-displacement graph [P §1] is the paper's own plane-level version of the same warning.
- **T3. Signal plus perfect noise** (for rigidity). A random pattern split into a smooth part and a "perfectly scrambled" part whose correlation with any shifted copy of itself is zero. Throwing the scrambled part away cannot change the unit-distance correlation. Label this as an analogy.
- **T4. Tiles and triple points** (for Lemma 7.5): bricks, hexagons and squares all have points where ≥ 3 tiles meet when the tiles are small.
- **T5. Pentagon walk** (for Prop 8.2): ±1 steps around a 5-clock, six steps that must close, antipodal constraint. Directly the paper's argument.

## 12. Sources

Primary
- [P] OpenAI, "The Euclidean plane is not five-colorable", preprint dated Sep 23, 2026. github.com/openai/math, `preprints/The-Euclidean-plane-is-not-five-colorable-September-23-2026/` (paper.pdf; build/sections/*.tex; build/figures/*.tex). Retrieved 2026-10-07.
- openai/math `README.md`, `CONTENTS.md` (family 158), `lean/docs/158.md`, `lean/formalization.yaml`, `lean/ComparatorChallenges/{EuclideanFiveColor,PlaneColoring}.{lean,json}`, `lean/OAI/Geometry/PlaneColoring/*`, `lean/OAI/Analysis/PlaneSpectrum/*`, `lean/OAI/MeasureTheory/CompactFactors/*`. Retrieved 2026-10-07.
- openai/math `reasoning_traces/irrationality-exponent-of-pi.pdf`, `reasoning_traces/quasipolynomial-arithmetic-progressions.pdf`.
- [OpenAI, "Sharing AI progress in mathematics"](https://openai.com/index/sharing-ai-progress-in-mathematics/), 6 Oct 2026. Inaccessible during script research; accessible during release preparation on 2026-10-07. Used for release context, not as verification of the proof.

Background (as cited by the paper unless noted)
- A. D. N. J. de Grey, "The chromatic number of the plane is at least 5", Geombinatorics 2018; arXiv:1804.02385 (v1 8 Apr 2018, v3 30 May 2018).
- M. J. H. Heule, "Computing small unit-distance graphs with chromatic number 5", Geombinatorics 2018; arXiv:1805.12181.
- J. Parts, "The chromatic number of the plane is at least 5: a human-verifiable proof", arXiv:2010.12661; "Graph minimization…", arXiv:2010.12665.
- G. Exoo, D. Ismailescu, DCG 2020, doi:10.1007/s00454-019-00058-1.
- L. Moser, W. Moser, Canad. Math. Bull. 4 (1961), solution to Problem 10.
- H. Hadwiger, "Ungelöste Probleme Nr. 40", Elem. Math. 16 (1961).
- A. Soifer, "The 50th anniversary of one problem…", Mathematics Competitions 2003, pp. 15–19.
- N. G. de Bruijn, P. Erdős, Indag. Math. 1951.
- K. J. Falconer, JCTA 1981, doi:10.1016/0097-3165(81)90014-5.
- M. S. Payne, EJC 2009, doi:10.37236/269.
- D. R. Woodall, JCTA 1973. S. P. Townsend, JCTA 1981; Geombinatorics 2005.
- G. Sokolov, V. Voronov, arXiv:2502.01958 (2025).
- S. Shelah, A. Soifer, "Axiom of choice and chromatic number of the plane", JCTA 103(2) (2003) 387–391 (not cited by the paper; used only for context).
- Okabe & Ito, "Color Universal Design" palette (for the visual identity; not a mathematical source).

Secondary (release context only)
- Interesting Engineering, "OpenAI's largest math release tackles 4000 problems…" (Oct 2026).
- Unite.AI, "OpenAI Releases 722 Math Manuscripts From an Unreleased AI Model" (Oct 2026).
