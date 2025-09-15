import streamlit as st
import nltk
import speech_recognition as sr
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
# Step 2: Speech-to-text using st.audio_input
# ---------------------------
def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError:
        return "API unavailable."

# ---------------------------
# Step 3: Streamlit App
# ---------------------------
st.title("🗣️ Speech-Enabled Chatbot (Streamlit Native)")

mode = st.radio("Choose input mode:", ("Text", "Speech"))

if mode == "Text":
    user_input = st.text_input("Type your message here:")
    if st.button("Send"):
        if user_input:
            bot_response = chatbot_response(user_input)
            st.write(f"**You:** {user_input}")
            st.write(f"**Bot:** {bot_response}")

elif mode == "Speech":
    audio_file = st.audio_input("🎤 Record or upload your voice")
    if audio_file is not None:
        text = speech_to_text(audio_file)
        st.write(f"**You (speech):** {text}")
        bot_response = chatbot_response(text)
        st.write(f"**Bot:** {bot_response}")
