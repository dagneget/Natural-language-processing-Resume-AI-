# 🚀 AI-Powered Resume Screener & Analyzer

A powerful, full-stack Natural Language Processing (NLP) application that automates resume screening, skill extraction, and candidate ranking. Built with Python, FastAPI, and React.

## ✨ Key Features

### 1. 🧠 Advanced Skill Extraction (Hybrid Engine)
We use a **Triple-Layer** extraction logic to ensure no skill is missed:
- **Layer 1: Deep Learning (BERT)**: Uses `transformers` to identify skills conceptually (e.g., understanding "coding in Rust" implies "Rust" is a skill). *Runs primarily in Docker/Linux environments.*
- **Layer 2: Machine Learning (Scikit-Learn)**: A trained TF-IDF model acting as a fallback to catch standard skill patterns locally.
- **Layer 3: Regex & Keyword Matching**: A hard-coded fallback to ensure common technologies (Java, Python, AWS) are never missed.

### 2. 🔍 Semantic Search & Ranking
Instead of just matching keywords, we use **Sentence-BERT (SBERT)** to understand meaning.
- *Example*: If the JD asks for "Backend Developer" and the resume says "Server-side Engineer", the AI knows they are a match.

### 3. 🏷️ Automated Domain Classification
The system automatically categorizes resumes into professional domains (e.g., "Data Science", "Web Development", "HR") using a classic ML classifier trained on thousands of resumes.

### 4. 📄 Professional PDF Reports
Generates a downloadable **Official Scorecard (PDF)** for every candidate, summarizing:
- Match Score
- Contact Information
- Extracted Skills
- Detected Domain

### 5. 🐳 Dockerized Deployment
Solves the "works on my machine" problem.
- **Backend (Python)**: Isolated environment avoids DLL/Version conflicts.
- **Frontend (React)**: Pre-configured Node.js environment.
- **One Command**: `docker-compose up --build` launches the entire stack.

---

## 🛠 Tech Stack
- **AI/NLP**: PyTorch, Transformers (BERT), Sentence-Transformers, Scikit-Learn.
- **Backend**: FastAPI, Uvicorn.
- **Frontend**: React (Vite), Lucide Icons, Modern CSS.
- **Data**: Pandas, NumPy.
- **Infrastructure**: Docker, Docker Compose.

---

## 🚀 How to Run

### Option 1: Docker (Recommended)
This approach guarantees access to the BERT Deep Learning features.
1. Install Docker Desktop.
2. Run:
   ```bash
   docker-compose up --build
   ```
3. Open `http://localhost:5173`

### Option 2: Local Python
1. Install Python 3.10+.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   run_project.bat
   ```
   (or `python main.py`)

---

## 📊 Training Your Own Model
You can retrain the internal models on your own data.
1. Place your dataset (JSON/CSV/Parquet) in `data/`.
2. Update `data/training_config.json`.
3. Run:
   ```bash
   python train_model.py
   ```
