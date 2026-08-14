# DareQuizo

🚀 **Multimodal Generative AI for Taxonomy-Based Assessment and Interactive Learning**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework Flask](https://img.shields.io/badge/Framework-Flask-red.svg)](https://flask.palletsprojects.com/)
[![Database PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue.svg)](https://www.postgresql.org/)
[![Model LLaMA 3.1 8B](https://img.shields.io/badge/LLM-LLaMA%203.1%20(8B)-purple.svg)](https://groq.com/)

---

## 📋 Executive Summary

Assessments are a cornerstone of modern educational evaluation, providing critical feedback to measure student progress and identify conceptual gaps. However, the manual generation of high-quality assessment items remains a tedious, resource-intensive process that demands substantial subject-matter expertise and pedagogical consideration. While automated question generation (AQG) systems have evolved from rule-based pipelines to transformer-based Large Language Models (LLMs), existing solutions are often limited by plain-text inputs, a lack of alignment with cognitive hierarchies, and the absence of real-time interactive scaffolds for self-directed learners.

**DareQuizo** is an open-source, full-stack research platform designed to bridge these gaps. The system integrates multi-format document parsers with a low-latency LLM inference pipeline, enabling the automated synthesis of diverse question sets directly from scanned notes, documents, PDFs, or raw text. By engineering zero-shot prompts mapped to Bloom's Taxonomy and specific national examination models (e.g., GATE, NET, UPSC), DareQuizo calibrates assessment depth to target distinct cognitive levels. 

To support real-time learner scaffolding, the platform incorporates browser-side text-to-speech rendering, client-side translation widgets, and an AJAX-based conversational chatbot. This design provides contextual, inline feedback during self-assessment, presenting a cohesive architecture for automated, personalized, and interactive evaluations.

### Key Capabilities
*   **Multimodal Input Processing**: Standardized ingestion of text files, layout-dense PDFs, Microsoft Word documents, and images via Optical Character Recognition (OCR).
*   **Pedagogical Calibration**: Zero-shot prompt templates aligned with the six levels of Bloom's Taxonomy and competitive examination structures (GATE, NET, UPSC).
*   **Adaptive Backend Heuristics**: Session-based difficulty adjustment based on student performance thresholds.
*   **Interactive Doubt Scaffolding**: Inline English-to-Hindi translation, SpeechSynthesis audio readout, and a context-aware chat client for real-time explanations.
*   **Document Export Utilities**: Automated generation and download of customized question banks in PDF, DOCX, and TXT formats.

---

## ✨ Key Features

| Feature Category | Specific Capabilities | Code / Technical Implementation |
| :--- | :--- | :--- |
| **Multimodal Ingestion** | Ingestion of raw text, PDF documents, DOCX files, and scanned notes/images. | Processes file buffers using `PyPDF2` (`PdfReader`), `python-docx` (`Document`), and `pytesseract` (OCR). |
| **Question Generation** | Renders 8 distinct formats: MCQs, Fill-in-the-Blanks, True/False, Assertion/Reason, Case Study, One Word, Short Answer, and Long Answer. | Prompt engineering formats LLM outputs using regular expression parser boundaries. |
| **Pedagogical Alignment** | Maps questions across the six stages of Bloom's Taxonomy (Remembering, Understanding, Applying, Analyzing, Evaluating, Creating). | Constructs dynamic prompt rules matching selected cognitive tiers. |
| **Adaptive Difficulty** | Backend recalibration of target question parameters (Easy, Medium, Hard) based on previous scoring handshakes. | Inline evaluation comparing user correct count against session totals: `score > 0.7 * count` (Hard), `score < 0.4 * count` (Easy). |
| **Interactive Scaffolding** | Floating chatbot, speech playback, English $\leftrightarrow$ Hindi translation, and simple Hindi explanations. | Lightweight AJAX fetch calls to `/chat` using LLaMA 3.1; client-side browser `SpeechSynthesisUtterance`. |
| **Export Formats** | Generates assessment documents for offline use. | Compiles document streams dynamically using ReportLab (PDF), python-docx (DOCX), and raw string writes (TXT). |
| **User Persistence** | Registration, login authorization, and historical quiz archiving. | Direct PostgreSQL queries via `psycopg2` with session authorization tags. |

---

## 🏗️ System Architecture

```mermaid
graph TD
    Client[Browser Frontend: HTML5/CSS3/Bootstrap 5/JS]
    Server[Flask Backend: Python 3.13]
    DB[(PostgreSQL Database)]
    OCR[Local Tesseract OCR Engine]
    LLM[Groq Inference Engine: llama-3.1-8b-instant]
    
    Client -- 1. Form Configuration & File Buffers --> Server
    Server -- 2. Parse PDF / DOCX --> Server
    Server -- 3. Image OCR Extraction --> OCR
    OCR -- 4. Raw Text Response --> Server
    Server -- 5. Compile Zero-shot Prompts --> LLM
    LLM -- 6. Structured Generation Output --> Server
    Server -- 7. Save Quiz Session --> DB
    Server -- 8. Render Assessment Layout --> Client
    
    Client -- 9. Asynchronous Chat & translation (AJAX fetch) --> Server
    Server -- 10. Query LLaMA 3.1 Contextually --> LLM
    Client -- 11. Read Aloud (Web Speech API) --> Client
```

### Component Descriptions
1.  **Frontend Layout**: A responsive single-page web dashboard built with Bootstrap 5. It manages quiz session states, tracks score metrics, translates questions client-side, and renders a floating chat widget.
2.  **Backend Controller**: A Flask routing application in `app.py` that processes files, organizes dynamic prompt templates, executes psycopg2 database transactions, and manages session variables.
3.  **Ingestion & Parsing Pipeline**: Standardizes input streams. PDF parsing extracts text by iterating pages; Word parsing loops paragraph items; and images are processed using pytesseract to extract textual characters. Text is normalized and truncated to 6,000 characters to prevent prompt overflow.
4.  **Generative Inference Pipeline**: Routes prompts to Groq's high-throughput API using `llama-3.1-8b-instant` to generate assessments and chatbot responses.
5.  **Database Storage**: A PostgreSQL instance storing user accounts and historical question logs using raw SQL connections.

---

## 🛠️ Technical Stack

| Layer | Component / Tool | Purpose |
| :--- | :--- | :--- |
| **Backend Framework** | Flask (Python 3.13) | RESTful API routing, session management, and template rendering |
| **Inference Engine** | Groq API (`llama-3.1-8b-instant`) | Low-latency question generation, translation, and chat reasoning |
| **Database** | PostgreSQL | Persistent storage of user data and historical generations |
| **Connection Driver** | `psycopg2-binary` | Low-level database connection pooling and raw SQL execution |
| **PDF Parser** | `PyPDF2` (`PdfReader`) | Text extraction from PDF documents |
| **DOCX Parser** | `python-docx` | Text extraction from Microsoft Word documents and export creation |
| **OCR Processor** | `pytesseract` + `Pillow` (PIL) | Optical Character Recognition for scanned images |
| **PDF Compilation** | `reportlab` | Programmatic layout generation for PDF exports |
| **Frontend Styling** | Bootstrap 5 + Vanilla CSS3 | Responsive interface styling and dual-theme configurations |
| **Frontend Logic** | Vanilla JavaScript | UI updates, timed quiz loops, AJAX calls, and SpeechSynthesis |
| **Production Server** | `gunicorn` | WSGI HTTP Server for production deployment |

---

## 🚀 Installation & Setup

### Prerequisites
*   **Python 3.10+**: Ensure Python is installed locally.
*   **PostgreSQL**: A running instance with access credentials.
*   **Tesseract OCR**: Install the binary on your host machine.
    *   *Windows*: Download the installer and add its path to your system's environment variables (e.g., `C:\Program Files\Tesseract-OCR`).
    *   *Ubuntu/Debian*: `sudo apt-get install tesseract-ocr`
    *   *macOS*: `brew install tesseract`

### 1. Clone the Repository
```bash
git clone https://github.com/username/DareQuizo.git
cd DareQuizo
```

### 2. Set Up a Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
GROQ_API_KEY="your_groq_api_key_here"
DATABASE_URL="postgresql://username:password@localhost:5432/darequizo_db"
SECRET_KEY="your_flask_session_secret_key"
```

### 5. Initialize the Database
Ensure PostgreSQL is running and the database matches your `DATABASE_URL`. Run the application once to automatically trigger table creation:
```bash
python app.py
```
*Note: The application checks for tables at startup and automatically creates `users` and `history` if they are missing.*

---

## 🗄️ Database Schema

DareQuizo uses a direct relational database connection handled through `psycopg2`. The database tables are structured as follows:

### 1. Users Table
```sql
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    full_name TEXT,
    email TEXT,
    username TEXT UNIQUE,
    password TEXT -- Hashed using werkzeug.security
);
```

### 2. History Table
```sql
CREATE TABLE IF NOT EXISTS history (
    id SERIAL PRIMARY KEY,
    username TEXT,
    topic TEXT,
    difficulty TEXT, -- Stores difficulty and Bloom's level configurations
    question_type TEXT,
    mode TEXT,
    generated_content TEXT, -- Contains the raw question set text
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔌 API Reference

### 1. Core Endpoints

#### `GET /`
Renders the main dashboard (`index.html`).

#### `POST /index`
Main controller route for question generation.
*   **Form Data Parameters**:
    *   `topic` (string, optional): Topic keyword search fallback.
    *   `difficulty` (string, required): Difficulty tier or Bloom's Taxonomy level.
    *   `question_type` (string, required): Assessment layout selection (e.g., MCQs, Mixed).
    *   `count` (integer, optional): Number of questions to generate (default: 5).
    *   `mode` (string, optional): Operates in `"practice"` (renders answers inline) or `"quiz"` (interactive timer).
    *   `score` (integer, optional): Previous score passed to activate adaptive difficulty.
    *   `pdf_file` / `docx_file` / `txt_file` / `image_file` (file buffers, optional): Source files for parsing.
*   **Response**: Renders `PracticeMode.html` or `result.html` based on the selected mode.

---

### 2. Interactive Features API

#### `POST /chat`
Asynchronous route handling doubts chat, Hindi explanations, and language translations.
*   **Request Payload (JSON)**:
    ```json
    {
      "message": "Translate this to Hindi",
      "context": "Q1) What is a router?\nA) Device\nB) Wire",
      "lang": "hi"
    }
    ```
*   **JSON Response**:
    ```json
    {
      "reply": "Q1) राउटर क्या है?\nA) डिवाइस\nB) वायर",
      "sources": ["Uploaded PDF File"]
    }
    ```
*   **Internal Routing Logic**:
    *   If `message` contains `"translate"`: Triggers a zero-shot translation prompt to convert text to pure Hindi (Devanagari script) or English.
    *   If `lang` is `"hi"`: Generates simple educational explanations in Hindi.
    *   Else: Explains the correct option, why other choices are wrong, and provides a concept summary in English.

---

### 3. Export API

#### `POST /export/<format>`
Compiles and downloads the active question bank.
*   **URL Parameter**: `<format>` can be `pdf`, `docx`, or `txt`.
*   **Form Data Parameter**:
    *   `mcqs` (string, required): Plain text representing the generated questions.
*   **Response**: File attachment stream containing the compiled assessment document.

---

## 📖 Usage Guide

### Generating Questions
1.  **Select Ingestion Modality**: Enter a topic keyword or upload a file (PDF, DOCX, TXT, or Image).
2.  **Configure Assessment Depth**: Select a difficulty tier (e.g., Easy, Hard), a competitive exam level (e.g., GATE, NET, UPSC), or a Bloom's Taxonomy cognitive level (e.g., Remembering, Evaluating) from the dropdown list.
3.  **Choose Layout**: Set the target question format (e.g., MCQs, True/False, Case Study, or Mixed) and count.
4.  **Generate**: Click "Generate Questions" to render the quiz.

### Interactive Self-Assessment
1.  **Quiz Mode**: Click "Quiz Mode" to start. The interface displays a timer, score trackers, and dynamic XP calculations.
2.  **TTS Readout**: Click the speaker icon to read a question stem aloud in English or Hindi.
3.  **Local Translation**: Use the translation button to toggle questions between English and Devanagari Hindi.
4.  **Ask Doubts**: Type a query into the floating chat widget to get step-by-step explanations of correct and incorrect answers from the active context.

---

## ⚠️ Implementation Limitations & Future Scope

### Current Technical Boundaries
*   **6,000-Character Constraint**: Input documents are truncated to 6,000 characters to prevent prompt context window limitations during inference.
*   **Local OCR Configuration**: Image ingestion depends on the host machine's local `tesseract-ocr` installation, which is sensitive to image resolution and font formats.
*   **Transient Gamification Metrics**: XP points, level progression, and weak area tracking are calculated dynamically in frontend JavaScript and are not persistently stored in the database.
*   **Manual Adaptive Handshake**: The backend implements scoring boundaries for difficulty adjustments, but automatic loop integration depends on subsequent frontend parameter integrations.
*   **Zero-Shot Output Dependencies**: There is no secondary automated validation agent; the linguistic and pedagogical quality of generated questions depends on the zero-shot performance of the LLaMA 3.1 model.

### Future Work
1.  **Whisper Ingestion Pipeline**: Integrating Whisper API to transcribe audio and video files in the backend, adding audio and video file support to the future scope.
2.  **Persistent Leaderboards**: Extending the database schema to store scoring history and global student ranks.
3.  **Dual-Agent Verification**: Implementing a self-correcting validation wrapper where a second LLM agent evaluates questions for ambiguity and distractor accuracy before rendering.
4.  **Empirical User Studies**: Conducting randomized trials with student cohorts to evaluate the platform's impact on learning outcomes and exam preparation.

---

## 🎓 Associated Research

This project forms the basis of the following manuscript:

> **Title**: *DareQuizo: A Multimodal Generative AI Platform for Taxonomy-Based Assessment and Interactive Learning*  
> **Authors**: *Anamika , Muskan Dewangan, Kashifa Fatima*  
> **Status**: *Prepared for Submission*

---

