# plot_waveform.py
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
import os

AUDIO_PATH = "input.wav"   # put your file here

if not os.path.exists(AUDIO_PATH):
    print(f"Error: {AUDIO_PATH} not found. Place your WAV file in the project folder.")
    raise SystemExit(1)

# load audio (librosa will resample to sr if you set it; leave sr=None to preserve original)
y, sr = librosa.load(AUDIO_PATH, sr=None, mono=True)  # sr=None keeps original sample rate
duration = len(y) / sr

print(f"Loaded: {AUDIO_PATH}")
print(f"Sample rate: {sr} Hz")
print(f"Duration: {duration:.2f} seconds")
print(f"Samples: {len(y)}")

# compute RMS energy (short-term)
frame_length = 2048
hop_length = 512
rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
times_rms = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop_length, n_fft=frame_length)

# plot waveform + rms
plt.figure(figsize=(10, 4))
librosa.display.waveshow(y, sr=sr, alpha=0.6)
plt.plot(times_rms, rms * np.max(np.abs(y)), color='r', label='RMS (scaled)')
plt.title("Waveform and RMS Energy")
plt.xlabel("Time (s)")
plt.legend()
plt.tight_layout()

out_png = "waveform.png"
plt.savefig(out_png)
print(f"Saved waveform image to {out_png}")
plt.show()
