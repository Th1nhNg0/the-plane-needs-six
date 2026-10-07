# Script and storyboard: "The Plane Needs Six"

One file per chapter (`ch0.md` … `ch8.md`). Each scene has this fixed shape, which `tools/script_tool.py` parses:

```
## S<chapter>.<n> · <title>
`id: s<c>_<n>` · `target: m:ss` · `time: <estimated start–end>`

**NARRATION**
> spoken prose … [beat] … more prose

**VISUAL**  numbered animation beats; "→ cue k" ties a visual beat to the k-th narration segment
**ON-SCREEN**  text and maths that appear (LaTeX only for formulas)
**SOURCE**  claim → source (brief.md section / paper section)
**MUST UNDERSTAND**  what the viewer needs before moving on
```

## Narration conventions
- Spoken prose only. Numbers that matter are written as words when TTS might misread them; formulas are spelled out.
- `[beat]` = pause (≈ 0.6 s; `[beat2]` ≈ 1.4 s). The narration is split at beats into **segments**. Each segment is one TTS clip, and the gaps are inserted as silence at assembly. So measured segment durations are the animation cue points, and editing one sentence regenerates one segment only.
- Status tags on screen: `FACT`, `INFERENCE — possible reconstruction, not confirmed by OpenAI`, `NOT PUBLIC`, `ANALOGY`, `TOY PROBLEM`.
- First person ("I") is the narrator's voice and is used only for things this production did (for example, re-checking the certificate).

## Timing
`time:` values are estimates at 150 words per minute plus beat silences, computed by `tools/script_tool.py timing`.
Measured audio replaces them in Phase 8.
