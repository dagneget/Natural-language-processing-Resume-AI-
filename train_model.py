import os
import joblib
import numpy as np
import json
import re
import ast
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report

model_dir = "models"
os.makedirs(model_dir, exist_ok=True)
config_path = "data/training_config.json"

def get_features(token):
    return {
        "word": token.lower(),
        "is_upper": token.isupper(),
        "is_title": token.istitle(),
        "is_digit": token.isdigit(),
        "len": len(token),
        "prefix-2": token[:2],
        "suffix-2": token[-2:],
    }

def clean_token(token):
    return re.sub(r'^[^\w]+|[^\w]+$', '', token).lower()

def load_and_normalize_data():
    if not os.path.exists(config_path):
        print(f"Config not found at {config_path}")
        return [], []

    with open(config_path, 'r') as f:
        config = json.load(f)

    X_features = []
    y_labels = []
    
    for ds_config in config['datasets']:
        ds_name = ds_config['name']
        print(f"Loading {ds_name}...")
        
        try:
            # Check if it's a local file
            if os.path.exists(ds_name):
                print(f"Detected local file: {ds_name}")
                if ds_name.endswith('.csv'):
                    df = pd.read_csv(ds_name)
                elif ds_name.endswith('.json'):
                    df = pd.read_json(ds_name)
                elif ds_name.endswith('.parquet'):
                    df = pd.read_parquet(ds_name)
                else:
                    print(f"Unsupported file extension: {ds_name}")
                    continue
            else:
                # Assume Hugging Face dataset
                print(f"Loading from Hugging Face: {ds_name}")
                try:
                    df = pd.read_parquet(f"hf://datasets/{ds_name}")
                except Exception:
                    print("Trying fallback URL pattern...")
                    df = pd.read_parquet(f"hf://datasets/{ds_name}/data/train-00000-of-00001.parquet")

        except Exception as e:
            print(f"Failed to load {ds_name}: {e}")
            continue

        print(f"Loaded {len(df)} rows.")

        count = 0
        # Iterate over DataFrame
        for _, item in df.iterrows():
            # Removed limit: processing full dataset
            count += 1
            if count % 1000 == 0:
                print(f"[{ds_name}] Processed {count} items...")

            text = item.get(ds_config['text_col'])
            if not isinstance(text, str) or not text: continue
            
            # Extract distinct skill/entity words from the row
            entity_words = set()
            
            raw_entities = item.get(ds_config['entities_col'])
            
            # Logic to parse entities based on format
            if ds_config['format'] == 'text_and_list':
                # sonchuate style
                entities_list = []
                if isinstance(raw_entities, list):
                    entities_list = raw_entities
                elif isinstance(raw_entities, str):
                    if '|' in raw_entities:
                        entities_list = raw_entities.split('|')
                    else:
                        entities_list = [raw_entities]
                elif isinstance(raw_entities, np.ndarray): # Pandas might return numpy array
                     entities_list = raw_entities.tolist()
                
                for ent in entities_list:
                     if isinstance(ent, str):
                        for w in ent.split():
                            entity_words.add(clean_token(w))
            
            # Tokenize & Label
            tokens = text.split()
            for token in tokens:
                cl = clean_token(token)
                # Exact match against set of words
                if cl in entity_words and len(cl) > 1:
                    label = 1
                else:
                    label = 0
                
                X_features.append(get_features(token))
                y_labels.append(label)
                
    return X_features, y_labels

def main():
    print("Starting Multi-Sector Training (Pandas Mode)...")
    
    X_features, y_labels = load_and_normalize_data()
    
    if not X_features:
        print("No data extracted. Exiting.")
        return
        
    print(f"Total tokens extracted: {len(X_features)}")
    print(f"Stats: Skill tokens: {sum(y_labels)}, Non-skill tokens: {len(y_labels) - sum(y_labels)}")
    
    if sum(y_labels) < 2:
        print("Error: Too few positive examples to train. Check data parsing.")
        return

    # Vectorize
    print("Vectorizing...")
    vec = DictVectorizer(sparse=True)
    X = vec.fit_transform(X_features)
    y = np.array(y_labels)

    # Train
    print("Training Model...")
    # Using partial_fit would be better for huge data, but fit is fine for 10k items
    clf = SGDClassifier(loss='log_loss', max_iter=10, random_state=42)
    clf.fit(X, y)

    # Evaluate
    print("Evaluating...")
    y_pred = clf.predict(X)
    print(classification_report(y, y_pred, target_names=["Not Skill", "Skill"]))

    # Save
    print("Saving model...")
    joblib.dump(clf, os.path.join(model_dir, "skill_classifier.pkl"))
    joblib.dump(vec, os.path.join(model_dir, "vectorizer.pkl"))
    print("Training complete!")

if __name__ == "__main__":
    main()
