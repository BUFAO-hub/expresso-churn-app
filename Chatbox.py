import nltk
# Ensure punkt and stopwords are available
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")
nltk.download("wordnet")
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import streamlit as st
import os

# --- Ensure NLTK resources are available ---
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

# --- Load the text file using relative path ---
file_path = os.path.join(os.path.dirname(__file__), "Symbol.txt")

if not os.path.exists(file_path):
    st.error(f"❌ Could not find {file_path}. Please make sure Symbol.txt is in the repo.")
    st.stop()

with open(file_path, "r", encoding="utf-8") as f:
    data = f.read().replace("\n", " ")

# --- Tokenize the text into sentences ---
sentences = sent_tokenize(data)

# --- Define a function to preprocess each sentence ---
def preprocess(sentence: str):
    words = word_tokenize(sentence)
    words = [
        word.lower()
        for word in words
        if word.lower() not in stopwords.words("english") and word not in string.punctuation
    ]
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return words

# --- Preprocess each sentence in the text ---
corpus = [preprocess(sentence) for sentence in sentences]

# --- Function to find most relevant sentence ---
def get_most_relevant_sentence(query: str) -> str:
    query = preprocess(query)
    max_similarity = 0
    most_relevant_sentence = "Sorry, I couldn't find a good match."
    for sentence in corpus:
        if len(query) == 0 and len(sentence) == 0:
            continue
        similarity = len(set(query).intersection(sentence)) / float(
            len(set(query).union(sentence))
        )
        if similarity > max_similarity:
            max_similarity = similarity
            most_relevant_sentence = " ".join(sentence)
    return most_relevant_sentence

# --- Chatbot wrapper ---
def chatbot(question: str) -> str:
    return get_most_relevant_sentence(question)

# --- Streamlit app ---
def main():
    st.title("📘 Chatbot")
    st.write("Hello! I'm a chatbot. Ask me anything about the topic in the text file.")

    question = st.text_input("You:")

    if st.button("Submit"):
        if question.strip() == "":
            st.warning("⚠️ Please type a question before submitting.")
        else:
            response = chatbot(question)
            st.success("Chatbot: " + response)

if __name__ == "__main__":
    main()
