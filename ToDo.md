# To-Do List: Automated Resume Screening and Skill Extraction Project

## Phase 1: Requirements & Planning

- [x] Write a clear project problem statement.
- [x] Define detailed objectives.
- [x] Identify all project deliverables.
- [x] Draft initial architecture plan.

## Phase 2: Dataset Collection

- [x] Download open-source resume datasets.
- [x] Acquire skill taxonomy dataset (ESCO, O\*NET).
- [x] Gather job description samples.
- [x] Organize datasets by type and format.

## Phase 3: Data Preprocessing

- [x] Convert PDF/DOCX resumes into readable text.
- [x] Remove formatting artifacts and noise.
- [x] Segment resumes into sections (Education, Skills, Experience).
- [x] Build normalization routines for skills and job titles.
- [x] Annotate NER labels for training data.

## Phase 4: Baseline Implementation

- [x] Implement regex-based extraction.
- [x] Build keyword-matching skill extractor.
- [x] Test rule-based parsing on sample resumes.
- [x] Document limitations.

## Phase 5: Model Development

- [x] Select pretrained transformer model (SBERT).
- [x] Fine-tune NER concepts for skills, education, experience.
- [x] Train similarity model for resume–job matching.
- [x] Evaluate model performance.
- [x] Conduct hyperparameter tuning for 512MB RAM stability.

## Phase 6: Pipeline Integration

- [x] Create data pipeline for resume processing.
- [x] Integrate NER logic into pipeline.
- [x] Map extracted skills to taxonomy.
- [x] Build ranking function for candidate scoring.
- [x] Test end-to-end workflow on Render.

## Phase 7: Evaluation & Testing

- [x] Confirm extraction accuracy.
- [x] Evaluate ranking model relevance.
- [x] Perform qualitative testing with sample resumes.
- [x] Perform error analysis (CORS & OOM fixes).

## Phase 8: Deployment Preparation

- [x] Build API (FastAPI) for resume screening.
- [x] Create JSON output structure.
- [x] Containerize using Docker (CPU-optimized).
- [x] Run performance & inference tests.

## Phase 9: Final Documentation

- [x] Write final report.
- [x] Add system architecture details.
- [x] Prepare README with installation and usage steps.
- [x] Package project for submission.
