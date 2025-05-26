# 🎙️ Whisper Transcribe App

A simple web app to transcribe audio files using OpenAI's Whisper model, built with Streamlit.

![whisper-transcribe-banner](https://img.shields.io/badge/Whisper-Transcription-blue) ![streamlit-badge](https://img.shields.io/badge/Built%20with-Streamlit-orange)

---

## 🚀 Features

- 🎧 Upload and play audio (`.mp3`, `.wav`, `.m4a`, `.mp4`)
- 🧠 Transcribe using Whisper model (`tiny`, `base`, `small`, `medium`, `large`)
- 📝 Display transcribed text directly in the app
- 💾 Runs locally or on Streamlit Cloud

---

## 📦 Requirements

Install dependencies with pip:

```bash
pip install -r requirements.txt
```

If you haven't already, make sure `ffmpeg` is available in your system.

For Linux (Debian/Ubuntu):

```bash
sudo apt-get install ffmpeg
```

---

## 📂 File Structure

```
whisper-transcribe-app/
├── app.py               # Streamlit app source code
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## ▶️ How to Run

### 🔹 Local Machine

```bash
streamlit run app.py
```

### 🔹 Streamlit Cloud

1. Push this repo to your GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Deploy new app from your GitHub repo
4. (Optional) Create `packages.txt` with:

```
ffmpeg
```

to ensure `ffmpeg` is available on the cloud platform.

---

## 🧠 Whisper Model Options

The app supports these model sizes (sorted from lightest to heaviest):

- `tiny` (~39 MB)
- `base` (~74 MB)
- `small` (~244 MB) **(default)**
- `medium` (~769 MB)
- `large` (~1.55 GB)

Choose based on your accuracy/speed/memory preferences.

---

## 📜 License

MIT License

---

## 💬 Acknowledgements

- [OpenAI Whisper](https://github.com/openai/whisper)
- [Streamlit](https://streamlit.io)