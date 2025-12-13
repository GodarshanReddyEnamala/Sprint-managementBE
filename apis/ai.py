from fastapi import APIRouter
import google.generativeai as genai
import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")
genai.configure(api_key=os.getenv(api_key))


class PromptRequest(BaseModel):
    prompt: str


def send_task_to_gemini(request: PromptRequest):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(request.prompt)
    return {"result": response.text}
