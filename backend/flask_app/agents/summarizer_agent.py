from flask_app.tools.gemini_connector import generate_response
from flask_app.core.utils.logger import log_info, log_error

class SummarizerAgent:
    def __init__(self):
        log_info("SummarizerAgent initialized.")

    def summarize(self, text, max_length=500):
        """
        Summarize or clarify given text content.

        Args:
            text (str): Text to summarize.
            max_length (int): Max tokens or words in summary (approx).

        Returns:
            str: Summarized text.
        """
        try:
            prompt = self._build_prompt(text, max_length)
            log_info(f"SummarizerAgent prompt: {prompt[:100]}...")  # Log first 100 chars

            response = generate_response(prompt)
            log_info("SummarizerAgent received response.")
            return response.strip()

        except Exception as e:
            log_error(f"SummarizerAgent error: {e}")
            return "Sorry, I couldn't summarize the content at the moment."

    def _build_prompt(self, text, max_length):
        base_prompt = (
            "Please provide a clear, concise, and structured summary of the following text:\n\n"
            f"{text}\n\n"
            f"Limit the summary to approximately {max_length} words or tokens."
        )
        return base_prompt
