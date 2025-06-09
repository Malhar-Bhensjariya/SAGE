from flask_app.tools.gemini_connector import generate_response
from flask_app.core.utils.logger import log_info, log_error

class CritiqueAgent:
    def __init__(self, threshold=0.8):
        """
        Args:
            threshold (float): Minimum score (0 to 1) required to pass critique.
        """
        self.threshold = threshold
        log_info(f"CritiqueAgent initialized with threshold={self.threshold}")

    def perform_critique(self, content, goal, context=None):
        """
        Critique content and evaluate how well it meets the goal.

        Args:
            content (str): Text/content to critique.
            goal (str): The goal or requirement the content should satisfy.
            context (str, optional): Additional context.

        Returns:
            dict: {
                "score": float (0-1),
                "passed": bool,
                "critique_text": str
            }
        """
        # Quick sanity check to avoid unnecessary calls
        if not content.strip():
            return {
                "score": 0.0,
                "passed": False,
                "critique_text": "Empty content; critique failed immediately."
            }

        try:
            prompt = self._build_prompt(content, goal, context)
            log_info(f"CritiqueAgent prompt: {prompt}")

            response = generate_response(prompt)
            log_info("CritiqueAgent received response.")

            score, critique_text = self._parse_response(response)

            passed = score >= self.threshold
            return {
                "score": score,
                "passed": passed,
                "critique_text": critique_text.strip()
            }

        except Exception as e:
            log_error(f"CritiqueAgent error: {e}")
            return {
                "score": 0,
                "passed": False,
                "critique_text": "Sorry, critique failed due to an error."
            }

    def _build_prompt(self, content, goal, context):
        base_prompt = (
            "You are an expert evaluator. Analyze the following content and score how well it satisfies the goal. "
            "Score on a scale from 0 (does not satisfy) to 1 (fully satisfies).\n\n"
            f"Goal:\n{goal}\n\n"
            f"Content:\n{content}\n"
        )
        if context:
            base_prompt += f"Additional context:\n{context}\n"
        base_prompt += (
            "Provide a numeric score between 0 and 1 on the first line, then a detailed critique explaining your reasoning."
        )
        return base_prompt

    def _parse_response(self, response):
        """
        Parse Gemini response expecting a score and critique.

        Args:
            response (str): Text response from Gemini.

        Returns:
            tuple: (score: float, critique_text: str)
        """
        lines = response.strip().split('\n', 1)
        try:
            score_line = lines[0].strip()
            score = float(score_line)
            # Clamp score between 0 and 1 to avoid weird AI output issues
            if score < 0 or score > 1:
                score = 0.0
        except Exception:
            score = 0.0

        critique_text = lines[1] if len(lines) > 1 else "No detailed critique provided."
        return score, critique_text
