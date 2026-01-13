import logging
try:
    from sentence_transformers import SentenceTransformer, util
except ImportError:
    SentenceTransformer = None

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import torch

# Load model globally
model = None
try:
    if SentenceTransformer:
        # Limit torch to single thread to save memory on Render
        torch.set_num_threads(1)
        torch.set_num_interop_threads(1)
        
        logger.info("Loading Lightweight SBERT (paraphrase-MiniLM-L3-v2)...")
        model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
        logger.info("Lighter model loaded successfully.")
    else:
        logger.warning("SentenceTransformers not available, will use TF-IDF fallback.")
except Exception as e:
    logger.error(f"Failed to load SBERT model: {e}")
    model = None

def calculate_similarity(resume_text, job_description):
    """
    Calculates similarity between resume and JD.
    Falls back to TF-IDF if SBERT is unavailable.
    """
    if model:
        try:
            embeddings = model.encode([job_description, resume_text], convert_to_tensor=True)
            cosine_scores = util.cos_sim(embeddings[0], embeddings[1])
            score = cosine_scores.item()
            return round(score * 100, 2)
        except Exception as e:
            logger.error(f"SBERT encoding failed: {e}. Falling back to TF-IDF.")
    
    # TF-IDF Fallback
    try:
        vectorizer = TfidfVectorizer()
        tfidf = vectorizer.fit_transform([job_description, resume_text])
        score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        return round(float(score) * 100, 2)
    except Exception as e:
        logger.error(f"TF-IDF similarity failed: {e}")
        return 0.0

def rank_resumes(resumes_data, job_description):
    ranked_resumes = []
    for resume in resumes_data:
        score = calculate_similarity(resume['text'], job_description)
        ranked_resumes.append({
            'filename': resume['filename'],
            'score': score,
            'email': resume.get('contact', {}).get('email'),
            'phone': resume.get('contact', {}).get('phone'),
            'skills': ', '.join(resume.get('skills', [])),
            'education': ', '.join(resume.get('education', [])),
            'experience': resume.get('experience')
        })
    ranked_resumes.sort(key=lambda x: x['score'], reverse=True)
    return ranked_resumes

