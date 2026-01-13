# 🚀 ResumeAI: Precision Semantic Screening Engine

ResumeAI is a state-of-the-art recruitment tool that leverages **Natural Language Processing (NLP)** and **Machine Learning (ML)** to automate the screening, ranking, and analysis of resumes against job descriptions. It moves beyond simple keyword matching to understand the **semantic context** of a candidate's experience.

---

## 🛠 Tech Stack & Core Tools

### 1. **Backend Architecture**

- **FastAPI**: A high-performance Python web framework used to build our RESTful API. It handles file uploads, triggers the NLP pipeline, and serves the analysis results.
- **Uvicorn**: An ASGI web server implementation for Python, used to serve the FastAPI application.
- **Pydantic**: Used for data validation and settings management using Python type annotations.

### 2. **Artificial Intelligence & NLP**

- **Sentence-Transformers (SBERT)**:
  - **Model**: `all-MiniLM-L6-v2`
  - **Usage**: Converts entire resumes and job descriptions into high-dimensional vectors (embeddings). It calculates the **Cosine Similarity** between these vectors to provide a "Match Score" based on meaning, not just words.
- **Scikit-Learn**:
  - Used for the **Domain Classification** model which categorizes resumes (e.g., "Data Science", "Frontend Developer") based on trained patterns.
  - Also acts as a fallback for similarity scoring using **TF-IDF** if the neural models are unavailable.
- **Transformers (HuggingFace)**: The underlying engine for our deep learning models.

### 3. **Parsing & Extraction**

- **PDFMiner.six**: A robust tool for extracting text from PDF files while maintaining character encoding integrity.
- **Python-Docx**: Used to parse and read Microsoft Word (.docx) files.
- **Custom Regex Engine**: A sophisticated, multi-stage regular expression system used to extract:
  - **Contact Info**: Precise patterns for global email and phone formats.
  - **Skills**: A cross-referenced library of 100+ technical keywords.
  - **Experience**: Logic to calculate years of experience from various text formats.
  - **Education**: Heuristics to identify degrees and universities.

### 4. **Frontend Experience**

- **React (Vite)**: A fast, modern frontend framework.
- **Lucide-React**: Premium iconography for the "Intelligence Scan" aesthetic.
- **Vanilla CSS (Glassmorphism)**: A custom-designed UI featuring blurred backgrounds, vibrant gradients, and micro-animations for a high-end "Neural Engine" feel.

---

## 🧠 How It Works (The Pipeline)

### Step 1: Ingestion

The user uploads a resume (PDF/DOCX) and pastes a Job Description. The `parser.py` module detects the file type and converts the binary data into clean, searchable text.

### Step 2: Semantic Analysis

Instead of just counting words, the system sends the text through the **SBERT model**. This model understands that "Machine Learning Specialist" and "AI Engineer" are related concepts, even if the specific words don't match. This results in the **Matching Score**.

### Step 3: Entity Extraction

The `extractor.py` module runs the text through a series of "Scanners":

1.  **Skill Scanner**: Compares text against categorized tech stacks (Web, Cloud, Data, etc.).
2.  **Gap Analysis**: Identifies which skills requested in the Job Description are _missing_ from the resume.
3.  **Detail Scanner**: Finds the candidate's email, phone, and estimated years of experience.

### Step 4: Classification

The extracted text is sent to a pre-trained **ML Classifier**. This confirms the candidate's primary domain (e.g., "Software Engineer") and verifies if they are applying for a job that fits their actual background.

### Step 5: Reporting

The `reporter.py` module takes all these data points and creates a professional **PDF Report** using `fpdf2`, which the recruiter can download and share.

---

## 📈 Optimization for Deployment (Render Core)

To run this complex "heavy" engine on free-tier servers (512MB RAM), we implemented several optimizations:

- **Dockerized Environment**: Using `python:3.11-slim` to reduce the image size by 60%.
- **Memory Pruning**: Removed heavy libraries like `SpaCy` and `GLiNER` in favor of high-performance custom regex, saving ~300MB of RAM.
- **Model Caching**: The SBERT model is downloaded _during_ the Docker build phase, so the app starts instantly without needing to fetch 100MB+ from the internet on every boot.
- **Dynamic Port Binding**: Configured to respect the `$PORT` environment variable required by cloud hosting providers.

---

## 🚀 Future Roadmap

- **LLM Integration**: Replacing the keyword gap analysis with a local Llama model for even deeper "Reasoning" on candidate fit.
- **Knowledge Graph**: Building a graph database of skills to understand career progression (e.g., knowing that a "Junior Developer" often becomes a "Senior Developer").
- **Multi-Resume Upload**: Batch processing of hundreds of resumes at once with a leaderboard view.
