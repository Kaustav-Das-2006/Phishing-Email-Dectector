import streamlit as st
import joblib
import re

# 1. Load the saved model and vectorizer
model = joblib.load('phishing_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# 2. Recreate the exact cleaning function from your notebook
def preprocess_email(text):
    text = str(text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'http[s]?://\S+', 'httpaddr', text)
    text = re.sub(r'\W', ' ', text)
    text = text.lower()
    return text

# 3. Build the User Interface
st.set_page_config(page_title="AI Phishing Detector", page_icon="🛡️")

st.title("🛡️ AI Phishing Email Detector")
st.write("Paste an email below to analyze it for malicious linguistic patterns, fake urgency, and hidden URLs.")

# Text box for user input
user_email = st.text_area("Email Content", height=200, placeholder="Paste the suspicious email here...")

# 4. Make the Prediction
if st.button("Analyze Email"):
    if user_email.strip() == "":
        st.warning("Please paste an email first.")
    else:
        # Clean the input, vectorize it, and predict
        cleaned_text = preprocess_email(user_email)
        vectorized_text = vectorizer.transform([cleaned_text])
        prediction = model.predict(vectorized_text)[0]
        
        st.divider()
        
        # Display the results
        if prediction == 1:
            st.error("🚨 **WARNING: PHISHING DETECTED** 🚨")
            st.write("This email matches the mathematical fingerprint of known phishing attacks. Do not click any links.")
        else:
            st.success("✅ **SAFE: NO PHISHING DETECTED** ✅")
            st.write("This email appears to be legitimate.")