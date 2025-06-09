from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from flask_app.core.utils.memory import get_memory, set_memory

class MemoryInput(BaseModel):
    key: str = Field(..., description="Memory key to access")
    value: str = Field(None, description="Value to store (for write operations)")
    operation: str = Field("get", description="Operation: 'get' or 'set'")

class MemoryTool(BaseTool):
    name = "Memory"
    description = "Stores and retrieves task context from memory"
    args_schema = MemoryInput

    def _run(self, key: str, value: str = None, operation: str = "get") -> str:
        if operation == "set":
            set_memory(key, value)
            return f"Value stored for key: {key}"
        return str(get_memory(key))