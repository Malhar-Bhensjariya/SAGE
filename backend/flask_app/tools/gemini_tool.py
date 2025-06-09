from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from flask_app.tools.gemini_connector import generate_response

class GeminiInput(BaseModel):
    prompt: str = Field(..., description="The input prompt for Gemini")

class GeminiTool(BaseTool):
    name = "Gemini"
    description = "Generates text responses using Google's Gemini model"
    args_schema = GeminiInput

    def _run(self, prompt: str) -> str:
        return generate_response(prompt)