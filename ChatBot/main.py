from fastapi import FastAPI, HTTPException, Depends, Header
from dotenv import load_dotenv
import os
import google.generativeai as genai
import re

# Load environment variables
load_dotenv()

# Configure Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Define strict Constitution-related keywords
CONSTITUTION_KEYWORDS = [
    r"\bconstitution\b", r"\bfundamental rights\b", r"\bdirective principles\b",
    r"\bpreamble\b", r"\bpresident\b", r"\bparliament\b", r"\bsupreme court\b",
    r"\bfundamental duties\b", r"\barticle\b", r"\bschedule\b", r"\bamendment\b",
    r"\blaw\b", r"\bgovernance\b", r"\bcitizenship\b", r"\bjustice\b",
    r"\bdemocracy\b", r"\bsecularism\b", r"\bgovernment\b", r"\belections\b"
]

# Dummy API Key (Replace with a secure one)
VALID_API_KEY = "your_secure_api_key_here"

# FastAPI app
app = FastAPI(title="Samvidhan Sathi API")

def is_constitution_related(question: str) -> bool:
    """Check if question is strictly about the Indian Constitution."""
    question_lower = question.lower()
    return any(re.search(keyword, question_lower) for keyword in CONSTITUTION_KEYWORDS)

def get_response(question: str) -> str:
    """Fetch response from Gemini API if valid, else return restriction message."""
    if is_constitution_related(question):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(question)
            return response.text if response else "No response received."
        except Exception as e:
            return f"Error: {str(e)}"
    else:
        return "⚠️ This chatbot only answers **Constitution of India** related questions. Please ask a relevant question."

# API Route for chatbot
@app.post("/chatbot")
async def chatbot(question: str, api_key: str = Header(None)):
    """Chatbot API that responds only to Constitution-related queries."""
    
    # Validate API key
    if api_key != VALID_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")

    # Get chatbot response
    answer = get_response(question)
    
    return {"question": question, "answer": answer}

