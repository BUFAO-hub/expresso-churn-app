import streamlit as st
import nltk
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import random

# ---------------------------
# Step 1: Load and preprocess chatbot data
# ---------------------------
nltk.download("punkt")

responses = {
    "hello": ["Hi there!", "Hello!", "Hey! How can I help you?"],
    "how are you": ["I'm doing great, thanks for asking!", "All good here. How about you?"],
    "bye": ["Goodbye!", "See you later!", "Take care!"],
}

def preprocess(text):
    return text.lower()

def chatbot_response(user_input):
    user_input = preprocess(user_input)
    for key in responses.keys():
        if key in user_input:
            return random.choice(responses[key])
    return "Sorry, I didn’t understand that."

# ---------------------------
# Step 2: Record audio without PyAudio
# ---------------------------
def record_audio(duration=5, fs=44100):
    st.write("🎤 Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    return np.squeeze(recording)

def speech_to_text():
    recognizer = sr.Recognizer()
    audio_data = record_audio()
    audio = sr.AudioData(audio_data.tobytes(), 44100, 2)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError:
        return "API unavailable."

# ---------------------------
# Step 3: Streamlit App
# ---------------------------
st.title("🗣️ Speech-Enabled Chatbot (No PyAudio)")

mode = st.radio("Choose input mode:", ("Text", "Speech"))

if mode == "Text":
    user_input = st.text_input("Type your message here:")
    if st.button("Send"):
        if user_input:
            bot_response = chatbot_response(user_input)
            st.write(f"**You:** {user_input}")
            st.write(f"**Bot:** {bot_response}")

elif mode == "Speech":
    if st.button("Speak"):
        user_input = speech_to_text()
        st.write(f"**You (speech):** {user_input}")
        bot_response = chatbot_response(user_input)
        st.write(f"**Bot:** {bot_response}")
