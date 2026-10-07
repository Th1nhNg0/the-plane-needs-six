# Chapter 7 · Checking it (target 3:30)

## S7.1 · A tiny Lean proof
`id: s7_1` · `target: 1:10` · `time: 34:48–35:52 (est.)`

**NARRATION**
> Whoever wrote it, is it right? A sixty-two-page proof that runs through ergodic theory and topology is hard to check. And "an AI produced it" is a statement about where it came from, not about whether it's correct. [beat] This is where proof assistants come in. Lean is a programming language in which you can state a theorem precisely and write a proof, which a small, trusted program, called the kernel, checks step by step. [beat] Here's a toy. The statement: if the three corners of a triangle get colours from just two options, then some two corners match. Lean checks all the cases and accepts. [beat] Now change the claim to something false: that three options aren't enough either. Lean refuses. [beat] A proof can be long, and written by anyone, or anything. The trust rests on the small kernel, and on reading the statement carefully to make sure it says what we mean.

**VISUAL**
1. The 62-page paper as a stack; a "who wrote it?" tag and an "is it right?" tag pulled apart into two separate dials. → cue 1
2. Diagram: big untrusted box "proof (any author)" → small trusted box "kernel" → ✓/✗. → cue 2
3. Code panel (monospace, our colours):
   ```lean
   theorem triangle_two_colours :
       ∀ a b c : Bool, a ≠ b → b ≠ c → a ≠ c → False := by
     decide
   ```
   Kernel lamp: ✓ "accepted". → cue 3
4. Edit `Bool` to `Fin 3`; kernel lamp ✗ with the actual Lean 4.34.1 error: "Tactic `decide` proved that the proposition … is false". → cue 4
5. Back to the diagram, with the statement highlighted as "read by humans". → cue 5

**ON-SCREEN**
- Lean toy code: verified 2026-10-07 with Lean 4.34.1 core (`tools/lean_toy/Accepted.lean` accepted, exit 0; `Rejected.lean` rejected, exit 1).
- "kernel: small, trusted" · "proof: any author" · "statement: read it"

**SOURCE**
- General description of proof assistants; toy is ours, compiled with Lean 4.34.1.

**MUST UNDERSTAND**
- Generated vs checked; the role of the statement.

## S7.2 · This result in Lean
`id: s7_2` · `target: 1:30` · `time: 35:52–37:01 (est.)`

**NARRATION**
> OpenAI's repository includes a Lean formalization of this result. Here is the statement it proves, in full. [beat] A colouring is any function from the plane, written as the complex numbers, to five colours. "Proper" means: any two points at distance exactly one get different colours. The theorem: no proper colouring exists. [beat] Notice what's missing: no assumption that the colour regions are measurable, or nice in any way. This is the unrestricted problem. [beat] The checking setup allows only Lean's three standard axioms, the usual foundations for classical mathematics. The formal proof behind the statement runs to roughly thirty thousand lines, built on Lean's mathematics library, and it follows the same two halves as the paper. There's a separate formalization of the seven-colour hexagon bound, too. [beat] So the accurate summary is: OpenAI reports a formal verification of the full, unrestricted statement. I scanned the published files for the usual escape hatches, unfinished steps or extra axioms, and found none, but I did not rebuild the proof myself.

**VISUAL**
1. Code panel with the comparator statement, verbatim:
   ```lean
   def ProperColoring (colorCount : ℕ) (coloring : ℂ → Fin colorCount) : Prop :=
     ∀ point otherPoint : ℂ, ‖point - otherPoint‖ = 1 → coloring point ≠ coloring otherPoint

   theorem no_proper_five_coloring : ¬ ∃ coloring : ℂ → Fin 5, ProperColoring 5 coloring
   ```
   (The `:= by sorry` placeholder of the challenge file is not shown; a footnote explains that the challenge file holds only the statement and the proof is checked against it.) → cue 1
2. Tokens light up with plain-language glosses: `ℂ → Fin 5` "any function, plane → 5 colours"; `‖point - otherPoint‖ = 1` "distance exactly 1"; `¬ ∃` "no such colouring". → cue 2
3. A ghost line "measurable?" drifts in and is struck out: "not assumed". → cue 3
4. Badge row: "axioms: propext · Quot.sound · Classical.choice" · "≈ 30,000 lines · Mathlib" · "two parts: proper → weak measurable; no weak measurable 5-colouring" · "7-colouring formalized separately". → cue 4
5. Status line `FACT`: "OpenAI reports a Lean formalization" · production note: "static scan: no `sorry`, no extra axioms · not rebuilt by us". → cue 5

**ON-SCREEN**
- Verbatim Lean statement; source line "openai/math · lean/ComparatorChallenges/EuclideanFiveColor.lean".
- "permitted axioms: propext, Quot.sound, Classical.choice" (from EuclideanFiveColor.json).

**SOURCE**
- brief §8 (lean/docs/158.md; comparator .lean/.json; Five.lean; line counts; scan 2026-10-07).

**MUST UNDERSTAND**
- The formal statement covers arbitrary colourings; the status is "reported by OpenAI", not reproduced here.

## S7.3 · Five words, five meanings
`id: s7_3` · `target: 0:50` · `time: 37:01–37:36 (est.)`

**NARRATION**
> Let's keep five words apart. [beat] AI-generated: yes, according to OpenAI. [beat] Computer-checked: the one explicit calculation is small, and it checks out. [beat] Formally verified, meaning checked by a proof assistant: OpenAI reports a Lean proof of the full statement. [beat] Independently reproduced: I found no public reproduction yet. [beat] Peer reviewed: no. It's a preprint in a company repository, and the repository's catalogue of formalizations lists their review status, as a whole, as "unchecked". [beat] These are different claims, and they deserve different levels of confidence.

**VISUAL**
1. Five rows appear one per cue, each with a status lamp:
   - "AI-generated" · lamp: ✓ "per OpenAI" → cue 2
   - "computer-checked (7-point certificate)" · ✓ "re-checked by us" → cue 3
   - "formally verified (Lean)" · ✓ "reported by OpenAI" → cue 4
   - "independently reproduced" · ○ "no public evidence" → cue 5
   - "peer reviewed" · ○ "no" + small chip "catalogue review status: unchecked" → cue 6
2. The rows stay on screen as a reference card. → cue 7

**ON-SCREEN**
- The five-row table above.

**SOURCE**
- brief §8 table; formalization.yaml `review: status: unchecked` (catalogue-wide).

**MUST UNDERSTAND**
- The five verification terms are distinct.
