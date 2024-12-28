from flask import Blueprint, request, jsonify
from app.services import generate_interview_questions

# Create a Blueprint for routes
api_bp = Blueprint("api", __name__)

@api_bp.route("/upload", methods=["POST"])
def upload():
    """
    Route to generate interview questions based on resume and job description.
    """
    try:

        data = request.get_json()
        resume_summary = data.get("resume_summary")
        job_description = data.get("job_description")

        if not resume_summary or not job_description:
            return jsonify({"error": "Resume summary and job description are required."}), 400

        response = generate_interview_questions(resume_summary, job_description)
        
        return jsonify({"apiResponse": response}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
