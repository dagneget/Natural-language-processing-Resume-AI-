# Project Roadmap

## Phase 1: MVP (Completed)
- [x] **Project Setup**: Core structure, directories, and dependencies.
- [x] **Resume Parsing**: Support for PDF, DOCX, and TXT files.
- [x] **Skill Extraction**: Regex-based extraction of key technical skills.
- [x] **Screening Engine**: Cosine similarity scoring (TF-IDF) against Job Descriptions.
- [x] **CLI Tool**: `main.py` and `run_project.bat` for easy execution.
- [x] **Testing**: Unit tests for all modules.

## Phase 2: User Interface (Completed)
- [x] **Web Dashboard**: Create a modern web app (React/Next.js) to upload resumes and view rankings visually.
- [x] **Backend API**: FastAPI integration.

## Phase 3: Advanced NLP (Completed)
- [x] **Custom Model**: Trained a Scikit-Learn model on `sonchuate/resume_ner`.
- [x] **Hybrid Extraction**: Combined Regex + ML for robust skill detection.

## Phase 4: Next Steps (Proposed)
- [ ] **Deployment**: Dockerize the application for easy sharing.
- [/] **Semantic Search**: Implemented SBERT.
- [x] **PDF Reports**: Added PDF generation logic using `fpdf2`.
