# Automated Resume Screening and Skill Extraction Using NLP

This project automates the process of screening resumes against a job description using Natural Language Processing (NLP).

## Features
- **Text Extraction**: parsed text from PDF, DOCX, and TXT files.
- **Skill Extraction**: Identifies skills using spaCy NER and keyword matching.
- **Ranking**: scores resumes based on cosine similarity to the job description.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

2. Place files:
   - Put candidate resumes in `data/resumes/`
   - Put the Job Description in `data/job_descriptions/`

### Option 2: Run with Docker (Recommended)
This is the easiest way to run the app on any machine.
Prerequisite: Install [Docker Desktop](https://www.docker.com/products/docker-desktop/).

1.  **Build and Run**:
    ```bash
    docker-compose up --build
    ```
2.  **Open Dashboard**:
    Go to `http://localhost:5173`

---

## 🛠 Features
- **Smart Parsing**: Extracts text from PDF/DOCX.
- **Skill Extraction**: Hybrid Model (Regex + ML) to find skills.
- **Categorization**: Classifies resumes into domains (e.g. Data Science).
- **Semantic Search**: Matches job descriptions by meaning (SBERT).
- **PDF Reports**: Generates downloadable scorecards.

## Usage

Run the main script:
```bash
python main.py
```

Options:
- `--resumes`: Path to resumes folder (default: `data/resumes`)
- `--jd`: Path to job descriptions folder (default: `data/job_descriptions`)
- `--jd_file`: Path to a specific JD file.

## Output
Results are printed to the console and saved to `results.csv`.
