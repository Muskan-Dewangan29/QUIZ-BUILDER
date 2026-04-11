from flask import Flask, render_template, request
from dotenv import load_dotenv
from groq import Groq
import os
from PyPDF2 import PdfReader
from docx import Document
import pytesseract
from PIL import Image
import tempfile

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = Flask(__name__)

# ✅ If you are on Windows, uncomment and set this path:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"




@app.route("/", methods=["GET", "POST"])
def index():
    mcqs = ""

    if request.method == "POST":
        difficulty = request.form.get("difficulty")
        count = request.form.get("count")
        count = int(count) if count else 5

        topic = request.form.get("topic", "").strip()

        pdf_file = request.files.get("pdf_file")
        txt_file = request.files.get("txt_file")
        docx_file = request.files.get("docx_file")
        image_file = request.files.get("image_file")
        audio_file = request.files.get("audio_file")
        video_file = request.files.get("video_file")

        extracted_text = ""
        source_used = "Topic"

        # ✅ TXT
        if txt_file and txt_file.filename != "":
            extracted_text = txt_file.read().decode("utf-8", errors="ignore")
            source_used = "TXT File"

        # ✅ PDF
        elif pdf_file and pdf_file.filename != "":
            reader = PdfReader(pdf_file)
            pdf_text = ""
            for page in reader.pages:
                pdf_text += (page.extract_text() or "") + "\n"
            extracted_text = pdf_text
            source_used = "PDF File"

        # ✅ DOCX
        elif docx_file and docx_file.filename != "":
            doc = Document(docx_file)
            extracted_text = "\n".join([p.text for p in doc.paragraphs])

        # ✅ IMAGE (OCR)
        elif image_file and image_file.filename != "":
            img = Image.open(image_file).convert("RGB")
            extracted_text = pytesseract.image_to_string(img, lang="eng")
            source_used = "Image (OCR)"


        

        # ✅ LIMIT extracted text (prevents 413 error)
        extracted_text = extracted_text.strip()[:6000]
        # ✅ Map level to detailed instruction
        level_instruction = ""

        if difficulty:
            level_instruction = f"""
            The MCQs must strictly follow this exam level: {difficulty}

            - If GATE: Focus on conceptual, numerical, and application-based questions.
            - If NET: Include theoretical, conceptual, and research-oriented questions.
            - If UPSC/CGPSC: Focus on factual + analytical + current-affairs style.
            - If Bloom's Taxonomy:
                * Remembering: Direct facts
                * Understanding: Concept clarity
                * Applying: Problem-solving
                * Analyzing: Comparison & reasoning
                * Evaluating: Judgement-based
                * Creating: Scenario-based
            - Maintain the exact tone and difficulty of the selected level.
            """
        # ✅ Build prompt
        if extracted_text:
            prompt = f"""
        You are an expert exam question setter.

        Task:
        Generate exactly {count} high-quality MCQs from the given text.

        {level_instruction}

        Rules:
        1. Output format MUST be:
        Q1) ...
        A) ...
        B) ...
        C) ...
        D) ...
        Answer: <A/B/C/D>
        Explanation: <1 line>

        2. Questions must be from the text only.
        3. Do not repeat questions.
        4. Do not add extra commentary.

        TEXT:
        {extracted_text}
        """
        else:
            prompt = f"""
        You are an expert exam question setter.

        Generate exactly {count} MCQs on this topic: {topic}
        {level_instruction}

        Format:
        Q1) ...
        A) ...
        B) ...
        C) ...
        D) ...
        Answer: <A/B/C/D>
        Explanation: <1 line>
        """


        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        mcqs = response.choices[0].message.content
        mcqs = f"Source Used: {source_used}\n\n" + mcqs

    return render_template("index.html", mcqs=mcqs)

from flask import jsonify

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    user_message = data.get("message")
    context = data.get("context")

    prompt = f"""
You are a helpful teacher.

Context:
{context}

Student Question:
{user_message}

Explain clearly in simple terms.
Also explain why the correct answer is right and others are wrong.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    reply = response.choices[0].message.content

    # ✅ Add basic sources (you can improve later)
    sources = []

    # If context came from MCQs (file-based)
    if context:
        if "PDF File" in context:
            sources.append("Uploaded PDF File")
        elif "TXT File" in context:
            sources.append("Uploaded TXT File")
        elif "Image (OCR)" in context:
            sources.append("Extracted from Image (OCR)")
        else:
            sources.append("Generated from provided content")

    # Optional fallback (for topic-based answers)
    if not sources:
        sources = [
            "https://en.wikipedia.org/",
            "https://www.geeksforgeeks.org/"
        ]

    return jsonify({
        "reply": reply,
        "sources": sources
    })
if __name__ == "__main__":
    app.run(debug=True)
