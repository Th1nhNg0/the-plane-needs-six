# Chapter 6 · What the AI did, and what we don't know (target 3:30)

Every on-screen claim in this chapter carries a status tag (`FACT` with source line, `INFERENCE — possible reconstruction, not confirmed by OpenAI`, or `NOT PUBLIC`). No narrated inner monologue for the model.

## S6.1 · What OpenAI states
`id: s6_1` · `target: 1:00` · `time: 32:00–32:54 (est.)`

**NARRATION**
> So who wrote this? The preprint is dated September twenty-third, 2026, and its listed author is simply "OpenAI". It's one of seven hundred and twenty-two manuscripts in a public repository that, according to OpenAI, were produced by an internal OpenAI model, one that hasn't been released. [beat] Here's what the repository says about the process. The vast majority of results came from the same procedure. Over the course of the evaluation, the model was posed about four thousand problems. On average, each result used three hours of ChatGPT Pro thinking compute with that model. [beat] The outputs were then grouped into families, and only results meeting a bar of significance were kept. [beat] Notice what kind of number that three hours is: an average across results, not a figure for this proof.

**VISUAL**
1. A repository panel (generic file-tree styling, no logos): "722 manuscripts · 372 families". `FACT` tag, source line "openai/math README". → cue 1
2. Three stat cards, each with a `FACT` tag: "≈ 4,000 problems posed" · "average ≈ 3 h ChatGPT Pro thinking compute per result" · "unreleased internal model". → cue 2
3. Funnel: 4,000 problems → families → "significance bar" → 722 manuscripts. → cue 3
4. The "3 h" card gets an underline "average across results". → cue 4

**ON-SCREEN**
- Quoted (small, verbatim): "On average, each result used three hours of ChatGPT Pro thinking compute with that model." "…the model was posed approximately 4,000 problems."
- Source line: github.com/openai/math · README · "How the results were produced"

**SOURCE**
- brief §7 F1–F5 (README; preprint README).

**MUST UNDERSTAND**
- What is officially stated, and that the compute figure is an average.

## S6.2 · What isn't public
`id: s6_2` · `target: 0:50` · `time: 32:54–33:32 (est.)`

**NARRATION**
> And here's what isn't public. OpenAI released condensed reasoning summaries for ten results. This is not one of them. [beat] So we don't know the exact prompt, how many attempts were made, what tools the model could use, how much compute this particular proof took, or whether people steered it along the way. [beat] A few things can be reasonably inferred. This result isn't listed among the exceptions to the standard procedure, so it probably followed it. But that's an inference, not a statement from OpenAI, and it's labelled that way.

**VISUAL**
1. A list of the ten families with published summaries; "158 · five-colour plane" is checked against the list: absent. → cue 1
2. A grid of question cards with `NOT PUBLIC` tags: "prompt", "attempts", "tools", "compute for this result", "human steering", "who wrote the Lean statement". → cue 2
3. One card with the `INFERENCE — possible reconstruction, not confirmed by OpenAI` banner: "standard procedure (not listed as an exception)". → cue 3

**ON-SCREEN**
- `NOT PUBLIC` ×6 · `INFERENCE — possible reconstruction, not confirmed by OpenAI`

**SOURCE**
- brief §7 F7, I1, U1–U5.

**MUST UNDERSTAND**
- The gap between what is stated and what is unknown.

## S6.3 · What a summary looks like (from a different result)
`id: s6_3` · `target: 0:50` · `time: 33:32–34:03 (est.)`

**NARRATION**
> To give a sense of what these summaries look like, here's one from a different result, about the irrationality exponent of pi. It's a forty-two-page condensed record: short descriptions of attempts, many of them abandoned, mixed with brief verbatim fragments like this one. [beat] It shows a process with dead ends and changes of direction. But it's a different problem, and it tells us nothing specific about how the five-colour proof was found.

**VISUAL**
1. Banner across the top: "DIFFERENT RESULT · family 017 · not the five-colour proof". A page mock (our typesetting) titled "Summarized chain of thought (The irrationality exponent of π is 2)". → cue 1
2. Highlight a verbatim fragment. Sidebar of struck-through approach names to show "abandoned attempts" (generic labels: "approach A ✗", "approach B ✗"). → cue 1 (continued)
3. A wall separates this page from the five-colour paper icon: "no summary for this result". → cue 2

**ON-SCREEN**
- Verbatim excerpt (from the published summary of family 017): "Polynomial log imposes finitely many parameters, eliminates arbitrary infinite path. Degree C huge but fixed; need theorem using its structure."
- Source line: openai/math · reasoning_traces/irrationality-exponent-of-pi.pdf, p. 1

**SOURCE**
- brief §7 ("What a published reasoning summary looks like").

**MUST UNDERSTAND**
- Summaries exist for other results; we can't project them onto this one.

## S6.4 · Reasoning or brute force?
`id: s6_4` · `target: 0:50` · `time: 34:03–34:48 (est.)`

**NARRATION**
> So, was this reasoning or brute force? For the proof itself, the answer is clear: there's no brute force in it. No search over graphs, no solver, just one seven-point check. Its content is conceptual: averaging and symmetry, topology, geometry. And it openly builds on known tools, from Falconer's density points to the interface ideas of Sokolov and Voronov, which the paper credits. [beat] For the process, it's less clear. Posing four thousand problems and keeping only the significant results is itself a kind of search, at a very large scale. How much of the selection was automatic, and how often the model was wrong along the way, isn't public.

**VISUAL**
1. Two-pan scale labelled "in the proof": "search / computation" pan nearly empty (one tiny "7-point check" weight), "concepts" pan full (icons: averaging, topology loop, sixty-degree rhombus, Moser spindle). Citation chips float in: "Falconer 1981", "Payne 2009", "Furstenberg–Zimmer", "Townsend", "Sokolov–Voronov 2025". → cue 1
2. A second panel, "in the process": the 4,000 → 722 funnel again, with a `NOT PUBLIC` tag over "selection details" and "error rate". → cue 2

**ON-SCREEN**
- "in the proof: 1 small certificate, no search" · "in the process: 4,000 problems → selected results (details not public)"

**SOURCE**
- Proof content and credits: P §1 (Falconer, Payne, Furstenberg–Zimmer, Sokolov–Voronov), P §8 (Townsend, Sokolov–Voronov), P §8.6; brief §6.
- Process: README (brief F4); unknowns U2, U4, U8.

**MUST UNDERSTAND**
- "Reasoning vs brute force" has different answers for the proof's content and for the (largely unknown) process.
