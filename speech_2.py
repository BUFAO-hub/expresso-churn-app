import streamlit as st
import speech_recognition as sr

# -----------------------------
# Transcription Function
# -----------------------------
def transcribe_speech(api_choice, language):
    recognizer = sr.Recognizer()
    st.info("Please upload or record audio")

    audio_file = st.file_uploader("Upload audio", type=["wav", "mp3", "m4a"])
    if audio_file is not None:
        with sr.AudioFile(audio_file) as source:
            st.write("🎙️ Processing audio...")
            audio_data = recognizer.record(source)

        try:
            if api_choice == "Google":
                return recognizer.recognize_google(audio_data, language=language)
            elif api_choice == "Sphinx":
                return recognizer.recognize_sphinx(audio_data, language=language)
            else:
                return "API not yet implemented."
        except sr.UnknownValueError:
            return "⚠️ Could not understand the audio."
        except sr.RequestError as e:
            return f"⚠️ API unavailable: {e}"
        except Exception as e:
            return f"⚠️ Unexpected error: {e}"
    return None

# -----------------------------
# Streamlit App
# -----------------------------
st.title("🗣️ Advanced Speech Recognition App")

# API Choice
api_choice = st.selectbox("Choose API:", ["Google", "Sphinx"])

# Language Choice
language = st.selectbox("Choose Language:", ["en-US", "fr-FR", "es-ES", "de-DE"])

# Transcribe Button
if st.button("Transcribe Speech"):
    transcript = transcribe_speech(api_choice, language)
    if transcript:
        st.success(f"**Transcript:** {transcript}")
        # Save option
        st.download_button("Download Transcript", transcript, file_name="transcript.txt")

# (Optional) Simulated Pause/Resume
if st.checkbox("Enable Pause/Resume Simulation"):
    st.write("🔄 Record audio in parts and transcribe separately, then combine results.")
