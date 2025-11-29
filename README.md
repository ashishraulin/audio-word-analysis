🎙️ Audio Word-Level Pronunciation & Speech Analysis

Word-by-word pronunciation, fluency, emphasis, tension & breathiness analysis using Whisper + WhisperX + Python.

This project analyzes an audio file at a per-word level.
It generates timestamps, duration, word emphasis, vocal tension, breathiness, fluency, pitch (F0), energy, and pronunciation scores using Deep Learning models.

🔥 Key Features

✔️ Accurate transcription using OpenAI Whisper

✔️ Word-level alignment using WhisperX

✔️ Extracts:

Pronunciation score

Fluency score

Emphasis score

Breathiness & tension

Pitch (F0)

Energy

Pause before each word

✔️ Saves all analysis in analysis_output.json

✔️ Auto-generates a beautiful report.html

✔️ Fully local — no API required

✔️ Works on Windows (CPU-only)

📂 Project Structure
audio-word-analysis/
│── analysis_output.json      # Complete analysis output  
│── analyze_words.py          # Extract speech features  
│── generate_report.py        # Creates report.html  
│── get_words.py              # Whisper + WhisperX transcription  
│── input.wav                 # Your audio sample  
│── plot_waveform.py          # Optional waveform plot  
│── report.html               # Final interactive report  
│── words.json                # Word timestamps  
│── venv/                     # Virtual environment  
└── README.md                 # This file  

🚀 Installation
1️⃣ Clone the repo
git clone https://github.com/ashishraulin/audio-word-analysis.git
cd audio-word-analysis

2️⃣ Create a virtual environment
python -m venv venv
venv\Scripts\Activate.ps1

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Add FFmpeg to PATH

Required for Whisper audio decoding.

🧠 How It Works
● Step 1 — Transcribe & Align Words
python get_words.py


Output → words.json

● Step 2 — Analyze Speech Features
python analyze_words.py


Output → analysis_output.json

● Step 3 — Generate Final Report
python generate_report.py


Opens → report.html (beautiful visual summary)

📊 Example Output

Each word contains:

{
  "word": "Hello",
  "start": 0.0,
  "end": 0.40,
  "duration": 0.40,
  "pronunciation_score": 0.85,
  "fluency_score": 1.0,
  "emphasis_score": -0.12,
  "tension_score": 0.02,
  "breathiness_score": 0.91,
  "energy": 0.104,
  "f0_median": 132.5
}

🌟 Why This Project Is Useful

This tool can be used for:

🧑‍🏫 English learning apps

🗣️ Speech therapy

🎙️ Voice-training analysis

📚 Language research

🤖 AI-based speaking evaluation systems

🤝 Contributing

Pull requests are welcome!
For major changes, open an issue first.

📜 License

MIT License — free to use & modify.
