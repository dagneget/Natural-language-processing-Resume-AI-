import os
import argparse
from src.parser import extract_text_from_file
from src.extractor import extract_skills, extract_contact_info
from src.screener import rank_resumes
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description="Automated Resume Screening Tool")
    parser.add_argument("--resumes", default="data/resumes", help="Path to resumes folder")
    parser.add_argument("--jd", default="data/job_descriptions", help="Path to job descriptions folder")
    parser.add_argument("--jd_file", help="Specific JD file to use (optional)")
    
    args = parser.parse_args()
    
    # 1. Load Job Description
    jd_text = ""
    if args.jd_file:
         jd_text = extract_text_from_file(args.jd_file)
    else:
        # Just pick the first file in the JD folder for now
        if not os.path.exists(args.jd):
             print(f"Job descriptions folder not found: {args.jd}")
             return
        
        jd_files = os.listdir(args.jd)
        if not jd_files:
             print("No job descriptions found in data/job_descriptions")
             return
             
        jd_path = os.path.join(args.jd, jd_files[0])
        print(f"Using Job Description: {jd_files[0]}")
        jd_text = extract_text_from_file(jd_path)

    if not jd_text:
        print("Could not extract text from Job Description.")
        return

    # 2. Process Resumes
    if not os.path.exists(args.resumes):
        print(f"Resumes folder not found: {args.resumes}")
        return

    resumes_data = []
    resume_files = [f for f in os.listdir(args.resumes) if f.lower().endswith(('.pdf', '.docx', '.txt'))]
    
    if not resume_files:
        print("No resumes found to process.")
        return

    print(f"Processing {len(resume_files)} resumes...")
    
    for filename in resume_files:
        filepath = os.path.join(args.resumes, filename)
        text = extract_text_from_file(filepath)
        
        if text:
            skills = extract_skills(text)
            contact = extract_contact_info(text)
            resumes_data.append({
                'filename': filename,
                'text': text,
                'skills': skills,
                'contact': contact
            })

    # 3. Rank and Score
    ranked = rank_resumes(resumes_data, jd_text)
    
    # 4. Output Results
    print("\n--- Recruitment Results ---\n")
    df = pd.DataFrame(ranked)
    print(df[['filename', 'score', 'email', 'skills']].to_string(index=False))
    
    # Save to CSV
    df.to_csv("results.csv", index=False)
    print("\nResults saved to results.csv")

if __name__ == "__main__":
    main()
