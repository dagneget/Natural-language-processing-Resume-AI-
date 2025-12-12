import pandas as pd
import numpy as np
import re
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Paths
DATA_PATH = "data/UpdatedResumeDataSet.csv"
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "category_model.pkl")
ENCODER_PATH = os.path.join(MODEL_DIR, "category_encoder.pkl")

def clean_resume(text):
    clean = re.sub('http\S+\s*', ' ', text)
    clean = re.sub('RT|cc', ' ', clean)
    clean = re.sub('#\S+', '', clean)
    clean = re.sub('@\S+', '  ', clean)
    clean = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', clean)
    clean = re.sub(r'[^\x00-\x7f]',r' ', clean)
    clean = re.sub('\s+', ' ', clean)
    return clean.lower()

def train_classifier():
    if not os.path.exists(DATA_PATH):
        print(f"Dataset not found at {DATA_PATH}")
        print("Please download it from Kaggle and place it in the data/ folder.")
        return

    print("Loading dataset...")
    df = pd.read_csv(DATA_PATH)
    
    # Validation
    if 'Resume' not in df.columns or 'Category' not in df.columns:
        print("Error: Dataset missing 'Resume' or 'Category' columns.")
        return

    print(f"Training on {len(df)} resumes...")
    
    # Cleaning
    df['Cleaned_Resume'] = df['Resume'].apply(lambda x: clean_resume(x))
    
    # Encoding Labels
    le = LabelEncoder()
    df['Encoded_Category'] = le.fit_transform(df['Category'])
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(df['Cleaned_Resume'], df['Encoded_Category'], test_size=0.2, random_state=42)
    
    # Pipeline: TF-IDF -> Naive Bayes (Standard for Text Classification)
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', max_features=1500)),
        ('clf', MultinomialNB())
    ])
    
    print("Training model...")
    pipeline.fit(X_train, y_train)
    
    # Evaluate
    print("Evaluating...")
    preds = pipeline.predict(X_test)
    print(classification_report(y_test, preds, target_names=le.classes_))
    
    # Save
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    joblib.dump(le, ENCODER_PATH)
    print("Model saved successfully!")

if __name__ == "__main__":
    train_classifier()
