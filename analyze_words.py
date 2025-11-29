# analyze_words.py
import json
import os
import librosa
import numpy as np
import parselmouth
from statistics import mean, stdev

AUDIO_PATH = "input.wav"
WORDS_JSON = "words.json"
OUT_JSON = "analysis_output.json"

# --- helpers ---
def load_audio(path, sr=16000):
    y, orig_sr = librosa.load(path, sr=sr, mono=True)
    return y, sr

def extract_segment_array(y, sr, start_s, end_s, pad_ms=30):
    pad = int((pad_ms/1000.0)*sr)
    s = max(0, int(start_s*sr) - pad)
    e = min(len(y), int(end_s*sr) + pad)
    return y[s:e]

def rms_energy(arr):
    return float(np.sqrt(np.mean(np.square(arr) + 1e-12)))

def parselmouth_measures(seg_array, sr):
    # return f0_median, jitter, shimmer, hnr
    try:
        snd = parselmouth.Sound(seg_array, sampling_frequency=sr)
        pitch = snd.to_pitch()
        f0_vals = pitch.selected_array['frequency']
        f0_vals = f0_vals[f0_vals > 0]
        f0_med = float(np.median(f0_vals)) if len(f0_vals) else 0.0

        # jitter, shimmer, HNR via Praat (may fail on very short segments)
        try:
            point_process = parselmouth.praat.call(snd, "To PointProcess (periodic, cc)", 75, 500)
            jitter_local = parselmouth.praat.call(point_process, "Get jitter (local)", 0.0001, 0.02, 1.3)
            shimmer_local = parselmouth.praat.call([snd, point_process], "Get shimmer (local)", 0.0001, 0.02, 1.3, 1.6)
            harmonicity = parselmouth.praat.call(snd, "To Harmonicity (cc)", 0.01, 75, 0.1)
            hnr_val = parselmouth.praat.call(harmonicity, "Get mean", 0, 0)
        except Exception:
            jitter_local = 0.0
            shimmer_local = 0.0
            hnr_val = 0.0

        return {"f0_median": f0_med, "jitter": float(jitter_local), "shimmer": float(shimmer_local), "hnr": float(hnr_val)}
    except Exception:
        return {"f0_median": 0.0, "jitter": 0.0, "shimmer": 0.0, "hnr": 0.0}

# --- load words.json ---
if not os.path.exists(WORDS_JSON):
    print(f"Error: {WORDS_JSON} not found. Run get_words.py first.")
    raise SystemExit(1)

with open(WORDS_JSON, "r", encoding="utf-8") as f:
    word_segments = json.load(f)

# --- load audio ---
if not os.path.exists(AUDIO_PATH):
    print(f"Error: {AUDIO_PATH} not found. Place your audio file in the project folder.")
    raise SystemExit(1)

y, sr = load_audio(AUDIO_PATH, sr=16000)

# --- compute global stats for z-scoring ---
energies = []
pitches = []
durations = []
for w in word_segments:
    start = w.get("start", 0.0)
    end = w.get("end", start + 0.05)
    seg = extract_segment_array(y, sr, start, end)
    energies.append(rms_energy(seg))
    durations.append(max(0.0001, end - start))
    pm = parselmouth_measures(seg, sr)
    pitches.append(pm["f0_median"] if pm["f0_median"] > 0 else 0.0)

e_mean = mean(energies) if energies else 0.0
e_std = stdev(energies) if len(energies) > 1 else (e_mean + 1e-6)
p_mean = mean(pitches) if pitches else 0.0
p_std = stdev(pitches) if len(pitches) > 1 else (p_mean + 1e-6)
d_mean = mean(durations) if durations else 0.0

def clamp01(x): return float(max(0.0, min(1.0, x)))

output = []
for i, w in enumerate(word_segments):
    word = w.get("word", "").strip()
    start = float(w.get("start", 0.0))
    end = float(w.get("end", start + 0.05))
    duration = max(0.0001, end - start)
    seg = extract_segment_array(y, sr, start, end)

    energy = rms_energy(seg)
    pm = parselmouth_measures(seg, sr)
    f0 = pm["f0_median"]
    jitter = pm["jitter"]
    shimmer = pm["shimmer"]
    hnr = pm["hnr"]

    # pause before (fluency)
    pause_before = 0.0
    if i > 0:
        prev_end = float(word_segments[i-1].get("end", 0.0))
        pause_before = max(0.0, start - prev_end)

    # Pronunciation proxy: if whisperx provides "confidence" use it; otherwise default 0.85
    pron_conf = w.get("confidence", w.get("probability", None))
    if pron_conf is None:
        pron_score = 0.85 if energy > 1e-5 else 0.6
    else:
        try:
            pron_score = float(pron_conf)
            if pron_score < 0 and pron_score > -50:
                pron_score = clamp01(1.0 + pron_score/50.0)
            else:
                pron_score = clamp01(pron_score)
        except Exception:
            pron_score = 0.85

    # Fluency: penalize long pauses > 0.5s
    fluency_score = clamp01(1.0 - min(1.0, pause_before / 0.5))

    # Tension: heuristic from jitter & shimmer (scaled)
    tension_raw = (jitter * 100.0) * 0.7 + (shimmer * 100.0) * 0.3
    tension_score = clamp01(tension_raw / 10.0)

    # Breathiness: lower HNR -> more breathy
    breathiness_score = clamp01(1.0 - (hnr / (hnr + 30.0)))

    # Emphasis: combination of energy and pitch z-scores
    energy_z = (energy - e_mean) / (e_std if e_std>0 else 1.0)
    pitch_z = (f0 - p_mean) / (p_std if p_std>0 else 1.0)
    emphasis_score = float((energy_z + pitch_z) / 2.0)

    output.append({
        "word": word,
        "start": round(start, 3),
        "end": round(end, 3),
        "duration": round(duration, 3),
        "energy": round(energy, 8),
        "f0_median": round(f0, 2),
        "jitter": round(jitter, 6),
        "shimmer": round(shimmer, 6),
        "hnr": round(hnr, 3),
        "pause_before": round(pause_before, 3),
        "pronunciation_score": round(pron_score, 3),
        "fluency_score": round(fluency_score, 3),
        "tension_score": round(tension_score, 3),
        "breathiness_score": round(breathiness_score, 3),
        "emphasis_score": round(emphasis_score, 3)
    })

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump({"audio_file": AUDIO_PATH, "word_analysis": output}, f, indent=2, ensure_ascii=False)

print(f"Saved analysis to {OUT_JSON}")
