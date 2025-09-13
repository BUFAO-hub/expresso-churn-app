import streamlit as st
import nltk
import speech_recognition as sr
import random
import os

# ---------------------------
# Step 1: Load and preprocess chatbot data
# ---------------------------
nltk.download("punkt")

# Example simple chatbot responses (you can load from file instead)
responses = {
    "hello": ["Hi there!", "Hello!", "Hey! How can I help you?"],
    "how are you": ["I'm doing great, thanks for asking!", "All good here. How about you?"],
    "bye": ["Goodbye!", "See you later!", "Take care!"],
}

def preprocess(text):
    """Lowercase and tokenize input."""
    return text.lower()

def chatbot_response(user_input):
    user_input = preprocess(user_input)
    for key in responses.keys():
        if key in user_input:
            return random.choice(responses[key])
    return "Sorry, I didn’t understand that."

# ---------------------------
# Step 2: Speech recognition function
# ---------------------------
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎤 Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError:
            return "Sorry, there was a problem with the speech recognition service."

# ---------------------------
# Step 3: Streamlit App
# ---------------------------
st.title("🗣️ Speech-Enabled Chatbot")

# Input mode selector
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
