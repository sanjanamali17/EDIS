# edis_assistant/memory.py

class EDISMemory:
    """
    In-memory session store.
    NOTE: Replace with Redis / DB for production.
    """

    def __init__(self):
        self.store = {}

    def _ensure_session(self, session_id: str):
        if session_id not in self.store:
            self.store[session_id] = {
                "chat": [],
                "last_context": None
            }

    def save_context(self, session_id: str, context: str):
        self._ensure_session(session_id)
        self.store[session_id]["last_context"] = context

    def add_message(self, session_id: str, role: str, content: str):
        self._ensure_session(session_id)
        self.store[session_id]["chat"].append({
            "role": role,
            "content": content
        })

    def get_chat(self, session_id: str):
        self._ensure_session(session_id)
        return self.store[session_id]["chat"]

    def get_last_context(self, session_id: str):
        self._ensure_session(session_id)
        return self.store[session_id]["last_context"]

    def clear_chat(self, session_id: str):
        """Clear all chat messages for a session."""
        self._ensure_session(session_id)
        self.store[session_id]["chat"] = []
