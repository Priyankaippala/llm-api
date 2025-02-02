from flask import Blueprint, request, jsonify
from PyPDF2 import PdfReader
import speech_recognition as sr
from io import BytesIO
from app.services import generate_interview_questions

# Create a Blueprint for routes
api_bp = Blueprint("api", __name__)

def extract_text_from_pdf(pdf_file):
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
    try:
        if "file" not in request.files:
            return jsonify({"error": "Resume file is required."}), 400

        resume_file = request.files["file"]
        job_description = request.form.get("job_description")

        if not resume_file or not job_description:
            return jsonify({"error": "Resume file and job description are required."}), 400

        resume_summary = extract_text_from_pdf(resume_file)

        response = generate_interview_questions(resume_summary, job_description)
        
        return jsonify({"apiResponse": response}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/convert-speech", methods=["POST"])
def convert_speech_to_text():
    """
    Route to convert audio blob (speech) to text.
    """
    try:
        if "audio" not in request.files:
            return jsonify({"error": "Audio file is required."}), 400

        audio_file = request.files["audio"]

        recognizer = sr.Recognizer()

        audio_data = sr.AudioFile(audio_file)
        with audio_data as source:
            audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio)
            return jsonify({"text": text}), 200
        except sr.UnknownValueError:
            return jsonify({"error": "Could not understand the audio."}), 400
        except sr.RequestError as e:
            return jsonify({"error": f"Could not request results from Google Speech Recognition service; {e}"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500