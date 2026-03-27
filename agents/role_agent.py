import json
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

from core.config import AZURE_ENDPOINT, MODEL_NAME
from tools.role_tools import (
    create_role,
    get_roles,
    get_role_by_id,
    update_role,
    delete_role
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
        "name": "create_role",
        "description": "Create a role",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "level": {"type": "integer"},
                "description": {"type": "string"},
                "is_active": {"type": "boolean"}
            },
            "required": ["title"]
        }
    },
    {
        "type": "function",
        "name": "get_roles",
        "description": "Get all roles",
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
        "name": "get_role_by_id",
        "description": "Get role by ID",
        "parameters": {
            "type": "object",
            "properties": {
                "role_id": {"type": "integer"}
            },
            "required": ["role_id"]
        }
    },
    {
        "type": "function",
        "name": "update_role",
        "description": "Update role",
        "parameters": {
            "type": "object",
            "properties": {
                "role_id": {"type": "integer"},
                "title": {"type": "string"},
                "level": {"type": "integer"},
                "description": {"type": "string"},
                "is_active": {"type": "boolean"}
            },
            "required": ["role_id"]
        }
    },
    {
        "type": "function",
        "name": "delete_role",
        "description": "Delete role",
        "parameters": {
            "type": "object",
            "properties": {
                "role_id": {"type": "integer"}
            },
            "required": ["role_id"]
        }
    }
]


# =========================
# 🚀 AGENT
# =========================
def run_roles_agent(user_input: str, token: str, session=None):

    history = session.get("history", [])[-10:] if session else []

    history_text = ""
    for msg in history:
        role = msg["role"].upper()
        content = str(msg["content"])
        history_text += f"{role}: {content}\n"

    prompt = f"""
    You are a roles assistant.

    STRICT RULES:
    - ALWAYS use tools
    - NEVER respond in plain text
    - ALWAYS call a function

    DECISION RULES:
    - "list roles" → get_roles
    - "create role" → create_role
    - "delete role" → delete_role

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

    if tool_name == "create_role":
        result = create_role(args, token)

    elif tool_name == "get_roles":
        result = get_roles(token, args)

    elif tool_name == "get_role_by_id":
        result = get_role_by_id(args["role_id"], token)

    elif tool_name == "update_role":
        role_id = args["role_id"]
        data = {k: v for k, v in args.items() if k != "role_id"}
        result = update_role(role_id, data, token)

    elif tool_name == "delete_role":
        result = delete_role(args["role_id"], token)

    else:
        return "❌ Unknown tool", {}

    return json.dumps(result, indent=2), {}