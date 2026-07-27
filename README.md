# 🛡️ AI-Driven Phishing Email Detector

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Live-red.svg)
![NLP](https://img.shields.io/badge/NLP-spaCy%20%7C%20NLTK-green.svg)
![Machine Learning](https://img.shields.io/badge/ML-Scikit_Learn-orange.svg)

## 📌 Project Overview

This project implements a robust Natural Language Processing (NLP) pipeline to automatically detect and classify phishing emails. By tokenizing text and extracting frequency-based mathematical features, the machine learning model identifies semantic and structural threats (such as manufactured urgency and deceptive links) faster and more accurately than manual human review.

The system is deployed as a real-time web application via Streamlit Community Cloud.

**[🔴 Try the Live Application Here](https://phishing-ml-pipeline.streamlit.app/)**

## 🧠 System Architecture & Methodology

### 1. Data Preprocessing & Metadata Extraction

- **Noise Reduction:** Stripped HTML tags, standard punctuation, and non-alphanumeric characters.
- **Feature Engineering:** Extracted sender domains and systematically replaced all embedded URLs with a standardized `httpaddr` token to capture structural phishing indicators.
- **NLP Pipeline:** Utilized **spaCy** for advanced tokenization and lemmatization, and **NLTK** for standard English stopword removal.
- **Data Integrity:** Dropped duplicate records prior to vectorization to strictly prevent train-test contamination.

### 2. Feature Extraction (TF-IDF)

The cleaned text was transformed into a numerical matrix using Term Frequency-Inverse Document Frequency (TF-IDF). To eliminate data leakage, the vectorizer was fitted _exclusively_ on the 80% training set before transforming the 20% testing set, limited to the top 5,000 most significant features.

### 3. Model Evaluation

Four distinct classification algorithms were trained and evaluated:

- **Logistic Regression**
- **Multinomial Naive Bayes**
- **Neural Network (MLP)**
- **Random Forest** (Selected for final deployment)

_Note: Strict train-test splitting and data deduplication confirmed the absence of data leakage. Feature importance analysis revealed the underlying benchmark dataset was highly linearly separable due to engineered structural tokens._

## 🚀 How to Run Locally

### Prerequisites

Ensure you have Python 3.11 installed.

### Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/phishing-email-detector.git](https://github.com/your-username/phishing-email-detector.git)
   cd phishing-email-detector
   ```
