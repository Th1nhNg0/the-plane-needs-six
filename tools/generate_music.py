"""Generate and cache the approved ElevenLabs instrumental chapter tracks.

Run from project: .venv/bin/python tools/generate_music.py
Never enables overage billing or prints/stores credentials. Re-running uses valid cached tracks.
"""
import hashlib
import json
import os
import subprocess
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "config/music.json").read_text())
DEST = ROOT / "audio/music"
MANIFEST = DEST / "manifest.json"


def key():
    if os.environ.get("ELEVENLABS_API_KEY", "").strip():
        return os.environ["ELEVENLABS_API_KEY"].strip()
    for envfile in (ROOT / ".env", ROOT.parent / ".env"):
        if envfile.exists():
            for line in envfile.read_text().splitlines():
                if line.strip().startswith("ELEVENLABS_API_KEY="):
                    value = line.split("=", 1)[1].strip().strip("\"'")
                    if value:
                        return value
    raise SystemExit("Set ELEVENLABS_API_KEY in your environment or .env")


def subscription(api_key):
    req = urllib.request.Request("https://api.elevenlabs.io/v1/user/subscription",
                                 headers={"xi-api-key": api_key})
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.load(r)
    return {k: d.get(k) for k in ("tier", "status", "character_count", "character_limit",
                                  "can_extend_character_limit")}


def probe(path):
    d = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_name,sample_rate,channels",
        "-of", "json", str(path)]))
    return {"duration_s": float(d["format"]["duration"]), "streams": d["streams"]}


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {"tracks": {}, "runs": []}
    api_key = key()
    before = subscription(api_key)
    print("Subscription before:", json.dumps(before), flush=True)
    run = {"started_utc": datetime.now(timezone.utc).isoformat(), "before": before}
    manifest["runs"].append(run)
    MANIFEST.write_text(json.dumps(manifest, indent=2))
    for ch in CFG["chapters"]:
        body = {"prompt": CFG["common_prompt"] + " " + ch["mood"],
                "music_length_ms": ch["length_ms"], "model_id": CFG["model_id"],
                "force_instrumental": CFG["force_instrumental"]}
        fingerprint = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()
        path = DEST / f"ch{ch['chapter']}_{ch['name']}.mp3"
        prior = manifest["tracks"].get(str(ch["chapter"]), {})
        if (path.exists() and prior.get("request_sha256") == fingerprint and
                hashlib.sha256(path.read_bytes()).hexdigest() == prior.get("audio_sha256")):
            info = probe(path)
            if abs(info["duration_s"] - ch["length_ms"] / 1000) < 1:
                print("Cached:", path.name, flush=True)
                continue
        current = subscription(api_key)
        spent = current["character_count"] - before["character_count"]
        # Reserve enough credits for the next track, with room for delayed billing.
        reserve = ch["length_ms"] / 1000 * 20
        if spent + reserve > CFG["max_session_credits"]:
            raise SystemExit("Music generation stopped at the configured session credit budget")
        if current["character_limit"] - current["character_count"] < reserve:
            raise SystemExit("Insufficient included credits; overage billing was not enabled")
        print("Generating:", path.name, ch["length_ms"] / 1000, "seconds", flush=True)
        req = urllib.request.Request(
            "https://api.elevenlabs.io/v1/music?output_format=" + CFG["output_format"],
            data=json.dumps(body).encode(), method="POST",
            headers={"xi-api-key": api_key, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                data = r.read()
                response_meta = {k: r.headers.get(k) for k in ("song-id", "request-id", "character-cost")
                                 if r.headers.get(k) is not None}
        except urllib.error.HTTPError as e:
            raise SystemExit(f"ElevenLabs music HTTP {e.code}: {e.read().decode(errors='replace')[:400]}")
        # No automatic retries on timeouts: a request may have been billed.
        temporary = path.with_suffix(".partial.mp3")
        temporary.write_bytes(data)
        info = probe(temporary)
        if abs(info["duration_s"] - ch["length_ms"] / 1000) > 1:
            raise SystemExit(f"Unexpected track duration for {path.name}: {info['duration_s']}")
        temporary.replace(path)
        after = subscription(api_key)
        manifest["tracks"][str(ch["chapter"])] = {
            "file": str(path.relative_to(ROOT)), "request": body, "request_sha256": fingerprint,
            "audio_sha256": hashlib.sha256(data).hexdigest(), **info, "response": response_meta,
            "generated_utc": datetime.now(timezone.utc).isoformat(), "subscription_after": after}
        run["latest_after"] = after
        run["observed_credit_delta"] = after["character_count"] - before["character_count"]
        MANIFEST.write_text(json.dumps(manifest, indent=2))
        print("Saved:", path.name, "observed session credits:", run["observed_credit_delta"], flush=True)
    run["completed_utc"] = datetime.now(timezone.utc).isoformat()
    run["after"] = subscription(api_key)
    run["observed_credit_delta"] = run["after"]["character_count"] - before["character_count"]
    MANIFEST.write_text(json.dumps(manifest, indent=2))
    print("Music generation complete:", json.dumps(run["after"]), flush=True)


if __name__ == "__main__":
    main()
