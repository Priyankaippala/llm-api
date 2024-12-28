from flask import Blueprint, request, jsonify
from PyPDF2 import PdfReader
from app.services import generate_interview_questions

# Create a Blueprint for routes
api_bp = Blueprint("api", __name__)

def extract_text_from_pdf(pdf_file):
    """
    Extract text content from a PDF file.
    :param pdf_file: File object of the uploaded PDF
    :return: Extracted text as a string
    """
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")

@api_bp.route("/upload", methods=["POST"])
def upload():
    """
    Route to generate interview questions based on resume and job description.
    """
    try:
        if "file" not in request.files:
            return jsonify({"error": "Resume file is required."}), 400

        resume_file = request.files["file"]
        job_description = request.form.get("job_description")

        if not resume_file or not job_description:
            return jsonify({"error": "Resume file and job description are required."}), 400

        # Extract text from the uploaded resume file
        resume_summary = extract_text_from_pdf(resume_file)

        # Generate interview questions
        response = generate_interview_questions(resume_summary, job_description)
        
        return jsonify({"apiResponse": response}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
