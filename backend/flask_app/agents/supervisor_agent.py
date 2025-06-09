from flask_app.core.services.agent_service import AgentService
from flask_app.core.services.planning_service import PlanningService
from flask_app.core.utils.logger import log_info, log_error

class SupervisorAgent:
    def __init__(self, use_web_search=False):
        self.agent_service = AgentService(use_web_search)
        self.planning_service = PlanningService()
        self.research_agent = self.agent_service.create_agent("research")
        self.summarize_agent = self.agent_service.create_agent("summarize")
        self.critique_agent = self.agent_service.create_agent("critique")
        self.strategy_agent = self.agent_service.create_agent("strategy")
        log_info("SupervisorAgent initialized with LangChain agents")

    def _needs_summarization(self, content: str) -> bool:
        """Determine if content needs summarization"""
        if len(content.split()) < 300:  # Don't summarize short content
            return False
        return True

    def _needs_critique(self, content: str, goal: str) -> bool:
        """Determine if content needs critique"""
        trivial_keywords = ["status", "update", "progress"]
        if any(kw in goal.lower() for kw in trivial_keywords):
            return False
        return True

    def manage_task(self, task_id, data):
        log_info(f"SupervisorAgent managing task: {task_id}")
        try:
            query = data.get("query", "")
            goals = data.get("goals", [])
            context = data.get("context", None)
            
            # Step 1: Planning
            plan = self.planning_service.create_plan(query, goals)
            
            # Step 2: Research
            research_input = f"Research: {query}"
            if context:
                research_input += f"\nContext: {context}"
            research_result = self.research_agent.run(research_input)
            
            # Step 3: Conditional Summarization
            summary = research_result
            if self._needs_summarization(research_result):
                summary = self.summarize_agent.run(
                    f"Summarize this research: {research_result}"
                )
            
            # Step 4: Conditional Critique
            critique_result = {"passed": True, "score": 1.0}
            for goal in goals:
                if self._needs_critique(summary, goal):
                    critique_input = f"Critique this against goal: {goal}\nContent: {summary}"
                    critique_response = self.critique_agent.run(critique_input)
                    # Parse critique response into result format
                    critique_result = self._parse_critique(critique_response)
                    if not critique_result["passed"]:
                        break
            
            # Step 5: Strategy
            strategy_input = f"Based on: {summary}\nGenerate strategy for: {', '.join(goals)}"
            strategy = self.agent_service.strategy_agent.run(strategy_input)
            
            return {
                "plan": plan,
                "research": research_result,
                "summary": summary,
                "critique": critique_result,
                "strategy": strategy
            }

        except Exception as e:
            log_error(f"SupervisorAgent error for task {task_id}: {e}")
            return {"error": str(e)}
    
    def _parse_critique(self, critique_text: str) -> dict:
        if "not sufficient" in critique_text.lower():
            return {"score": 0.4, "passed": False, "text": critique_text}
        return {"score": 0.85, "passed": True, "text": critique_text}
