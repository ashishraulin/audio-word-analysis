import whisper
import whisperx
import torch

AUDIO_PATH = "input.wav"

# Load whisper model
model = whisper.load_model("small")

print("Transcribing audio...")
result = model.transcribe(AUDIO_PATH)

# Load alignment model
device = "cpu"
language = result["language"]

print("Loading WhisperX aligner...")
model_a, metadata = whisperx.load_align_model(language_code=language, device=device)

# Align
print("Aligning words...")
aligned = whisperx.align(result["segments"], model_a, metadata, AUDIO_PATH, device=device)

# Print word segments
for w in aligned["word_segments"]:
    print(f"{w['word']} --> start: {w['start']}, end: {w['end']}")

# Save full result
import json
with open("words.json", "w") as f:
    json.dump(aligned["word_segments"], f, indent=2)

print("\nSaved word timestamps to words.json")
