# Word-by-Word Speech Analysis System

This project takes an input audio file and performs detailed **word-level speech analysis**, including:

- ⏱ **Word timestamps** (start/end)
- 🔊 **Energy (loudness)**
- 🎤 **Pitch (F0)**
- 🗣 **Pronunciation score**
- 📈 **Fluency score**
- ⚡ **Tension score (jitter/shimmer)**
- 🌬 **Breathiness score (HNR)**
- 🎯 **Word emphasis score**

Generated using **Whisper + WhisperX + Librosa + Praat-Parselmouth**.


## 🚀 How It Works

### **1. Generate Word Timestamps**
python get_words.py

Produces:
- `words.json`


### **2. Analyze Each Word (Pitch, Energy, HNR, Jitter, Shimmer)**
python analyze_words.py
Produces:
- `analysis_output.json`



### **3. Generate HTML Report**
python generate_report.py

Produces:
- `report.html` (open in browser)


## 📂 Project Structure

audio-system/
│
├── input.wav
├── get_words.py
├── analyze_words.py
├── generate_report.py
├── words.json
├── analysis_output.json
├── report.html
└── README.md


## 📘 Output Files

### **words.json**
Contains all word timestamps from WhisperX alignment.

### **analysis_output.json**
Contains detailed acoustic features + scores per word.

### **report.html**
A clean, readable report showing all word metrics.


## 🙌 Credits
- OpenAI Whisper  
- WhisperX Alignment  
- Librosa  
- Parselmouth (Praat)  
- Ashish Raj (Developer)

