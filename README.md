# The Plane Needs Six

I asked Opus 5.5 to create a 3Blue1Brown-inspired animated video to help me understand
OpenAI's preprint *The Euclidean plane is not five-colorable*, from its
[math release](https://openai.com/index/sharing-ai-progress-in-mathematics/).

The film explains the Hadwiger–Nelson colouring problem, the Moser spindle, and the
preprint's proposed proof that five colours cannot suffice. It also discusses what
OpenAI reports about the AI's role and formal verification. This repository contains
the English scripts, Manim animations, research notes, and audio/video build tools.

Made with Opus 5.5 and ElevenLabs.

## Run

Use Linux or WSL with Python 3.12, [uv](https://docs.astral.sh/uv/), FFmpeg (including
`ffprobe`), Cairo, Pango, and LaTeX with `dvisvgm`. On Debian/Ubuntu/Kali:

```bash
sudo apt install build-essential python3-dev pkg-config libcairo2-dev libpango1.0-dev \
  ffmpeg texlive-latex-extra texlive-fonts-recommended texlive-science dvisvgm
```

From the repository root:

```bash
uv venv --python 3.12
uv pip install --python .venv/bin/python -r requirements.txt
cp .env.example .env
# Set ELEVENLABS_API_KEY in .env, or export it in your shell.
./build.sh
```

The build generates narration through ElevenLabs, aligns it locally using
faster-whisper, renders 34 scenes, and assembles `renders/final.mp4` and
`renders/final.srt`. The default is 1080p60; `QUALITY=l JOBS=2 ./build.sh` produces a
480p draft with two render workers. Narration is cached by text hash. A fresh build
makes paid API calls; alignment may download the `small.en` model on first use.

Optional music generation is a separate paid step:

```bash
.venv/bin/python tools/generate_music.py
.venv/bin/python tools/mix_music.py
```

Mixing uses cached chapter tracks and writes `renders/final_with_music.mp4` and a
matching SRT. It makes no API calls. Voice and music settings are in `config/`.

## Files

- `scripts/`: chapter narration and storyboards; `narration.json` is generated.
- `scenes/` and `components/`: Manim scenes and reusable visual helpers.
- `tools/`: narration, alignment, rendering, assembly, and verification examples.
- `research/`: source-tagged brief, insight map, and dependency graph.

This is a source-only repository. Audio, video, caches, local production records,
and downloaded reference copies are git-ignored and stay local. Downloaded references
are not needed to render the film; citations are in [the research brief](research/brief.md#12-sources).

## Verification and sources

The film explains a preprint. OpenAI's
[formalization notes](https://github.com/openai/math/blob/main/lean/docs/158.md)
describe the no-five-colouring and seven-colouring statements. This project does not
rebuild or independently certify the complete Lean formalization.

To check the small Moser-spindle and seven-point placement examples used in the film:

```bash
.venv/bin/python tools/verify_moser_certificate.py
```

The checker uses symbolic unit-edge calculations and high-precision placement
inequalities. The examples in `tools/lean_toy/` illustrate Lean proof checking on a
triangle, separately from the preprint's formalization.

Read the [paper](https://github.com/openai/math/blob/main/preprints/The-Euclidean-plane-is-not-five-colorable-September-23-2026/paper.pdf)
and [research brief](research/brief.md) for sources, simplifications, and unresolved
questions. The visual style is inspired by 3Blue1Brown; this is an independent project.
