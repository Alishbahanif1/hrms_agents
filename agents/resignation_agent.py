import json
from core.config import MODEL_NAME, AZURE_ENDPOINT
from core.session import get_session

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from tools.resignation_tools import (
    create_resignation,
    get_resignations,
    get_resignation_by_id,
    update_resignation,
    delete_resignation,
    get_clearance_list,
    update_clearance
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
# 🔥 TOOL SCHEMA
# =========================
tools = [
    {
        "type": "function",
        "name": "create_resignation",
        "description": "Create resignation",
        "parameters": {
            "type": "object",
            "properties": {
                "resignation_date": {"type": "string"},
                "notice_end_date": {"type": "string"}
            },
            "required": ["resignation_date", "notice_end_date"]
        }
    },
    {
        "type": "function",
        "name": "get_resignations",
        "description": "Get all resignations",
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
        "name": "get_resignation_by_id",
        "description": "Get resignation by ID",
        "parameters": {
            "type": "object",
            "properties": {
                "resignation_id": {"type": "integer"}
            },
            "required": ["resignation_id"]
        }
    },
    {
        "type": "function",
        "name": "update_resignation",
        "description": "Update resignation",
        "parameters": {
            "type": "object",
            "properties": {
                "resignation_id": {"type": "integer"},
                "manager_approved": {"type": "boolean"},
                "status": {"type": "string"},
                "is_active": {"type": "boolean"}
            },
            "required": ["resignation_id"]
        }
    },
    {
        "type": "function",
        "name": "delete_resignation",
        "description": "Delete resignation",
        "parameters": {
            "type": "object",
            "properties": {
                "resignation_id": {"type": "integer"}
            },
            "required": ["resignation_id"]
        }
    },
    {
        "type": "function",
        "name": "get_clearance_list",
        "description": "Get clearance records",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "type": "function",
        "name": "update_clearance",
        "description": "Update clearance",
        "parameters": {
            "type": "object",
            "properties": {
                "resignation_id": {"type": "integer"},
                "laptop_returned": {"type": "boolean"},
                "access_revoked": {"type": "boolean"},
                "email_deactivated": {"type": "boolean"},
                "is_active": {"type": "boolean"}
            },
            "required": ["resignation_id"]
        }
    }
]

# =========================
# 🚀 RESIGNATION AGENT
# =========================
def run_resignation_agent(user_input: str, token: str, session=None):

    # =========================
    # 🧠 BUILD CONTEXT
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
You are a Resignation Assistant.

STRICT RULES:
- You MUST use tools for ALL operations
- NEVER say "I don’t have access"
- NEVER ask user for data
- ALWAYS call tools

DECISION RULES:

If user asks:
- "apply resignation" → create_resignation
- "submit resignation" → create_resignation
- "list resignations" → get_resignations
- "show resignations" → get_resignations
- "resignation details" → get_resignation_by_id
- "approve resignation" → update_resignation
- "reject resignation" → update_resignation
- "delete resignation" → delete_resignation
- "clearance list" → get_clearance_list
- "update clearance" → update_clearance

IMPORTANT:
- DO NOT answer without tool
- ALWAYS prefer tool call

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
        "resignation_id": None
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
    if tool_name == "create_resignation":
        result = create_resignation(args, token)

    elif tool_name == "get_resignations":
        result = get_resignations(token, args)

    elif tool_name == "get_resignation_by_id":
        result = get_resignation_by_id(args["resignation_id"], token)
        meta["resignation_id"] = args["resignation_id"]

    elif tool_name == "update_resignation":
        rid = args["resignation_id"]
        data = {k: v for k, v in args.items() if k != "resignation_id"}
        result = update_resignation(rid, data, token)
        meta["resignation_id"] = rid

    elif tool_name == "delete_resignation":
        result = delete_resignation(args["resignation_id"], token)
        meta["resignation_id"] = args["resignation_id"]

    elif tool_name == "get_clearance_list":
        result = get_clearance_list(token)

    elif tool_name == "update_clearance":
        rid = args["resignation_id"]
        data = {k: v for k, v in args.items() if k != "resignation_id"}
        result = update_clearance(rid, data, token)
        meta["resignation_id"] = rid

    else:
        return "❌ Unknown tool", meta

    # =========================
    # 🎨 FORMAT RESPONSE
    # =========================
    format_prompt = f"""
You are a Resignation Assistant.

User Request:
{user_input}

STRICT RULES:
- DO NOT change or invent data
- DO NOT skip fields

FORMATTING RULES:
- If multiple records → return table
- If single record → structured format
- Keep response clean

TABLE COLUMNS:
ID | Resignation Date | Notice End | Status | Active

DATA LIMIT:
- Max 10 records
- Mention if truncated

API Response:
{json.dumps(result)}
"""

    format_response = client.responses.create(
        model=MODEL_NAME,
        input=format_prompt
    )

    return format_response.output_text, meta