from langchain.agents import AgentExecutor, Tool, initialize_agent
from langchain.memory import ConversationBufferMemory
from flask_app.tools import (
    GeminiTool,
    SerpTool,
    DocumentQATool,
    MemoryTool
)
from flask_app.core.utils.logger import log_info
from flask_app.core.services.rag_service import RAGService

class AgentService:
    def __init__(self, use_web_search=False):
        self.tools = self._initialize_tools(use_web_search)
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        log_info("AgentService initialized with LangChain tools")

    def _initialize_tools(self, use_web_search):
        tools = [
            Tool(
                name="Gemini",
                func=self._gemini_fallback,
                description="General purpose AI assistant"
            ),
            DocumentQATool(),
            MemoryTool()
        ]

        if use_web_search:
            tools.append(SerpTool())

        return tools

    def _gemini_fallback(self, prompt: str) -> str:
        from flask_app.tools.gemini_connector import generate_response
        return generate_response(prompt)

    def create_agent(self, agent_type: str, **kwargs):
        agent_map = {
            "research": self._create_research_agent,
            "summarize": self._create_summarize_agent,
            "critique": self._create_critique_agent,
            "strategy": self._create_strategy_agent,
            "supervisor": self._create_supervisor_agent
        }
        return agent_map[agent_type](**kwargs)

    def _create_research_agent(self):
        return initialize_agent(
            tools=self.tools,
            agent="zero-shot-react-description",
            memory=self.memory,
            verbose=True,
            max_iterations=5
        )

    def _create_summarize_agent(self):
        return initialize_agent(
            tools=[t for t in self.tools if t.name in ["Gemini", "Memory"]],
            agent="zero-shot-react-description",
            memory=self.memory,
            verbose=True,
            max_iterations=3
        )

    def _create_critique_agent(self):
        return initialize_agent(
            tools=[t for t in self.tools if t.name == "Gemini"],
            agent="zero-shot-react-description",
            memory=self.memory,
            verbose=False,
            max_iterations=2
        )

    def _create_strategy_agent(self):
        return initialize_agent(
            tools=[t for t in self.tools if t.name in ["Gemini", "Memory", "DocumentQA"]],
            agent="zero-shot-react-description",
            memory=self.memory,
            verbose=True,
            max_iterations=4
        )

    def _create_supervisor_agent(self):
        return initialize_agent(
            tools=self.tools,
            agent="zero-shot-react-description",
            memory=self.memory,
            verbose=False,
            max_iterations=6
        )
