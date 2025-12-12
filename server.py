from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import shutil
import os
import uuid
from typing import List

# Import our NLP logic
from src.parser import extract_text_from_file
from src.extractor import extract_skills, extract_contact_info
from src.screener import calculate_similarity

app = FastAPI()

# Enable CORS for React frontend (dev mode)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for dev, restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
        
        # 2. Extract Skills & Info
        # 2. Extract Skills (Hybrid)
        skills, info = extract_skills(resume_text)
        
        # 3. Categorize Resume
        category = "Unknown"
        if os.path.exists("models/category_model.pkl"):
            try:
                clf = joblib.load("models/category_model.pkl")
                enc = joblib.load("models/category_encoder.pkl")
                
                # Clean text before predicting (same logic as training)
                import re
                def clean(text):
                    clean = re.sub('http\S+\s*', ' ', text)
                    clean = re.sub('RT|cc', ' ', clean)
                    clean = re.sub('#\S+', '', clean)
                    clean = re.sub('@\S+', '  ', clean)
                    clean = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', clean)
                    clean = re.sub(r'[^\x00-\x7f]',r' ', clean)
                    clean = re.sub('\s+', ' ', clean)
                    return clean.lower()
                    
                cleaned_text = clean(resume_text)
                prediction = clf.predict([cleaned_text])
                category = enc.inverse_transform(prediction)[0]
            except Exception as e:
                print(f"Classification failed: {e}")

        # 4. Calculate Score
        score = calculate_similarity(resume_text, job_description)
        
        # 5. Generate Report
        from src.reporter import generate_report
        report_path = generate_report({
            "score": score,
            "skills": skills,
            "contact": info,
            "category": category
        }, job_description, resume.filename)
        
        # Cleanup
        os.remove(temp_path)
        
        return {
            "filename": resume.filename,
            "score": score,
            "skills": skills,
            "contact": info,
            "category": category,
            "report_url": f"/report/Report_{resume.filename}.pdf",
            "summary": resume_text[:200] + "..." # Preview
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
    uvicorn.run(app, host="0.0.0.0", port=8000)
