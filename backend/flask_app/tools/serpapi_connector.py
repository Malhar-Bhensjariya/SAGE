import os
import requests
from dotenv import load_dotenv
from flask_app.core.utils.logger import log

load_dotenv()

SERP_API_KEY = os.getenv("SERP_API_KEY")
SERP_URL = "https://serpapi.com/search"

def search_google(query: str, num_results: int = 5) -> list:
    """
    Fetches search results from SerpAPI (Google Search).
    """
    try:
        params = {
            "q": query,
            "api_key": SERP_API_KEY,
            "num": num_results,
            "engine": "google"
        }
        response = requests.get(SERP_URL, params=params)
        results = response.json().get("organic_results", [])

        links = [{
            "title": r.get("title"),
            "link": r.get("link"),
            "snippet": r.get("snippet")
        } for r in results[:num_results]]

        return links
    except Exception as e:
        log(f"SerpAPI error: {e}", level="ERROR")
        return []
