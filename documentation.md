# 📘 Project Documentation: Resume AI Application

## 1. Project Overview
**Resume AI** is an intelligent Candidate Screening and Ranking application designed to automate the initial analysis of job applications. It uses a hybrid Natural Language Processing (NLP) engine to extract skills, understand semantic meaning, and rank candidates against specific job descriptions.

---

## 2. 🤖 Key Functionalities

### A. Hybrid Skill Extraction Engine
The system uses a triple-layer approach to identify candidate skills:
1.  **Deep Learning (BERT)**: Uses `transformers` to identify skills based on context (e.g., "Deployed on EC2" -> "AWS").
2.  **Machine Learning (TF-IDF + SGD)**: A trained classifier that recognizes skill-like patterns in text.
3.  **Keyword Matching (Regex)**: A robust fallback for 500+ common technical terms (Python, SQL, React, etc.).

### B. Semantic Candidate Ranking
Unlike traditional ATS (Applicant Tracking Systems) that only count keywords, this project uses **Sentence-Transformers (SBERT)** to calculate **Semantic Similarity**.
-   **Method**: Converts both the Resume and Job Description into 384-dimensional vector embeddings.
-   **Benefit**: Matches specialized terms (e.g., "React Native") with general requirements (e.g., "Mobile Development") even if exact keywords differ.

### C. Automated Domain Classification
The system automatically predicts the candidate's professional domain (e.g., "Data Science", "Sales", "Web Development") using a supervised Multi-Class Classifier trained on 900+ resumes.

### D. Professional Reporting
Automatically generates a downloadable **PDF Scorecard** for every analysis, containing:
-   Executive Summary
-   Match Score (0-100%)
-   Contact Details (Email/Phone)
-   Extracted Skills List

---

## 3. 📊 Data & Models

### Dataset
The project was originally trained on the **UpdatedResumeDataSet** (sourced from Kaggle/Hugging Face), which contains approx. **962 Resumes** across **25+ Categories**.
-   **Size**: ~3MB CSV file.
-   **Fields**: `Category` (Label), `Resume` (Text).

### Models Used
| features | Model / Technology | Purpose |
| :--- | :--- | :--- |
| **Skill Extraction** | `bert-base-ner` (HuggingFace) | Contextual entity recognition |
| **Ranking** | `all-MiniLM-L6-v2` (Sentence-Transformers) | Text Embeddings & Cosine Similarity |
| **Classification** | `SGDClassifier` (Scikit-Learn) | Predicting Resume Category |
| **Text Processing** | `NLTK` & `Spacy` | Tokenization & Stopword removal |

---

## 4. 🛠 Technical Architecture

### Backend (Python/FastAPI)
-   **Framework**: FastAPI (High performance async framework).
-   **Environment**: Docker container (Python 3.10+).
-   **API Endpoints**:
    -   `POST /analyze`: Main endpoint processing PDF uploads.
    -   `GET /report/{id}`: Serves generated PDF reports.

### Frontend (React/Vite)
-   **Framework**: React 18 with Vite.
-   **Styling**: Modern CSS with Glassmorphism effects.
-   **Communication**: Fetches data from Backend API via HTTP.

### Deployment (Docker)
-   **Containerization**: Full stack is containerized using `docker-compose`.
-   **Isolation**: Features isolated environments to prevent dependency conflicts (e.g., between PyTorch and System libraries).

---

## 5. 🚀 Usage Guide

### Prerequisites
-   Docker Desktop (Recommended)
-   OR Python 3.10+ & Node.js 18+ (For local run)

### Running the Project
1.  **Start Application**:
    ```bash
    docker-compose up --build
    ```
2.  **Access UI**:
    Open browser to `http://localhost:5173`
3.  **Analyze**:
    -   Paste a Job Description (or leave empty).
    -   Upload a Resume (PDF/DOCX).
    -   Click "Analyze Candidate".

### Training Custom Models
To retrain the internal classifiers on new data:
1.  Place your dataset (CSV/JSON) in the `data/` folder.
2.  Configure `data/training_config.json`.
3.  Run the training script:
    ```bash
    python train_model.py
    ```

---

## 6. 📁 structure
```
NLP-Project/
├── data/               # Datasets & Training Configs
├── models/             # Saved .pkl models (Classifier, Vectorizer)
├── src/                # Core NLP Logic
│   ├── extractor.py    # Skill Extraction
│   ├── parser.py       # PDF/Docx Text Reading
│   ├── reporter.py     # PDF Report Generation
│   └── screener.py     # Similarity Calculation
├── ui/                 # React Frontend
├── server.py           # FastAPI Backend
├── train_model.py      # ML Training Script
└── docker-compose.yml  # Deployment Config
```
