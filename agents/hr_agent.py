import json
from core.config import MODEL_NAME, AZURE_ENDPOINT
from core.session import get_session

# from agents.hr_agent import run_hr_agent
# from agents.department_agent import run_department_agent

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from tools.employee_tools import (
    create_employee,
    get_employees,
    get_employee_by_id,
    update_employee,
    delete_employee
)


# =========================
# 🔹 Azure Client
# =========================
project_client = AIProjectClient(
    endpoint=AZURE_ENDPOINT,
    credential=DefaultAzureCredential()
)

client = project_client.get_openai_client()

# =========================
# 🔥 TOOL SCHEMA (HR)
# =========================
tools = [
    {
        "type": "function",
        "name": "create_employee",
        "description": "Create a new employee",
        "parameters": {
            "type": "object",
            "properties": {
                "full_name": {"type": "string"},
                "email": {"type": "string"},
                "personal_email": {"type": "string"},
                "department_id": {"type": "integer"},
                "role_id": {"type": "integer"},
                "manager_id": {"type": "integer"},
                "joining_date": {"type": "string"},
                "salary": {"type": "number"}
            },
            "required": [
                "full_name",
                "email",
                "personal_email",
                "department_id",
                "role_id"
            ]
        }
    },
    {
        "type": "function",
        "name": "get_employees",
        "description": "Get all employees with optional filters",
        "parameters": {
            "type": "object",
            "properties": {
                "page": {"type": "integer"},
                "per_page": {"type": "integer"},
                "search": {"type": "string"},
                "is_active": {"type": "boolean"}
            }
        }
    },
    {
        "type": "function",
        "name": "get_employee_by_id",
        "description": "Get employee details by ID",
        "parameters": {
            "type": "object",
            "properties": {
                "employee_id": {"type": "integer"}
            },
            "required": ["employee_id"]
        }
    },
    {
        "type": "function",
        "name": "update_employee",
        "description": "Update an employee",
        "parameters": {
            "type": "object",
            "properties": {
                "employee_id": {"type": "integer"},
                "full_name": {"type": "string"},
                "email": {"type": "string"},
                "personal_email": {"type": "string"},
                "department_id": {"type": "integer"},
                "role_id": {"type": "integer"},
                "manager_id": {"type": "integer"},
                "joining_date": {"type": "string"},
                "salary": {"type": "number"},
                "is_active": {"type": "boolean"}
            },
            "required": ["employee_id"]
        }
    },
    {
        "type": "function",
        "name": "delete_employee",
        "description": "Delete an employee",
        "parameters": {
            "type": "object",
            "properties": {
                "employee_id": {"type": "integer"}
            },
            "required": ["employee_id"]
        }
    }
]

# =========================
# 🚀 HR AGENT
# =========================
def run_hr_agent(user_input: str, token: str, session=None):

    # =========================
    # 🧠 BUILD CONTEXT (FIXED)
    # =========================

    history = session.get("history", [])[-10:] if session else []

    history_text = ""

    for msg in history:
        if not msg.get("content"):
            continue

        role = msg["role"].upper()
        content = str(msg["content"])

        history_text += f"{role}: {content}\n"
    prompt = f"""
You are an HR assistant.

STRICT RULES:
- You MUST use tools for ALL data retrieval
- NEVER say "I don’t have access"
- NEVER ask user for data
- ALWAYS call tools if data is needed

DECISION RULES:

If user asks:
- "list employees" → call get_employees
- "employees in department X" → call get_employees and filter
- "employee details" → call get_employee_by_id

IMPORTANT:
- DO NOT answer without tool
- ALWAYS prefer tool over text response

Conversation:
{history_text}

User:
{user_input}
"""

    # =========================
    # 🤖 LLM CALL
    # =========================
    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
        tools=tools,
        tool_choice="auto"
    )

    output = response.output[0]

    meta = {
        "employee_id": None
    }

    # =========================
    # ❌ Prevent hallucination
    # =========================
    if output.type != "function_call":
        return "⚠️ I couldn't perform that action. Please be more specific.", meta

    tool_name = output.name
    args = json.loads(output.arguments)

    print("TOOL:", tool_name)
    print("ARGS:", args)

    # =========================
    # 🔧 TOOL EXECUTION
    # =========================
    if tool_name == "create_employee":
        result = create_employee(args, token)

    elif tool_name == "get_employees":
        result = get_employees(token)

    elif tool_name == "get_employee_by_id":
        result = get_employee_by_id(args["employee_id"], token)
        meta["employee_id"] = args["employee_id"]

    elif tool_name == "update_employee":
        employee_id = args["employee_id"]
        data = {k: v for k, v in args.items() if k != "employee_id"}

        result = update_employee(employee_id, data, token)
        meta["employee_id"] = employee_id

    elif tool_name == "delete_employee":
        result = delete_employee(args["employee_id"], token)
        meta["employee_id"] = args["employee_id"]

    else:
        return "❌ Unknown tool", meta

    # =========================
    # ✅ RETURN REAL RESULT
    # =========================
# =========================
# 🎨 FORMAT RESPONSE (NEW)
# =========================
    format_prompt = f"""
    You are an HR assistant.

    User Request:
    {user_input}

    Format the API response accordingly.

    STRICT RULES:
    - DO NOT change or invent data
    - DO NOT skip fields

    FORMATTING RULES:
    - If user asks for "table" or "tabular" → MUST return markdown table
    - If multiple employees → prefer table format
    - If single employee → show structured readable format
    - Keep response clean and readable

    TABLE RULES (if table required):
    - Columns: ID | Name | Email | Department | Role | Status
    - Use markdown table format

    DATA LIMIT RULE:
    - If more than 10 records → ONLY show first 10
    - Mention: "Showing 10 of X employees"

    API Response:
    {json.dumps(result)}
    """

    format_response = client.responses.create(
        model=MODEL_NAME,
        input=format_prompt
    )

    output = format_response.output[0]

    return format_response.output_text, meta