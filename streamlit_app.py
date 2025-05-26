import streamlit as st
import whisper
import tempfile
import os

st.set_page_config(page_title="Whisper Transcribe", layout="centered")

st.title("🎙️ Transkripsi Audio dengan Whisper")

# Pilihan model
model_options = ["tiny", "base", "small", "medium", "large"]
model_choice = st.selectbox("Pilih model Whisper", model_options, index=2)  # default: small

# Load model sekali saja
@st.cache_resource
def load_model(name):
    return whisper.load_model(name)

model = load_model(model_choice)

uploaded_file = st.file_uploader("Upload file audio", type=["mp3", "wav", "m4a", "mp4"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/mp3")

    with st.spinner("🔍 Sedang mentranskripsi..."):
        # Simpan ke file sementara
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        # Transkripsi
        result = model.transcribe(tmp_path)

        # Hapus file sementara
        os.remove(tmp_path)

        st.subheader("📄 Hasil Transkripsi:")
        st.write(result["text"])