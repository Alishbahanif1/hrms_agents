# master_agent.py
import json
from core.session import get_session
from agents.hr_agent import run_hr_agent
from agents.department_agent import run_department_agent
from agents.hiring_agent import run_hiring_agent
from agents.role_agent import run_roles_agent
from agents.resignation_agent import run_resignation_agent
from core.config import MODEL_NAME
from core.llm_client import client  # use single LLM client

# =========================
# 🧠 HELPER: Check if user wants formatting
# =========================
def is_format_request(user_input: str):
    keywords = ["bullet", "tabular", "table", "format", "list"]
    text = user_input.lower()
    return any(word in text for word in keywords)

# =========================
# 🧠 LLM ROUTER
# =========================
def detect_module(user_input: str, session: dict) -> str:
    """
    Uses LLM to detect intent/module from user input.
    """
    # Last few messages for context
    history = session.get("history", [])[-5:]
    history_text = ""
    for msg in history:
        role = msg["role"].upper()
        content = str(msg["content"])
        history_text += f"{role}: {content}\n"

    response = client.responses.create(
        model=MODEL_NAME,
        input=f"""
You are a smart HRMS request router.

Your task: Classify the user request into a single module.
Modules:
- hr → employees, payroll, leave, salary
- department → CRUD departments
- roles → CRUD roles
- hiring → hiring requests, recruitment, job postings
- resignation → resignations, notice period, clearance, exit process
- format → only when user explicitly asks to reformat output (table, bullets, etc.)

Rules:
- If user says "create hiring", "get hiring", "list hiring", "update hiring", → routing must be "hiring"
- If user says "employee", "salary", "manager" → routing is "hr"
- Only return "format" if user says explicitly "format", "table", "bullets", "convert"
- If user says "resign", "resignation", "notice period", "apply resignation" → routing must be "resignation"
- If user says "clearance", "exit clearance", "final clearance" → routing must be "resignation"

IMPORTANT:
- Return only valid JSON: {{ "module": "<module_name>" }}
- Do not add extra text
- Never guess a module; default only to "hr" if LLM fails

Conversation History:
{history_text}

User Input:
{user_input}
"""
)

    try:
        module = json.loads(response.output_text.strip()).get("module", "hr")
        return module
    except Exception:
        return "hr"

# =========================
# 🚀 MASTER AGENT
# =========================
def run_master_agent(user_input: str, token: str, session_id: str):
    session = get_session(session_id)

    # Store token
    session["user"]["token"] = token

    # Add user message to history
    session["history"].append({"role": "user", "content": user_input})
    session["history"] = session["history"][-5:]  # keep last 10 messages

    # =========================
    # 🧠 ROUTING
    # =========================
    text = user_input.lower()

    if is_format_request(user_input):
        module = "format"

    elif "resign" in text or "resignation" in text or "notice" in text or "clearance" in text:
        module = "resignation"

    elif "hiring" in text or "job" in text:
        module = "hiring"

    elif "role" in text:
        module = "roles"

    elif "department" in text:
        module = "department"

    elif "employee" in text or "salary" in text or "manager" in text:
        module = "hr"

    else:
        module = detect_module(user_input, session)

    print("ROUTED TO:", module)

    # =========================
    # 🔥 HANDLE MODULES
    # =========================
    if module == "hr":
        response, meta = run_hr_agent(user_input, token, session)
    elif module == "department":
        response, meta = run_department_agent(user_input, token, session)
    elif module == "roles":
        response, meta = run_roles_agent(user_input, token, session)
    elif module == "hiring":
        response, meta = run_hiring_agent(user_input, token, session)
    elif module == "format":
        # Find last assistant response
        last_response = next(
            (msg["content"] for msg in reversed(session["history"]) if msg["role"] == "assistant"), 
            None
        )
        if not last_response:
            return "⚠️ Nothing to format yet."
        from agents.format_agent import format_response_with_llm
        response = format_response_with_llm(last_response, user_input)
        meta = {}
    elif module == "resignation":
        response, meta = run_resignation_agent(user_input, token, session)
    else:
        return "❌ Could not determine module"

    # =========================
    # 🧠 STORE ASSISTANT RESPONSE
    # =========================
    session["history"].append({"role": "assistant", "content": response})
    session["history"] = session["history"][-10:]

    # Store last employee/department for context if available
    if meta.get("employee_id"):
        session["context"]["last_employee_id"] = meta["employee_id"]
    if meta.get("department_id"):
        session["context"]["last_department_id"] = meta["department_id"]

    session["context"]["last_module"] = module

    return response