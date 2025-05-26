import streamlit as st
import whisper
import tempfile
import os
import json

st.set_page_config(page_title="Whisper Transcribe", layout="centered")

st.title("🎙️ Transkripsi Audio dengan Whisper")

model_options = ["tiny", "base", "small", "medium", "large"]
model_choice = st.selectbox("Pilih model Whisper", model_options, index=2)  # default small

@st.cache_resource
def load_model(name):
    return whisper.load_model(name)

model = load_model(model_choice)

uploaded_file = st.file_uploader("Upload file audio", type=["mp3", "wav", "m4a", "mp4"])

def write_srt(segments, file):
    def format_timestamp(seconds):
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds - int(seconds)) * 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    with open(file, "w", encoding="utf-8") as srt:
        for i, seg in enumerate(segments, start=1):
            start = format_timestamp(seg["start"])
            end = format_timestamp(seg["end"])
            text = seg["text"].strip()
            srt.write(f"{i}\n{start} --> {end}\n{text}\n\n")

def write_vtt(segments, file):
    def format_timestamp(seconds):
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds - int(seconds)) * 1000)
        return f"{h:02}:{m:02}:{s:02}.{ms:03}"

    with open(file, "w", encoding="utf-8") as vtt:
        vtt.write("WEBVTT\n\n")
        for i, seg in enumerate(segments, start=1):
            start = format_timestamp(seg["start"])
            end = format_timestamp(seg["end"])
            text = seg["text"].strip()
            vtt.write(f"{i}\n{start} --> {end}\n{text}\n\n")

def write_txt(segments, file):
    with open(file, "w", encoding="utf-8") as txt:
        for seg in segments:
            txt.write(seg["text"].strip() + "\n")

def write_segments_json(segments, file):
    with open(file, "w", encoding="utf-8") as js:
        json.dump(segments, js, indent=2, ensure_ascii=False)

if uploaded_file is not None:
    # Simpan file audio sekali
    if "audio_path" not in st.session_state:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_audio:
            tmp_audio.write(uploaded_file.read())
            st.session_state.audio_path = tmp_audio.name

    # Jalankan transcribe hanya sekali
    if "transcription_result" not in st.session_state:
        with st.spinner("🔍 Sedang mentranskripsi..."):
            st.session_state.transcription_result = model.transcribe(st.session_state.audio_path)

        segments = st.session_state.transcription_result["segments"]

        # Buat temporary directory untuk simpan hasil file output
        if "tmp_output_dir" not in st.session_state:
            st.session_state.tmp_output_dir = tempfile.TemporaryDirectory()

        txt_path = os.path.join(st.session_state.tmp_output_dir.name, "transcription.txt")
        srt_path = os.path.join(st.session_state.tmp_output_dir.name, "transcription.srt")
        vtt_path = os.path.join(st.session_state.tmp_output_dir.name, "transcription.vtt")
        json_path = os.path.join(st.session_state.tmp_output_dir.name, "transcription.json")

        write_txt(segments, txt_path)
        write_srt(segments, srt_path)
        write_vtt(segments, vtt_path)
        write_segments_json(segments, json_path)

        st.session_state.files = {
            "transcription.txt": txt_path,
            "transcription.srt": srt_path,
            "transcription.vtt": vtt_path,
            "transcription.json": json_path,
        }

    # Tampilkan audio
    st.audio(st.session_state.audio_path)

    # Tampilkan hasil text
    st.subheader("📄 Hasil Transkripsi (Text):")
    st.write(st.session_state.transcription_result["text"])

    # Tombol download file
    st.subheader("⬇️ Download File Output:")
    for name, path in st.session_state.files.items():
        with open(path, "rb") as f:
            st.download_button(
                label=f"Download {name}",
                data=f,
                file_name=name,
                mime="text/plain"
            )
