print("Testing installations...\n")

try:
    import torch
    print("✓ torch installed")
except:
    print("✗ torch NOT installed")

try:
    import whisper
    print("✓ whisper installed")
except:
    print("✗ whisper NOT installed")

try:
    import librosa
    print("✓ librosa installed")
except:
    print("✗ librosa NOT installed")

try:
    import numpy
    print("✓ numpy installed")
except:
    print("✗ numpy NOT installed")

try:
    import scipy
    print("✓ scipy installed")
except:
    print("✗ scipy NOT installed")

try:
    import soundfile
    print("✓ soundfile installed")
except:
    print("✗ soundfile NOT installed")

try:
    import parselmouth
    print("✓ praat-parselmouth installed")
except:
    print("✗ praat-parselmouth NOT installed")

try:
    import whisperx
    print("✓ whisperx installed")
except:
    print("✗ whisperx NOT installed")

print("\nDone testing!")
