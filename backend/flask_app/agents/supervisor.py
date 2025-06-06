# flask_app/agents/supervisor_agent.py

from flask_app.core.services.planning_service import PlanningService
from flask_app.core.services.agent_service import AgentService
from flask_app.core.utils.logger import log_info, log_error

class SupervisorAgent:
    def __init__(self, use_web_search=False):
        self.agent_service = AgentService(use_web_search=use_web_search)
        self.planning_service = PlanningService()
        log_info("SupervisorAgent initialized.")

    def _is_trivial_input(self, query):
        # Basic filter: short greetings or empty queries don't need critique
        trivial_phrases = {"hi", "hello", "hey", "", "thanks", "thank you"}
        return query.strip().lower() in trivial_phrases or len(query.strip()) < 5

    def manage_task(self, task_id, data):
        log_info(f"SupervisorAgent managing task: {task_id}")

        try:
            query = data.get("query", "")
            goals = data.get("goals", [])
            context = data.get("context", None)
            threshold = data.get("critique_threshold", 0.8)  # Use float between 0-1

            # Step 1: Plan
            plan = self.planning_service.create_plan(query, goals)
            log_info(f"Plan created: {plan}")

            # Step 2: Research
            research_result = self.agent_service.perform_research(query, context)
            log_info("Research completed.")

            # Step 3: Summarize
            summary = self.agent_service.summarize(research_result)
            log_info("Summarization completed.")

            # Step 4: Critique - skip if trivial input
            if self._is_trivial_input(query):
                log_info("Trivial input detected, skipping critique.")
                critique_result = {"score": 1.0, "passed": True, "critique_text": "Skipped critique for trivial input."}
            else:
                critique_result = self.agent_service.critique(summary, goals, threshold)
                log_info(f"Critique completed: Passed={critique_result['passed']}")

            if not critique_result["passed"]:
                log_info("Critique failed, returning feedback.")
                return {
                    "plan": plan,
                    "research": research_result,
                    "summary": summary,
                    "critique": critique_result,
                    "strategy": None,
                    "message": "Output did not meet quality threshold."
                }

            # Step 5: Strategy formulation
            strategy = self.agent_service.strategize(summary, goals)
            log_info("Strategy formulation completed.")

            return {
                "plan": plan,
                "research": research_result,
                "summary": summary,
                "critique": critique_result,
                "strategy": strategy,
                "message": "Task completed successfully."
            }

        except Exception as e:
            log_error(f"SupervisorAgent error for task {task_id}: {e}")
            return {
                "error": f"SupervisorAgent failed: {e}"
            }
