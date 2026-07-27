import streamlit as st
import joblib
import re
import spacy
import nltk
from nltk.corpus import stopwords

# Download NLTK data securely for Streamlit Cloud
@st.cache_resource
def download_nltk_data():
    nltk.download('stopwords')

download_nltk_data()
stop_words = set(stopwords.words('english'))

# Load saved models
model = joblib.load('phishing_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def extract_sender_domain(text):
    match = re.search(r'[\w\.-]+@([\w\.-]+)', str(text))
    return match.group(1) if match else "unknown_domain"

def advanced_preprocess(text):
    text = str(text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'http[s]?://\S+', 'httpaddr', text)
    text = re.sub(r'\W', ' ', text).lower()
    
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if token.text not in stop_words and not token.is_space]
    return " ".join(tokens)

# UI Layout
st.set_page_config(page_title="AI Phishing Detector", page_icon="🛡️")
st.title("🛡️ AI Phishing Email Detector (spaCy & NLTK Powered)")
st.write("Paste an email below to analyze it using Advanced NLP.")

user_email = st.text_area("Email Content", height=200, placeholder="Paste suspicious email text or headers here...")

if st.button("Analyze Email"):
    if user_email.strip() == "":
        st.warning("Please paste an email first.")
    else:
        # We extract domain to show on UI, but only feed text to the model
        domain = extract_sender_domain(user_email)
        cleaned_text = advanced_preprocess(user_email)
        
        vectorized_text = vectorizer.transform([cleaned_text])
        prediction = model.predict(vectorized_text)[0]
        
        st.divider()
        st.write(f"**Detected Sender Domain:** `{domain}`")
        if prediction == 1:
            st.error("🚨 **WARNING: PHISHING DETECTED** 🚨")
            st.write("This message exhibits known structural and linguistic traits of phishing attacks.")
        else:
            st.success("✅ **SAFE: NO PHISHING DETECTED** ✅")
            st.write("This email appears to be legitimate.")