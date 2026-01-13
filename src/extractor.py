import re
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_entities_basic(text):
    """
    Enhanced extraction using comprehensive keyword matching and specialized regex.
    """
    text_lower = text.lower()
    
    extracted = {
        "skills": set(),
        "education": set(),
        "experience": set(),
        "job_titles": set(),
        "companies": set()
    }
    
    # Comprehensive Skill Categories
    skill_map = {
        "Languages": ["python", "javascript", "java", "c\+\+", "c\#", "ruby", "golang", "typescript", "swift", "kotlin", "rust", "php", "scala"],
        "Web Tech": ["react", "node", "express", "angular", "vue", "html5", "css3", "sass", "tailwind", "bootstrap", "next.js", "graphql", "rest api"],
        "Cloud/DevOps": ["aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "terraform", "ansible", "ci/cd", "serverless", "ec2", "s3", "lambda"],
        "Data/AI": ["sql", "nosql", "postgresql", "mongodb", "redis", "elasticsearch", "spark", "hadoop", "nlp", "machine learning", "deep learning", "pytorch", "tensorflow", "pandas", "numpy", "scikit-learn", "data science"],
        "Frameworks": ["fastapi", "django", "flask", "spring boot", "laravel", "pytorch", "keras", "opencv"],
        "Business/Productivity": ["google workspace", "microsoft office", "trello", "asana", "calendar management", "inbox management", "data entry", "project coordination", "virtual assistance", "administrative support"]
    }

    for category, skills in skill_map.items():
        for skill in skills:
            pattern = rf'\b{re.escape(skill)}\b'
            if re.search(pattern, text_lower):
                # Format appropriately
                display_name = skill.replace('\\', '').title()
                if len(skill) <= 3 or skill.lower() in ["aws", "gcp", "sql", "api", "nlp", "php"]:
                    display_name = skill.replace('\\', '').upper()
                extracted["skills"].add(display_name)
            
    # Specialized Domain Detection (Job Titles)
    titles = ["software engineer", "data scientist", "frontend developer", "backend developer", "fullstack developer", "devops engineer", "product manager", "project manager", "qa engineer", "solutions architect", "virtual assistant", "administrative assistant", "event coordinator"]
    for title in titles:
        if re.search(rf'\b{re.escape(title)}\b', text_lower):
            extracted["job_titles"].add(title.title())

    # Education Patterns (Improved)
    edu_keywords = ["university", "college", "institute", "school", "bachelor", "master", "phd", "btech", "mtech", "degree"]
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    for line in lines:
        line_low = line.lower()
        if any(kw in line_low for kw in edu_keywords):
            # Clean up the line (remove extra dates or symbols often found in resume headers)
            clean_edu = re.sub(r'\d{4}', '', line).strip(' ,-')
            if len(clean_edu) > 5:
                extracted["education"].add(clean_edu)
            
    # Experience Patterns (Robust year extraction)
    exp_patterns = [
        r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
        r'experience[:\s]+(\d+)\s*years',
        r'(?:total|overall)\s*(\d+)\s*years'
    ]
    for pattern in exp_patterns:
        match = re.search(pattern, text_lower)
        if match:
            extracted["experience"].add(f"{match.group(1)}")
            break

    return {k: list(v) for k, v in extracted.items()}

def extract_skills(text):
    data = extract_entities_basic(text)
    return data.get("skills", [])

def extract_all_details(text):
    data = extract_entities_basic(text)
    contact = extract_contact_info(text)
    
    data["email"] = contact["email"]
    data["phone"] = contact["phone"]
    
    return data

def extract_contact_info(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'(?:\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}'
    
    email = re.findall(email_pattern, text)
    phone = re.findall(phone_pattern, text)
    
    return {
        "email": email[0] if email else None,
        "phone": phone[0] if phone else None
    }

def extract_education(text):
    data = extract_entities_basic(text)
    return data.get("education", [])

def extract_experience(text):
    data = extract_entities_basic(text)
    exps = data.get("experience", [])
    return exps[0] if exps else None   

