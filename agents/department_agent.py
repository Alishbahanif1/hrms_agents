import json
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

from core.config import AZURE_ENDPOINT, MODEL_NAME
from tools.department_tools import (
    create_department,
    get_departments,
    get_department_by_id,
    update_department,
    delete_department
)

project_client = AIProjectClient(
    endpoint=AZURE_ENDPOINT,
    credential=DefaultAzureCredential()
)

client = project_client.get_openai_client()


# =========================
# 🔥 TOOL SCHEMA
# =========================
tools = [
    {
        "type": "function",
        "name": "create_department",
        "description": "Create department",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "is_active": {"type": "boolean"}
            },
            "required": ["name"]
        }
    },
    {
        "type": "function",
        "name": "get_departments",
        "description": "Get all departments",
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
        "name": "get_department_by_id",
        "description": "Get department by ID",
        "parameters": {
            "type": "object",
            "properties": {
                "department_id": {"type": "integer"}
            },
            "required": ["department_id"]
        }
    },
    {
        "type": "function",
        "name": "update_department",
        "description": "Update department",
        "parameters": {
            "type": "object",
            "properties": {
                "department_id": {"type": "integer"},
                "name": {"type": "string"}
            },
            "required": ["department_id"]
        }
    },
    {
        "type": "function",
        "name": "delete_department",
        "description": "Delete department",
        "parameters": {
            "type": "object",
            "properties": {
                "department_id": {"type": "integer"}
            },
            "required": ["department_id"]
        }
    }
]


# =========================
# 🚀 AGENT
# =========================
def run_department_agent(user_input: str, token: str, session=None):

    history = session.get("history", [])[-10:] if session else []

    history_text = ""
    for msg in history:
        role = msg["role"].upper()
        content = str(msg["content"])
        history_text += f"{role}: {content}\n"

        prompt = f"""
        You are a department assistant.
        
        STRICT RULES (VERY IMPORTANT):
        
        - You MUST ALWAYS use tools
        - You are NOT allowed to respond in plain text
        - You MUST call a function for ANY user request
        
        NEVER:
        - ask user for clarification if intent is obvious
        - say "I don't have access"
        - respond without tool
        
        DECISION RULES:
        
        If user says:
        - "list departments" → call get_departments
        - "get all departments" → call get_departments
        - "departments" → call get_departments
        - "create department X" → call create_department
        - "delete department" → call delete_department
        
        If unsure → STILL call closest tool
        
        Conversation:
        {history_text}
        
        User:
        {user_input}
        """
    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
        tools=tools,
        tool_choice="auto"
    )

    output = response.output[0]

    if output.type != "function_call":
        return "⚠️ Please be more specific.", {}

    tool_name = output.name
    args = json.loads(output.arguments)

    print("TOOL:", tool_name)
    print("ARGS:", args)

    if tool_name == "create_department":
        result = create_department(args, token)

    elif tool_name == "get_departments":
        result = get_departments(token, args)

    elif tool_name == "get_department_by_id":
        result = get_department_by_id(args["department_id"], token)

    elif tool_name == "update_department":
        department_id = args["department_id"]
        data = {k: v for k, v in args.items() if k != "department_id"}
        result = update_department(department_id, data, token)

    elif tool_name == "delete_department":
        result = delete_department(args["department_id"], token)

    else:
        return "❌ Unknown tool", {}

    return json.dumps(result, indent=2), {}