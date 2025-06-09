import os
import json
from typing import Any, Optional
from datetime import datetime
from flask_app.core.utils.logger import log

MEMORY_PATH = os.path.join("flask_app", "data", "memory", "task_context.json")

class MemoryManager:
    def __init__(self):
        self.memory = self._load_memory()

    def _load_memory(self) -> dict:
        try:
            if os.path.exists(MEMORY_PATH):
                with open(MEMORY_PATH, "r") as f:
                    return json.load(f)
            return {}
        except Exception as e:
            log(f"Error loading memory: {e}", level="ERROR")
            return {}

    def _save_memory(self):
        try:
            os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)
            with open(MEMORY_PATH, "w") as f:
                json.dump(self.memory, f, indent=4)
        except Exception as e:
            log(f"Error saving memory: {e}", level="ERROR")

    def get(self, key: str, default: Any = None) -> Any:
        return self.memory.get(key, default)

    def set(self, key: str, value: Any):
        self.memory[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        self._save_memory()

# Global instance for backward compatibility
_memory_manager = MemoryManager()

# Legacy functions (deprecated but kept for compatibility)
def load_memory():
    pass  # Now handled by MemoryManager initialization

def save_memory():
    _memory_manager._save_memory()

def get_memory(key: str) -> Any:
    return _memory_manager.get(key)

def set_memory(key: str, value: Any):
    _memory_manager.set(key, value)