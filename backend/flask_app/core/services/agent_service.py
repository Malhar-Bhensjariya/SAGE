# flask_app/core/services/agent_service.py

from flask_app.agents.research_agent import ResearchAgent
from flask_app.agents.summarizer_agent import SummarizerAgent
from flask_app.agents.critique_agent import CritiqueAgent
from flask_app.agents.strategy_agent import StrategyAgent
from flask_app.agents.supervisor_agent import SupervisorAgent
from flask_app.core.utils.logger import log_info, log_error

class AgentService:
    def __init__(self, use_web_search=False):
        self.research_agent = ResearchAgent(use_web_search=use_web_search)
        self.summarizer_agent = SummarizerAgent()
        self.critique_agent = CritiqueAgent()
        self.strategy_agent = StrategyAgent()
        self.supervisor_agent = SupervisorAgent()

        log_info("AgentService initialized with all core agents.")

    def perform_research(self, query, context=None):
        log_info("Starting research...")
        return self.research_agent.perform_research(query, context)

    def summarize(self, content):
        log_info("Starting summarization...")
        return self.summarizer_agent.summarize(content)

    def critique(self, content, goal, threshold=80):
        log_info("Starting critique...")
        return self.critique_agent.critique(content, goal, threshold)

    def strategize(self, content, goals):
        log_info("Starting strategy formulation...")
        return self.strategy_agent.formulate_strategy(content, goals)

    def supervise(self, task_id, data):
        log_info(f"Supervisor agent managing task {task_id}")
        return self.supervisor_agent.manage_task(task_id, data)

