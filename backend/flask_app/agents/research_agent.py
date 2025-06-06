from flask_app.tools.gemini_connector import generate_response
from flask_app.tools.serpapi_connector import fetch_search_results
from flask_app.core.utils.logger import log_info, log_error

class ResearchAgent:
    def __init__(self, use_web_search=False):
        """
        Args:
            use_web_search (bool): Enable SERPAPI usage for live web data.
        """
        self.use_web_search = use_web_search
        log_info(f"ResearchAgent initialized with use_web_search={self.use_web_search}")

    def perform_research(self, query, context=None):
        """
        Research using live web search (SERPAPI) + Gemini AI as fallback/refinement.

        Args:
            query (str): Research topic or question.
            context (str, optional): Additional context.

        Returns:
            str: Research output.
        """
        try:
            web_results = ""
            if self.use_web_search:
                log_info(f"Performing web search for query: {query}")
                search_data = fetch_search_results(query)
                web_results = self._format_web_results(search_data)
                log_info("Web search completed.")

            prompt = self._build_prompt(query, context, web_results)
            log_info(f"ResearchAgent prompt: {prompt}")

            response = generate_response(prompt)
            log_info("ResearchAgent received response.")
            return response.strip()

        except Exception as e:
            log_error(f"ResearchAgent error: {e}")
            return "Sorry, I couldn't fetch research data at the moment."

    def _format_web_results(self, search_data):
        """
        Convert raw SERPAPI search data into text summary to guide Gemini.

        Args:
            search_data (dict): SERPAPI JSON response.

        Returns:
            str: Text summary of web results.
        """
        if not search_data or "organic_results" not in search_data:
            return ""

        snippets = []
        for result in search_data["organic_results"][:5]:  # limit to top 5
            title = result.get("title", "")
            snippet = result.get("snippet", "")
            link = result.get("link", "")
            snippets.append(f"{title}: {snippet} ({link})")

        return "\n".join(snippets)

    def _build_prompt(self, query, context, web_results):
        """
        Build Gemini prompt including web search data if available.

        Args:
            query (str): Research question.
            context (str or None): Additional context.
            web_results (str): Summarized web search snippets.

        Returns:
            str: Full prompt string.
        """
        base_prompt = f"Research thoroughly on the following topic:\n{query}\n"
        if context:
            base_prompt += f"Use this context to refine your research:\n{context}\n"
        if web_results:
            base_prompt += f"Also consider these recent web search results:\n{web_results}\n"
        base_prompt += "Provide detailed, accurate, and well-structured information."

        return base_prompt
