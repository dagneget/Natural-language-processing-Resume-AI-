import re
import os
import joblib

# Global variable for model
bert_nlp = None

def extract_skills_bert(text):
    """
    Extract skills using BERT Deep Learning model.
    Returns a list of unique skills.
    
    NOTE: Setup to import transformers ONLY inside the function
    to prevent DLL crashes on Windows systems that have broken PyTorch.
    On Docker (Linux), this will import successfully.
    """
    global bert_nlp
    
    if bert_nlp is None:
        try:
            from transformers import pipeline
            bert_nlp = pipeline('token-classification', model='yashpwr/resume-ner-bert-v2', aggregation_strategy='simple')
        except Exception:
            # Silent failure or log once
            return []

    try:
        # BERT has a token limit (usually 512). We process the first chunk of text.
        # For a full implementation, we'd overlap-chunk the text.
        # Truncate to ~2000 chars roughly to avoid massive inputs, though pipeline handles some.
        results = bert_nlp(text[:2000])
        
        skills = set()
        for entity in results:
            # The model returns entities with groups like 'LABEL_1' or 'Skill' depending on training
            # yashpwr model usually returns 'Skill' entities
            if 'Skill' in entity.get('entity_group', '') or 'LABEL_1' in entity.get('entity_group', ''):
                skills.add(entity['word'].strip())
                
        return list(skills)
    except Exception as e:
        print(f"BERT Extraction failed: {e}")
        return []

# Load trained model if available
MODEL_PATH = "models/skill_classifier.pkl"
VEC_PATH = "models/vectorizer.pkl"
clf = None
vec = None

if os.path.exists(MODEL_PATH) and os.path.exists(VEC_PATH):
    try:
        clf = joblib.load(MODEL_PATH)
        vec = joblib.load(VEC_PATH)
        print("Loaded ML model for skill extraction.")
    except Exception as e:
        print(f"Error loading ML model: {e}")

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

def extract_skills_ml(text):
    """
    Extract skills using the trained scikit-learn model.
    """
    if not clf or not vec:
        return []

    tokens = text.split()
    features = [get_features(t) for t in tokens]
    
    # Vectorize
    X = vec.transform(features)
    
    # Predict
    preds = clf.predict(X)
    
    skills = set()
    for token, label in zip(tokens, preds):
        if label == 1:
            # Simple cleaning
            clean_token = re.sub(r'^[^\w]+|[^\w]+$', '', token)
            if len(clean_token) > 1: # Ignore single chars
                skills.add(clean_token)
            
    return list(skills)

def extract_skills(text):
    """
    Extracts potential skills using ML model first, then falls back/augments with Regex.
    """
    found_skills = set()
    
    # 1. BERT Extraction (Highest Priority)
    found_skills.update(extract_skills_bert(text))
    
    # 2. ML Extraction (Scikit-Learn)
    if clf:
        ml_skills = extract_skills_ml(text)
        found_skills.update(ml_skills)

    # 3. Regex Extraction (Fallback)
    # Hybrid approach is usually best
    common_skills = [
        "python", "java", "c++", "javascript", "html", "css", "sql", "react", 
        "node.js", "aws", "docker", "kubernetes", "machine learning", "nlp",
        "pytorch", "tensorflow", "git", "linux", "excel", "communication",
        "scikit-learn", "pandas", "numpy"
    ]
    
    for skill in common_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            found_skills.add(skill)

    return list(found_skills)

def extract_contact_info(text):
    """
    Extracts email and phone number.
    """
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'(?:\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}'
    
    email = re.findall(email_pattern, text)
    phone = re.findall(phone_pattern, text)
    
    return {
        "email": email[0] if email else None,
        "phone": phone[0] if phone else None
    }

def extract_education(text):
    """
    Extracts education degrees using Regex.
    """
    # Common degrees
    patterns = [
        r"(?i)\b(?:B\.?Sc|M\.?Sc|B\.?A|M\.?A|B\.?Tech|M\.?Tech|Ph\.?D|MBA|Bachelor|Master|Diploma)\b.*?(?:in|of)?.*?(?:Computer Science|Engineering|Information Technology|Data Science|Business|Arts)?",
    ]
    
    education = []
    for pattern in patterns:
        found = re.findall(pattern, text)
        for f in found:
            # Clean up long matches that might be false positives
            if len(f.split()) < 10: 
                education.append(f.strip())
                
    # Deduplicate while preserving order
    return list(dict.fromkeys(education))

def extract_experience(text):
    """
    Extracts years of experience.
    """
    # Pattern: "5+ years of experience", "5 years experience", "Experience: 5 years"
    pattern = r"(\d+(?:\.\d+)?\+?)\s*(?:years?|yrs?)\s*(?:of)?\s*experience"
    
    matches = re.search(pattern, text, re.IGNORECASE)
    if matches:
        return matches.group(1) # Return the number part (e.g. "5+")
    
    # Fallback to just finding "X years" if it looks like a summary
    # Be more conservative here
    return None
