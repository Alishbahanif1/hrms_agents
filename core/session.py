# Simple in-memory session store (replace with Redis later)

sessions = {}


def get_session(session_id: str):
    if session_id not in sessions:
        sessions[session_id] = {
            "user": {
                "token": None,
                "role": None
            },
            "context": {
                "last_module": None,
                "last_intent": None,
                "last_employee_id": None
            },
            "history": []  # 🔥 conversation memory
        }
    return sessions[session_id]