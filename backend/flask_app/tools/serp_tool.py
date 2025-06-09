from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from flask_app.tools.serpapi_connector import search_google

class SerpInput(BaseModel):
    query: str = Field(..., description="Search query for Google")
    num_results: int = Field(5, description="Number of results to return")

class SerpTool(BaseTool):
    name = "SerpAPI"
    description = "Performs Google searches using SerpAPI"
    args_schema = SerpInput

    def _run(self, query: str, num_results: int = 5) -> list:
        return search_google(query, num_results)