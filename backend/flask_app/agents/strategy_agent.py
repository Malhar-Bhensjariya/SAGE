from flask_app.tools.gemini_connector import generate_response
from flask_app.core.utils.logger import log_info, log_error

class StrategyAgent:
    def __init__(self):
        log_info("StrategyAgent initialized.")

    def plan_next_steps(self, current_context, long_term_goals):
        """
        Generate strategic plans or next actions based on context and goals.

        Args:
            current_context (str): Summary of current progress or situation.
            long_term_goals (str): Description of long-term objectives.

        Returns:
            str: Suggested strategy or next steps.
        """
        try:
            prompt = self._build_prompt(current_context, long_term_goals)
            log_info(f"StrategyAgent prompt: {prompt}")

            response = generate_response(prompt)
            log_info("StrategyAgent received response.")
            return response.strip()

        except Exception as e:
            log_error(f"StrategyAgent error: {e}")
            return "Sorry, I couldn't formulate a strategy at the moment."

    def _build_prompt(self, current_context, long_term_goals):
        base_prompt = (
            "You are a strategic planner AI.\n"
            "Given the current context and long-term goals, "
            "suggest clear, prioritized next steps and strategies.\n\n"
            f"Current Context:\n{current_context}\n\n"
            f"Long-Term Goals:\n{long_term_goals}\n\n"
            "Provide a detailed, actionable plan."
        )
        return base_prompt
