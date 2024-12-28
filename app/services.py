import google.generativeai as genai
from app.config import Config

genai.configure(api_key=Config.GEMINI_API_KEY)

def generate_interview_questions(resume_summary, job_description):
    """
    Generates interview questions using the Gemini API.
    """
    try:
        # Format the prompt
        prompt = f"Generate interview questions based on the following resume and job description: Job Description: {job_description} Questions: in text format"
        
        # Use Gemini API to generate questions
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        # Return the generated questions or a fallback message
        return response.text.strip() if response.text else "No score generated."
    
    except Exception as e:
        raise RuntimeError(f"Error generating questions: {e}")
