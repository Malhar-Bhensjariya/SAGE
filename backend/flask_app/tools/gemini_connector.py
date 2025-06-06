import os
import google.generativeai as genai
from flask_app.core.utils.logger import log
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini with your API key
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("models/gemini-2.0-flash")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192
}

def generate_response(prompt: str) -> str:
    """
    Send a prompt to Gemini and return the raw text response.
    """
    try:
        chat = model.start_chat(history=[])
        response = chat.send_message(prompt, generation_config=generation_config)
        return response.text

    except Exception as e:
        log(f"Gemini error: {e}", level="ERROR")
        return "Sorry, failed to generate a response."
