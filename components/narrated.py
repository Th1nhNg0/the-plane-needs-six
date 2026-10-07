"""NarratedScene: a Scene whose timeline is driven by measured narration timing.

audio/scenes/<id>.timing.json  gives segment start/end (seconds) -> cue(k)
audio/scenes/<id>.words.json   gives word start times            -> word("orange", n)
Animation code calls `self.until(t)` to wait to an absolute time, and `self.play_at(t, *anims, run_time=...)`.
Overruns (animation still running when a cue should start) are logged to renders/sync_log.txt for QA.
"""
import json
import re
from pathlib import Path

from manim import Scene, VGroup, config

from .style import BG

ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / "audio" / "scenes"


def _norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


class NarratedScene(Scene):
    scene_id = None  # e.g. "s2_3"
    with_audio = True

    def setup(self):
        self.camera.background_color = BG
        self.bg = VGroup()          # v2 look: plain ground, no texture
        t = json.loads((AUDIO / f"{self.scene_id}.timing.json").read_text())
        self.segments = t["segments"]
        self.audio_duration = t["duration"]
        wpath = AUDIO / f"{self.scene_id}.words.json"
        self.words = json.loads(wpath.read_text()) if wpath.exists() else []
        self._overruns = []
        if self.with_audio:
            self.add_sound(str(AUDIO / f"{self.scene_id}.wav"))

    def clear_stage(self):
        """Remove everything except the background plate."""
        self.clear()
        self.add(self.bg)

    # time ---------------------------------------------------------------------------
    @property
    def now(self):
        return self.renderer.time

    def cue(self, k, offset=0.0):
        """Start time of narration segment k (1-based) plus offset."""
        return self.segments[k - 1]["start"] + offset

    def cue_end(self, k):
        return self.segments[k - 1]["end"]

    def frac(self, k, f):
        """Time at fraction f through narration segment k (for beats inside long segments)."""
        s = self.segments[k - 1]
        return s["start"] + f * (s["end"] - s["start"])

    def left(self, t):
        """Seconds from now until absolute time t (minimum 0.2) — handy as run_time."""
        return max(t - self.now, 0.2)

    def word(self, w, n=1, after=0.0):
        """Start time of the n-th occurrence of word w at or after time `after`."""
        target, seen = _norm(w), 0
        for x in self.words:
            if x["s"] >= after and _norm(x["w"]) == target:
                seen += 1
                if seen == n:
                    return x["s"]
        raise KeyError(f"word {w!r} #{n} after {after} not found in {self.scene_id}")

    def wc(self, k, w, n=1):
        """Start time of the n-th occurrence of word w inside narration segment k (robust to repeated words)."""
        seg = self.segments[k - 1]
        target, seen = _norm(w), 0
        for x in self.words:
            if seg["start"] - 0.6 <= x["s"] <= seg["end"] + 0.3 and _norm(x["w"]) == target:
                seen += 1
                if seen == n:
                    return x["s"]
        raise KeyError(f"word {w!r} #{n} not in segment {k} of {self.scene_id}")

    def until(self, t, label=""):
        dt = t - self.now
        if dt > 1e-3:
            self.wait(dt)
        elif dt < -0.05:
            self._overruns.append((label or f"t={t:.2f}", round(-dt, 2)))

    def play_at(self, t, *anims, label="", **kw):
        self.until(t, label)
        self.play(*anims, **kw)

    def finish(self):
        self.until(self.audio_duration, "end")
        log = ROOT / "renders" / "sync_log.txt"
        log.parent.mkdir(exist_ok=True)
        lines = [l for l in (log.read_text().splitlines() if log.exists() else []) if not l.startswith(self.scene_id + " ")]
        lines.append(f"{self.scene_id} duration={self.audio_duration:.2f} rendered={self.now:.2f} overruns={self._overruns}")
        log.write_text("\n".join(sorted(lines)) + "\n")
