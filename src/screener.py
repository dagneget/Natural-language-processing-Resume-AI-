from sentence_transformers import SentenceTransformer, util
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load model globally to avoid reloading on every request (crucial for performance)
logger.info("Loading SBERT model (all-MiniLM-L6-v2)...")
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    logger.info("SBERT model loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load SBERT model: {e}")
    model = None

def calculate_similarity(resume_text, job_description):
    """
    Calculates the semantic similarity between the resume text and the job description
    using SentenceBERT embeddings.
    """
    if not model:
        logger.warning("Model not loaded, returning 0 score.")
        return 0.0
        
    # Encode both texts to get their embeddings
    # Convert to list if single string to satisfy some versions, though encode handles strings too.
    embeddings = model.encode([job_description, resume_text], convert_to_tensor=True)
    
    # Compute cosine similarity
    cosine_scores = util.cos_sim(embeddings[0], embeddings[1])
    
    # Extract score (tensor to float)
    score = cosine_scores.item()
    
    # Convert to percentage 0-100
    match_percentage = round(score * 100, 2)
    
    return match_percentage

def rank_resumes(resumes_data, job_description):
    """
    Ranks resumes based on semantic similarity to job description.
    resumes_data: List of dicts {'filename': str, 'text': str, 'skills': list}
    """
    ranked_resumes = []
    
    for resume in resumes_data:
        score = calculate_similarity(resume['text'], job_description)
        ranked_resumes.append({
            'filename': resume['filename'],
            'score': score,
            'email': resume.get('contact', {}).get('email'),
            'phone': resume.get('contact', {}).get('phone'),
            'skills': ', '.join(resume.get('skills', []))
        })
    
    ranked_resumes.sort(key=lambda x: x['score'], reverse=True)
    return ranked_resumes
