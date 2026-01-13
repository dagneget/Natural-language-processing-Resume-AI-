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

## 📂 Project Directory Structure

### 🏗 **Root Directory**

- `server.py`: The heart of the application. It hosts the FastAPI endpoints, manages CORS, and orchestrates the analysis flow.
- `main.py`: The Command Line Interface (CLI) version of the tool for batch processing resumes without the UI.
- `Dockerfile`: Contains the blueprints for building the production container, optimized for minimal memory usage.
- `docker-compose.yml`: Used for local development to spin up both the backend and frontend in a single command.
- `requirements.txt`: Lists all Python dependencies required for the NLP engine.
- `train_model.py`: Utility script used to train the Scikit-Learn domain classification model.

### 🧠 **`src/` (Core Logic)**

- `parser.py`: Handles file ingestion. It contains logic to strip text from **PDF** and **DOCX** files while maintaining text purity.
- `extractor.py`: The "Smart Scanner." Contains the regex logic and keyword maps for identifying skills, education, and contact details.
- `screener.py`: The "Brain." Implements the SBERT neural embedding logic and the cosine similarity math for ranking.
- `reporter.py`: The "Writer." Uses `fpdf2` to generate the stylized deep-analysis PDF reports.
- `classifier.py`: Manages the loading and execution of the ML model for domain categorization.

### 🎨 **`ui/` (Frontend)**

- `ui/src/App.jsx`: The main React component. Manages the state of uploads, the analysis spinner, and result rendering.
- `ui/src/index.css`: The "Premium Shield." Contains the glassmorphism design system and animation keyframes.
- `ui/dist/`: (Created after build) Contains the optimized static code served to the user's browser.

### 📁 **Data & Temp Folders**

- `uploads/`: A secure temporary landing zone for resumes as they are being processed.
- `reports/`: Storage for generated PDF scorecards before they are served to the recruiter.
- `models/`: Stores the serialized `.pkl` or weights for the domain classification models.
- `data/`: Contains sample resumes or datasets used for testing and training.

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

## � Dataset & Knowledge Base

The accuracy of ResumeAI is built upon multiple high-quality datasets used for training our Machine Learning models:

### 1. **Resume Classification Dataset**

- **Source**: `UpdatedResumeDataSet.csv` (Commonly sourced from Kaggle's "Resume Dataset").
- **Size**: ~962 unique resumes.
- **Categories**: 25 distinct job domains including Data Science, HR, Advocate, Arts, Web Designing, Mechanical Engineering, Sales, Health and Fitness, Civil Engineering, and more.
- **Purpose**: This dataset trains the `SGDClassifier` to recognize the linguistic patterns unique to each profession, allowing the app to automatically detect the "Category" of an uploaded resume.

### 2. **NER (Skill Extraction) Dataset**

- **Source**: `sonchuate/resume_ner` (Hugging Face).
- **Type**: Annotated Named Entity Recognition (NER) data.
- **Usage**: Used to train the model to distinguish between a "Skill" (e.g., Python), an "Organization" (e.g., Google), and a "Job Title".
- **Logic**: Our `train_model.py` script tokenizes this data into hundreds of thousands of individual words (tokens) and trains a model to predict the probability that a specific word represents a technical competency.

### 3. **Semantic Embedding Weights**

- **Source**: Sentence-Transformers / Hugging Face.
- **Model**: `all-MiniLM-L6-v2`.
- **Context**: This model was pre-trained on a diverse corpus of over 1 billion sentence pairs. We utilize these pre-trained "weights" to perform the vector math (embeddings) that powers our **Semantic Score**.

---

## �🚀 Future Roadmap

- **LLM Integration**: Replacing the keyword gap analysis with a local Llama model for even deeper "Reasoning" on candidate fit.
- **Knowledge Graph**: Building a graph database of skills to understand career progression (e.g., knowing that a "Junior Developer" often becomes a "Senior Developer").
- **Multi-Resume Upload**: Batch processing of hundreds of resumes at once with a leaderboard view.
