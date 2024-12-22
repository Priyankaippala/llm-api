import google.generativeai as genai
from app.config import Config
# Configure the Gemini API
genai.configure(api_key=Config.GEMINI_API_KEY)

def generate_interview_questions(resume_summary, job_description):
    """
    Generates interview questions using the Gemini API.
    """
    try:
        # Format the prompt
        prompt = f"Generate 5 technical interview questions based on the following resume and job description: Resume Summary: {resume_summary} Job Description: {job_description} Questions: in text format"
        
        # Use Gemini API to generate questions
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        # Return the generated questions or a fallback message
        return response.text.strip() if response.text else "No questions generated."
    
    except Exception as e:
        raise RuntimeError(f"Error generating questions: {e}")
