import google.generativeai as genai
from app.config import Config

genai.configure(api_key=Config.GEMINI_API_KEY)

def generate_interview_questions(resume_summary, job_description):
    """
    Generates interview questions using the Gemini API.
    """
    try:
        prompt = f"Generate interview 10 questions based on the following resume and job description: resume : {resume_summary} Job Description: {job_description} Questions: JSON-like structure to represent the sections, subsections, and questions.Strictly stick to this format without any extra data/text in the response."
        
        # Use Gemini API to generate questions
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        # Return the generated questions or a fallback message
        return response.text.strip() if response.text else "No score generated."
    
    except Exception as e:
        raise RuntimeError(f"Error generating questions: {e}")
