# Chapter 1 · The colouring game (target 4:00)

## S1.1 · Exactly one
`id: s1_1` · `target: 0:50` · `time: 1:06–1:44 (est.)`

**NARRATION**
> Let's be precise about the rule, because it's stranger than it sounds. [beat] Two points exactly one unit apart must get different colours. That's the only constraint. [beat] Two points at distance zero point nine nine nine? They're allowed to match. One point zero zero one? Also fine. Only the exact distance one is forbidden. [beat] And "colour every point" really does mean every point. Not a pattern of tiles, not regions with tidy borders. Any assignment at all is allowed: each point simply gets a colour, and that's it.

**VISUAL**
1. A unit stick in close-up between two pins; the distance indicator (callipers) above it. → cue 1
2. The pins get colours; the indicator reads 1.000; the pins must differ (orange ●, sky ▲). → cue 2
3. The right pin slides: indicator 0.999, both pins orange, a quiet tick ✓; then 1.001, both orange, ✓; back to 1.000, both orange: clash spark. → cue 3
4. Zoom out: the plane as a field of individual dots, each flicking to a random colour independently (no regions), to show "each point simply gets a colour". → cue 4

**ON-SCREEN**
- Distance readouts `0.999` · `1.000` · `1.001`.
- Rule card (small, lower-left, stays through Ch 1): "distance exactly 1 ⇒ different colours".

**SOURCE**
- Definition of proper colouring, no regularity: P §1 para 1; brief §1.

**MUST UNDERSTAND**
- Only exact unit distance matters; colourings can be completely arbitrary.

## S1.2 · Two colours
`id: s1_2` · `target: 1:10` · `time: 1:44–2:45 (est.)`

**NARRATION**
> So, start small. Can two colours work? [beat] Stripes are the natural first try. Make each stripe a little narrower than one, alternating orange and blue. Drop the stick straight across, and the ends land on different stripes. [beat] Tilt it, and both ends can land in the same stripe, or two stripes apart, which have the same colour. [beat] Checkerboards fail in the same way. So do rings. [beat] It's worth pausing here to hunt for a two-colouring yourself. [beat2] Here's why every attempt is doomed. Take three points, each exactly one unit from the other two: an equilateral triangle with side one. [beat] Every pair of corners needs different colours. Three corners, all different from each other, takes three colours. [beat] So two can never be enough. It has nothing to do with clever patterns: just three points are enough to rule it out.

**VISUAL**
1. Vertical stripes of width 0.8, orange ● / sky ▲. → cue 1
2. A horizontal stick spans two adjacent stripes, ✓. → cue 2
3. The stick tilts until both pins sit in the same stripe: clash. Then it slides so the pins are two stripes apart (same colour): clash. → cue 3
4. Quick montage (1 s each): checkerboard with a diagonal stick clash; concentric rings with a chord stick clash. → cue 4
5. Everything dims; a pause card "try it" with a 2-second idle (no motion). → cue 5
6. Three points appear and are joined by three unit sticks into a triangle; the pins colour one at a time: orange, sky, then the third tries orange (clash with the first) and sky (clash with the second). → cue 6–7
7. The third corner turns green ■. Caption "needs 3". → cue 8

**ON-SCREEN**
- "2 colours?" header. Final: "triangle ⇒ at least 3".

**SOURCE**
- Standard (equilateral triangle argument). Brief §11 T1.

**MUST UNDERSTAND**
- Three mutually unit-distance points force three colours.

## S1.3 · Three colours
`id: s1_3` · `target: 1:40` · `time: 2:45–3:54 (est.)`

**NARRATION**
> So, three colours. The triangle is happy now: one corner orange, one blue, one green. [beat] Let's try to paint the whole plane. A natural idea is to tile it with hexagons and use three colours, so that neighbouring hexagons always differ. [beat] Watch the stick. If the hexagons are small enough, no two points inside one hexagon are a full unit apart, so that's safe. Neighbouring hexagons have different colours, so that's safe too. [beat] But with only three colours, hexagons of the same colour are never far apart, only one hexagon away, and the stick can reach from one to the other. [beat] Make the hexagons bigger, and now the stick fits inside a single hexagon. [beat] There seems to be no comfortable size. [beat2] That's not a proof that three colours fail, only that this attempt does. Maybe some cleverer, stranger pattern works. [beat] If you like, pause here and try to break three colours yourself, or to rescue them.

**VISUAL**
1. The triangle from S1.2 settles in a corner with its three colours. → cue 1
2. Hexagon tiling, circumradius 0.4, 3-coloured (orange ●, sky ▲, green ■) in the standard pattern. → cue 2
3. A stick inside one hexagon (too short to reach across: the indicator max reads 0.800) ✓; a stick across a shared edge ✓. → cue 3
4. Highlight two same-colour hexagons one hexagon apart (gap 0.4); the stick rotates until its pins land in both: clash. → cue 4
5. The tiling scales up smoothly to circumradius 0.6 (diameter 1.2); a stick inside one hexagon: clash. → cue 5
6. A size slider shows red "clash" marks at both ends. → cue 6
7. The tiling fades to a question mark between "3" and "4". → cue 7–8

**ON-SCREEN**
- "3 colours?" · hexagon size slider labels "small" / "large".

**SOURCE**
- Construction is ours (illustrative). The geometry is checked in the production code: with circumradius 0.4, same-colour hexagons have gap 0.4 and maximum distance 2.0, so a unit pair exists; with circumradius 0.6, the diameter is 1.2 > 1.

**MUST UNDERSTAND**
- Trying patterns doesn't settle the question; we need reasoning.

## S1.4 · Too many to try
`id: s1_4` · `target: 0:20` · `time: 3:54–4:12 (est.)`

**NARRATION**
> Painting experiments will never settle this. There are infinitely many points, and infinitely many ways to colour them. [beat] We need a way to reason about all colourings at once, and the first step is to look past the paint, at the stick itself.

**VISUAL**
1. Rapid flicker through dozens of random colourings of the plane. → cue 1
2. The paint drains away, leaving only one stick, highlighted. → cue 2

**ON-SCREEN**
- none

**SOURCE**
- n/a (framing)

**MUST UNDERSTAND**
- Motivation for the graph view.
