# To-Do List: Automated Resume Screening and Skill Extraction Project

## Phase 1: Requirements & Planning

* [ ] Write a clear project problem statement.
* [ ] Define detailed objectives.
* [ ] Identify all project deliverables.
* [ ] Draft initial architecture plan.

## Phase 2: Dataset Collection

* [ ] Download open-source resume datasets.
* [ ] Acquire skill taxonomy dataset (ESCO, O*NET).
* [ ] Gather job description samples.
* [ ] Organize datasets by type and format.

## Phase 3: Data Preprocessing

* [ ] Convert PDF/DOCX resumes into readable text.
* [ ] Remove formatting artifacts and noise.
* [ ] Segment resumes into sections (Education, Skills, Experience).
* [ ] Build normalization routines for skills and job titles.
* [ ] Annotate NER labels for training data.

## Phase 4: Baseline Implementation

* [ ] Implement regex-based extraction.
* [ ] Build keyword-matching skill extractor.
* [ ] Test rule-based parsing on sample resumes.
* [ ] Document limitations.

## Phase 5: Model Development

* [ ] Select pretrained transformer model.
* [ ] Fine-tune NER for skills, education, experience.
* [ ] Train similarity model for resume–job matching.
* [ ] Evaluate model performance.
* [ ] Conduct hyperparameter tuning.

## Phase 6: Pipeline Integration

* [ ] Create data pipeline for resume processing.
* [ ] Integrate NER model into pipeline.
* [ ] Map extracted skills to taxonomy.
* [ ] Build ranking function for candidate scoring.
* [ ] Test end-to-end workflow.

## Phase 7: Evaluation & Testing

* [ ] Confirm NER accuracy with F1, precision, recall.
* [ ] Evaluate ranking model relevance.
* [ ] Perform qualitative testing with sample resumes.
* [ ] Perform error analysis.

## Phase 8: Deployment Preparation

* [ ] Build API for resume screening.
* [ ] Create JSON output structure.
* [ ] Containerize using Docker.
* [ ] Run performance & inference tests.

## Phase 9: Final Documentation

* [ ] Write final report.
* [ ] Add system architecture diagrams.
* [ ] Prepare README with installation and usage steps.
* [ ] Package project for submission.
