"""Mix cached chapter music under the existing film without rendering animation.

.venv/bin/python tools/mix_music.py
Outputs renders/final_with_music.mp4, a matching SRT, music stem and QA report.
The original final.mp4 and final.srt remain available. No API calls are made here.
"""
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy import signal

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "config/music.json").read_text())
MIX = CFG["mix"]
SR = MIX["sample_rate"]
SOURCE = ROOT / "renders/final.mp4"
OUTPUT = ROOT / "renders/final_with_music.mp4"
QA = ROOT / "renders/qa/music"
BLOCK = int(SR * 0.02)


def run(args):
    return subprocess.run(args, check=True, capture_output=True, text=True)


def probe(path):
    return json.loads(run(["ffprobe", "-v", "error", "-show_entries",
                          "format=duration,size:stream=codec_type,codec_name,width,height,sample_rate,channels,start_time,duration,nb_frames",
                          "-of", "json", str(path)]).stdout)


def decode(path, destination):
    run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", str(path), "-vn", "-ar", str(SR),
         "-af", f"aresample={SR}:async=1:first_pts=0:min_hard_comp=0.000001:min_comp=0.000001",
         "-ac", "2", "-c:a", "pcm_f32le", str(destination)])
    data, rate = sf.read(destination, dtype="float32", always_2d=True)
    assert rate == SR
    return data


def block_levels(data):
    """Stereo RMS every 20 ms; small working slices avoid full-film temporary arrays."""
    n = len(data) // BLOCK
    levels = np.empty(n, dtype=np.float32)
    for start in range(0, n, 500):
        end = min(n, start + 500)
        chunk = data[start * BLOCK:end * BLOCK].reshape(end - start, BLOCK, 2)
        levels[start:end] = np.sqrt(np.mean(chunk * chunk, axis=(1, 2)))
    return levels


def db(values):
    return 20 * np.log10(np.maximum(values, 1e-12))


def trim_track(track):
    levels = block_levels(track)
    threshold = max(float(np.max(levels)) * 0.01, 1e-5)
    active = np.flatnonzero(levels > threshold)
    if not len(active):
        raise RuntimeError("Generated music contains no usable signal")
    start = max(0, (int(active[0]) - 2) * BLOCK)
    end = min(len(track), (int(active[-1]) + 3) * BLOCK)
    return track[start:end], {"trim_start_s": start / SR, "trim_end_s": end / SR}


def extend_track(track, length):
    """Linear overlap fades keep repeated ambient textures from making a volume bump."""
    overlap = min(int(MIX["loop_crossfade_s"] * SR), len(track) // 8)
    result = np.zeros((length, 2), dtype=np.float32)
    result[:min(length, len(track))] = track[:length]
    end = min(length, len(track))
    ramp = np.linspace(0, 1, overlap, dtype=np.float32)[:, None]
    while end < length:
        start = end - overlap
        count = min(len(track), length - start)
        result[start:end] = result[start:end] * (1 - ramp) + track[:overlap] * ramp
        result[end:start + count] = track[overlap:count]
        end = start + count
    return result


def loudness(path):
    p = run(["ffmpeg", "-nostdin", "-hide_banner", "-nostats", "-i", str(path), "-vn", "-af",
             f"loudnorm=I={MIX['target_lufs']}:TP={MIX['true_peak_db']}:LRA=11:print_format=json",
             "-f", "null", "-"])
    match = re.search(r'\{[^{}]*"input_i"[^{}]*\}', p.stderr, re.S)
    if not match:
        raise RuntimeError("FFmpeg returned no loudness measurement")
    return json.loads(match.group(0))


def video_fingerprint(path, destination):
    run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", str(path), "-map", "0:v:0", "-c", "copy",
         "-f", "framehash", "-hash", "sha256", str(destination)])
    rows = [x for x in destination.read_text().splitlines() if x and not x.startswith("#")]
    # Includes every packet's timestamps, duration, size and hash.
    return rows


def audio_sample(path, start):
    data = subprocess.check_output([
        "ffmpeg", "-nostdin", "-v", "error", "-ss", str(start), "-i", str(path),
        "-t", "5", "-vn", "-ar", str(SR),
        "-af", f"aresample={SR}:async=1:first_pts=0:min_hard_comp=0.000001:min_comp=0.000001",
        "-ac", "1", "-f", "f32le", "-"])
    return np.frombuffer(data, dtype=np.float32)


def compare_audio(a, b):
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    correlation = signal.correlate(b, a, mode="full", method="fft")
    center, width = n - 1, SR
    lag = int(np.argmax(correlation[center - width:center + width + 1])) - width
    gain = float(np.dot(a.astype(np.float64), b.astype(np.float64)) /
                 np.dot(a.astype(np.float64), a.astype(np.float64)))
    return {"lag_samples": lag, "lag_ms": lag * 1000 / SR,
            "gain_db": float(20 * np.log10(abs(gain))),
            "correlation": float(np.corrcoef(a, b)[0, 1])}


def check_decoded_timing(voice):
    results = []
    for start in (30, 270, 700, 1200, 1650, 1890, 2070, 2250):
        a = audio_sample(SOURCE, start)
        b = np.mean(voice[round(start * SR):round((start + 5) * SR)], axis=1)
        result = {"at_s": start, **compare_audio(a, b)}
        results.append(result)
        if abs(result["lag_ms"]) > 1 or result["correlation"] < 0.99:
            raise RuntimeError(f"Decoded narration did not preserve source timestamps: {result}")
    return results


def main():
    QA.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((ROOT / "audio/music/manifest.json").read_text())
    offsets = json.loads((ROOT / "renders/scene_offsets.json").read_text())
    chapter_starts = {int(s[1]): t for s, t in reversed(offsets) if s != "Credits"}
    report = {"source": str(SOURCE.relative_to(ROOT)), "output": str(OUTPUT.relative_to(ROOT)),
              "config": CFG, "chapters": [], "sound_effects": False, "validation_status": "in_progress"}
    source_subtitles = ROOT / "renders/final.srt"
    report["subtitles_sha256"] = hashlib.sha256(source_subtitles.read_bytes()).hexdigest()
    with tempfile.TemporaryDirectory(prefix="music_mix_") as directory:
        tmp = Path(directory)
        print("Decoding the existing narration", flush=True)
        voice = decode(SOURCE, tmp / "voice.wav")
        report["decoded_narration_timing"] = check_decoded_timing(voice)
        # Match the decoded sample timeline, including AAC padding; do not move or stretch narration.
        n = len(voice)
        duration = n / SR
        source_levels = block_levels(voice)
        active = source_levels > 10 ** (-35 / 20)
        if not np.any(active):
            raise RuntimeError("No narration detected in the source")
        voice_reference_db = float(np.median(db(source_levels[active])))
        music_reference_db = voice_reference_db - MIX["voice_to_music_db"]
        report.update({"decoded_duration_s": duration, "voice_reference_rms_dbfs": voice_reference_db,
                       "music_reference_rms_dbfs": music_reference_db})
        bed = np.zeros_like(voice)
        half_fade = int(SR * MIX["chapter_crossfade_s"] / 2)
        for ch in CFG["chapters"]:
            c = ch["chapter"]
            start = round(chapter_starts[c] * SR)
            stop = round(chapter_starts[c + 1] * SR) if c < 8 else n
            a, b = max(0, start - half_fade), min(n, stop + half_fade)
            item = manifest["tracks"][str(c)]
            path = ROOT / item["file"]
            if hashlib.sha256(path.read_bytes()).hexdigest() != item["audio_sha256"]:
                raise RuntimeError(f"Music source changed: {path.name}")
            track, trim = trim_track(decode(path, tmp / "track.wav"))
            track_rms = float(np.sqrt(np.mean(track * track)))
            target_db = music_reference_db + ch["level_db"]
            track *= 10 ** (target_db / 20) / track_rms
            extended = extend_track(track, b - a)
            if c > 0:
                fade_len = min(2 * half_fade, len(extended))
                extended[:fade_len] *= np.linspace(0, 1, fade_len, dtype=np.float32)[:, None]
            if c < 8:
                fade_len = min(2 * half_fade, len(extended))
                extended[-fade_len:] *= np.linspace(1, 0, fade_len, dtype=np.float32)[:, None]
            bed[a:b] += extended
            report["chapters"].append({"chapter": c, "name": ch["name"], "start_s": start / SR,
                                       "end_s": stop / SR, "track": item["file"], "level_db": ch["level_db"],
                                       "target_rms_dbfs": target_db, **trim})
            print("Chapter bed:", c, ch["name"], flush=True)
            del extended, track

        # A speech-driven envelope ducks gently and anticipates words by 60 ms.
        detected = source_levels > 10 ** (max(-42, voice_reference_db - 19) / 20)
        ahead = round(MIX["anticipation_s"] / 0.02)
        target = detected.astype(np.float32)
        for shift in range(1, ahead + 1):
            target[:-shift] = np.maximum(target[:-shift], detected[shift:])
        activity = np.empty_like(target)
        value = 0.0
        attack = np.exp(-0.02 / MIX["duck_attack_s"])
        release = np.exp(-0.02 / MIX["duck_release_s"])
        for i, wanted in enumerate(target):
            coefficient = attack if wanted > value else release
            value = coefficient * value + (1 - coefficient) * wanted
            activity[i] = value
        gains = 10 ** (MIX["pause_lift_db"] * (1 - activity) / 20)
        for first in range(0, n, SR * 10):
            last = min(n, first + SR * 10)
            points = np.arange(first, last, dtype=np.float64) / BLOCK
            gain = np.interp(points, np.arange(len(gains)), gains).astype(np.float32)
            bed[first:last] *= gain[:, None]
        fade_in = round(SR * MIX["intro_fade_s"])
        fade_out = round(SR * MIX["outro_fade_s"])
        bed[:fade_in] *= np.linspace(0, 1, fade_in, dtype=np.float32)[:, None]
        bed[-fade_out:] *= np.linspace(1, 0, fade_out, dtype=np.float32)[:, None]
        music_levels = block_levels(bed)
        for ch in report["chapters"]:
            a, b = round(ch["start_s"] / 0.02), min(len(source_levels), round(ch["end_s"] / 0.02))
            mask = active[a:b] & (music_levels[a:b] > 1e-7)
            differences = db(source_levels[a:b][mask]) - db(music_levels[a:b][mask])
            ch["voice_above_music_db"] = {
                "p10": float(np.percentile(differences, 10)), "median": float(np.median(differences)),
                "p90": float(np.percentile(differences, 90))}
        report["pause_lift_observed_max_db"] = float(np.max(db(gains)))
        stem = ROOT / "audio/music/bed_ducked.wav"
        sf.write(stem, bed, SR, subtype="PCM_24")
        raw = tmp / "mixed.wav"
        print("Writing the mix and measuring loudness", flush=True)
        with sf.SoundFile(raw, "w", samplerate=SR, channels=2, subtype="FLOAT") as out:
            for a in range(0, n, SR * 10):
                b = min(n, a + SR * 10)
                out.write(voice[a:b] + bed[a:b])
        del voice, bed
        measurement = loudness(raw)
        report["mix_before_normalization"] = measurement
        af = (f"loudnorm=I={MIX['target_lufs']}:TP={MIX['true_peak_db']}:LRA=11:"
              f"measured_I={measurement['input_i']}:measured_TP={measurement['input_tp']}:"
              f"measured_LRA={measurement['input_lra']}:measured_thresh={measurement['input_thresh']}:"
              f"offset={measurement['target_offset']}:linear=true:print_format=json")
        print("Normalizing and copying the video stream", flush=True)
        encoded = run(["ffmpeg", "-nostdin", "-y", "-hide_banner", "-nostats", "-i", str(SOURCE),
                       "-i", str(raw), "-map", "0:v:0", "-map", "1:a:0", "-map_metadata", "0",
                       "-c:v", "copy", "-af", af, "-ar", str(SR), "-c:a", "aac", "-b:a", "192k",
                       "-movflags", "+faststart", str(OUTPUT)])
        report["normalization"] = json.loads(re.search(r'\{[^{}]*"input_i"[^{}]*\}', encoded.stderr, re.S).group(0))
        report["output_probe"] = probe(OUTPUT)
        report["source_probe"] = probe(SOURCE)
        report["duration_difference_s"] = (float(report["output_probe"]["format"]["duration"]) -
                                           float(report["source_probe"]["format"]["duration"]))
        if abs(report["duration_difference_s"]) > 0.05:
            raise RuntimeError("The audio remix changed the film duration")
        print("Checking the encoded loudness and video packet identity", flush=True)
        report["encoded_loudness"] = loudness(OUTPUT)
        (QA / "mix_report.json").write_text(json.dumps(report, indent=2))
        print("Encoded loudness:", json.dumps(report["encoded_loudness"]), flush=True)
        sync = []
        for start in (30, 270, 700, 1200, 1650, 1890, 2070, 2250):
            result = {"at_s": start, **compare_audio(audio_sample(SOURCE, start), audio_sample(OUTPUT, start))}
            sync.append(result)
            if abs(result["lag_ms"]) > 1 or abs(result["gain_db"]) > 0.5 or result["correlation"] < 0.98:
                raise RuntimeError(f"Encoded narration timing or level changed: {result}")
        report["encoded_narration_sync"] = sync
        (QA / "narration_sync.json").write_text(json.dumps(sync, indent=2))
        before_packets = video_fingerprint(SOURCE, QA / "source_video.framehash")
        after_packets = video_fingerprint(OUTPUT, QA / "output_video.framehash")
        report["video_packets_identical_including_timestamps"] = before_packets == after_packets
        if before_packets != after_packets:
            raise RuntimeError("Video packets or timestamps changed during remux")
        if abs(float(report["encoded_loudness"]["input_i"]) - MIX["target_lufs"]) > 0.3:
            raise RuntimeError("The encoded mix missed its loudness target")
        if float(report["encoded_loudness"]["input_tp"]) > -1.4:
            raise RuntimeError("The encoded true peak needs additional headroom: " +
                               report["encoded_loudness"]["input_tp"] + " dBTP")
        output_subtitles = OUTPUT.with_suffix(".srt")
        shutil.copyfile(source_subtitles, output_subtitles)
        report["subtitles_unchanged"] = hashlib.sha256(output_subtitles.read_bytes()).hexdigest() == report["subtitles_sha256"]
        for name, start, length in (("opening", 0, 45), ("colouring", chapter_starts[1], 45),
                                    ("proof", chapter_starts[5], 45), ("verification", chapter_starts[7], 45),
                                    ("ending", duration - 45, 45)):
            run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-ss", str(start), "-i", str(OUTPUT),
                 "-t", str(length), "-vn", "-c:a", "libmp3lame", "-b:a", "192k", str(QA / f"{name}.mp3")])
        report["validation_status"] = "passed"
        (QA / "mix_report.json").write_text(json.dumps(report, indent=2))
        print("Complete:", OUTPUT, flush=True)
        print("Encoded loudness:", json.dumps(report["encoded_loudness"]), flush=True)


if __name__ == "__main__":
    main()
