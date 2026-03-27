import json
from core.config import MODEL_NAME, AZURE_ENDPOINT
from core.session import get_session

from agents.hr_agent import run_hr_agent
from agents.department_agent import run_department_agent

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential


# =========================
# 🔹 Azure Client
# =========================
project_client = AIProjectClient(
    endpoint=AZURE_ENDPOINT,
    credential=DefaultAzureCredential()
)

client = project_client.get_openai_client()


# =========================
# 🧠 FORMAT DETECTOR
# =========================
def is_format_request(user_input: str):
    text = user_input.lower()
    return any(word in text for word in [
        "bullet", "bulleted", "bullets",
        "table", "tabular",
        "format", "list"
    ])


# =========================
# 🧠 ROUTER (LLM + fallback)
# =========================
def detect_module(user_input: str, session):

    history = session.get("history", [])[-5:]

    history_text = "\n".join([
        f"{msg['role'].upper()}: {msg['content']}"
        for msg in history if msg.get("content")
    ])

    response = client.responses.create(
        model=MODEL_NAME,
        input=f"""
You are a request router.

Decide the module.

Context:
{history_text}

User input:
{user_input}

Rules:
- hr → employees
- department → departments
- format → formatting request
- admin → roles/permissions
- sales → customers/orders

IMPORTANT:
- If formatting requested → return "format"

Return ONLY JSON:
{{ "module": "hr" }}
"""
    )

    try:
        return json.loads(response.output_text.strip()).get("module", "hr")
    except:
        return "hr"


# =========================
# 🎨 FORMATTER (RE-FORMAT)
# =========================
def format_response_with_llm(raw_response: str, user_input: str):

    prompt = f"""
You are a helpful assistant.

User request:
{user_input}

Reformat the data.

RULES:
- DO NOT change data
- ONLY change format

If bullets:
• Name — Role

If table:
Return markdown table

DATA:
{raw_response}
"""

    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt
    )

    return response.output_text


# =========================
# 🎨 FINAL FORMATTER
# =========================
def format_final_response(raw_response: str, user_input: str):

    prompt = f"""
You are a helpful HR assistant.

User asked:
{user_input}

Convert the API response into a natural, human-friendly response.

STRICT RULES:
- DO NOT show JSON
- Extract useful info only
- Keep it short
- Be conversational

Examples:

Create:
→ "Department 'Finance' created successfully."

List:
→ bullet list or table

Single:
→ structured details

DATA:
{raw_response}
"""

    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt
    )

    return response.output_text


# =========================
# 🚀 MASTER AGENT
# =========================
def run_master_agent(user_input: str, token: str, session_id: str):

    session = get_session(session_id)

    # =========================
    # 🧠 STORE USER MESSAGE
    # =========================
    session["history"].append({
        "role": "user",
        "content": user_input
    })

    session["history"] = session["history"][-10:]

    # =========================
    # 🧠 ROUTING (fallback first)
    # =========================
    text = user_input.lower()

    if "department" in text:
        module = "department"
    elif "employee" in text:
        module = "hr"
    elif is_format_request(user_input):
        module = "format"
    else:
        module = detect_module(user_input, session)

    print("ROUTED TO:", module)

    # =========================
    # 🎨 FORMAT REQUEST
    # =========================
    if module == "format":

        last_response = next(
            (m["content"] for m in reversed(session["history"]) if m["role"] == "assistant"),
            None
        )

        if not last_response:
            return "⚠️ Nothing to format."

        formatted = format_response_with_llm(last_response, user_input)

        session["history"].append({
            "role": "assistant",
            "content": formatted
        })

        session["history"] = session["history"][-10:]

        return formatted

    # =========================
    # 🔥 HR MODULE
    # =========================
    if module == "hr":

        raw_response, meta = run_hr_agent(
            user_input=user_input,
            token=token,
            session=session
        )

    # =========================
    # 🔥 DEPARTMENT MODULE
    # =========================
    elif module == "department":

        raw_response, meta = run_department_agent(
            user_input=user_input,
            token=token,
            session=session
        )

    else:
        return "❌ Could not determine module"

    # =========================
    # 🎨 FINAL FORMAT (ALWAYS)
    # =========================
    formatted = format_final_response(raw_response, user_input)

    # =========================
    # 🧠 STORE ONLY FORMATTED
    # =========================
    session["history"].append({
        "role": "assistant",
        "content": formatted
    })

    session["history"] = session["history"][-10:]

    return formatted