import os
import json

MEMORY_PATH = "flask_app/data/memory/task_context.json"
_memory_store = {}

def load_memory():
    global _memory_store
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "r") as f:
            _memory_store = json.load(f)

def save_memory():
    with open(MEMORY_PATH, "w") as f:
        json.dump(_memory_store, f, indent=4)

def get_memory(key):
    return _memory_store.get(key)

def set_memory(key, value):
    _memory_store[key] = value
    save_memory()

# Auto-load memory when module is imported
load_memory()
