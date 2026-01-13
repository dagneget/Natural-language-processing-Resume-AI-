from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import shutil
import os
import uuid
from typing import List
import joblib

# Import our NLP logic
from src.parser import extract_text_from_file
from src.extractor import extract_all_details, extract_skills
from src.screener import calculate_similarity

# Global models for caching
CLF = None
ENC = None

# Pre-load classification models
if os.path.exists("models/category_model.pkl"):
    try:
        import joblib
        CLF = joblib.load("models/category_model.pkl")
        ENC = joblib.load("models/category_encoder.pkl")
        print("Classification models loaded successfully.")
    except Exception as e:
        print(f"Warning: Could not load classification models: {e}")

def clean_text_for_classifier(text):
    """
    Cleaning logic for the classification model.
    """
    import re
    clean = re.sub(r'http\S+\s*', ' ', text)
    clean = re.sub('RT|cc', ' ', clean)
    clean = re.sub(r'#\S+', '', clean)
    clean = re.sub(r'@\S+', '  ', clean)
    clean = re.sub('[%s]' % re.escape(r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', clean)
    clean = re.sub(r'[^\x00-\x7f]',r' ', clean)
    clean = re.sub(r'\s+', ' ', clean)
    return clean.lower()

import gc

app = FastAPI()

# Refined CORS for production stability
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False, # Must be False when using origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "online", "message": "ResumeAI Precision API is Live!", "branch": "enhanced-skills-analysis"}

UPLOAD_DIR = "uploads"
REPORT_DIR = "reports"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Endpoint to upload a resume and JD, and get a suitability score.
    """
    try:
        # Save uploaded file temporarily
        file_ext = os.path.splitext(resume.filename)[1]
        temp_filename = f"{uuid.uuid4()}{file_ext}"
        temp_path = os.path.join(UPLOAD_DIR, temp_filename)
        
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)
            
        # 1. Parse Text
        resume_text = extract_text_from_file(temp_path)
        if not resume_text:
             os.remove(temp_path)
             raise HTTPException(status_code=400, detail="Could not extract text from file.")
        
        # 2. Extract Info (Single Pass)
        details = extract_all_details(resume_text)
        resume_skills = details.get("skills", [])
        
        # JD Skills (still use simple extract_skills wrapper for quickness or same logic)
        jd_skills = extract_skills(job_description) if job_description else []
        
        # Calculate Missing Skills
        r_skills_norm = {s.lower() for s in resume_skills}
        missing_skills = [s for s in jd_skills if s.lower() not in r_skills_norm]

        info = {"email": details.get("email"), "phone": details.get("phone")}
        education = details.get("education", [])
        experience = details.get("experience", [])
        
        # 3. Categorize Domain
        detected_titles = details.get("job_titles", [])
        if detected_titles:
            category = detected_titles[0]
        elif CLF and ENC:
            try:
                cleaned_text = clean_text_for_classifier(resume_text)
                prediction = CLF.predict([cleaned_text])
                category = ENC.inverse_transform(prediction)[0]
            except Exception as e:
                print(f"Classification failed: {e}")
        else:
             # Heuristic based on skills
             if details.get("skills"):
                 if any(s in ["Python", "Machine Learning", "NLP"] for s in details["skills"]):
                     category = "Data Science"
                 elif any(s in ["React", "HTML", "CSS"] for s in details["skills"]):
                     category = "Frontend Dev"
                 else:
                     category = "Software Engineer"
             else:
                 category = "Professional"

        # 4. Calculate Score
        score = calculate_similarity(resume_text, job_description)
        
        # 5. Generate Report
        from src.reporter import generate_report
        report_path = generate_report({
            "score": score,
            "skills": resume_skills,
            "missing_skills": missing_skills,
            "contact": info,
            "education": education,
            "experience": experience,
            "category": category
        }, job_description, resume.filename)
        
        # Cleanup
        os.remove(temp_path)
        # Clear large text variables before GC
        resume_text = None
        details = None
        gc.collect() 
        
        return {
            "filename": resume.filename,
            "score": score,
            "skills": resume_skills,
            "missing_skills": missing_skills,
            "contact": info,
            "education": education,
            "experience": experience,
            "category": category,
            "report_url": f"/report/Report_{resume.filename}.pdf",
            "summary": resume_text[:10000] # Limit preview size
        }

    except Exception as e:
        print(f"Error processing file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

from fastapi.responses import FileResponse

@app.get("/report/{filename}")
async def get_report(filename: str):
    file_path = os.path.join("reports", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Report not found")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
