import json
from urllib import response
from core.llm_client import client
from core.config import MODEL_NAME

from tools.hiring_tools import (
    create_hiring_request,
    get_hiring_requests,
    get_hiring_request_by_id,
    update_hiring_request,
    delete_hiring_request,
    create_job_posting,
    get_job_postings,
    get_job_posting_by_id,
    update_job_posting,
    delete_job_posting
)


# =========================
# 🔥 TOOL SCHEMA
# =========================
tools = [
    {
        "type": "function",
        "name": "create_hiring_request",
        "description": "Create hiring request",
        "parameters": {
            "type": "object",
            "properties": {
                "department_id": {"type": "integer"},
                "role_title": {"type": "string"},
                "manager_id": {"type": "integer"},
                "required_skills": {"type": "string"},
                "experience_level": {"type": "string"},
                "budget_range": {"type": "string"}
            },
            "required": ["department_id", "role_title", "manager_id", "required_skills", "experience_level", "budget_range"]
        }
    },
    {
        "type": "function",
        "name": "get_hiring_requests",
        "description": "Get all hiring requests",
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
        "name": "get_hiring_request_by_id",
        "description": "Get hiring request by ID",
        "parameters": {
            "type": "object",
            "properties": {
                "hiring_id": {"type": "integer"}
            },
            "required": ["hiring_id"]
        }
    },
    {
        "type": "function",
        "name": "update_hiring_request",
        "description": "Update hiring request",
        "parameters": {
            "type": "object",
            "properties": {
                "hiring_id": {"type": "integer"},
                "status": {"type": "string"},
                "manager_approved": {"type": "boolean"}
            },
            "required": ["hiring_id"]
        }
    },
    {
        "type": "function",
        "name": "delete_hiring_request",
        "description": "Delete hiring request",
        "parameters": {
            "type": "object",
            "properties": {
                "hiring_id": {"type": "integer"}
            },
            "required": ["hiring_id"]
        }
    },

    # =========================
    # 🔥 JOB POSTINGS
    # =========================
    {
        "type": "function",
        "name": "create_job_posting",
        "description": "Create job posting",
        "parameters": {
            "type": "object",
            "properties": {
                "hiring_request_id": {"type": "integer"}
            },
            "required": ["hiring_request_id"]
        }
    },
    {
        "type": "function",
        "name": "get_job_postings",
        "description": "Get all job postings",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "type": "function",
        "name": "get_job_posting_by_id",
        "description": "Get job posting by ID",
        "parameters": {
            "type": "object",
            "properties": {
                "posting_id": {"type": "integer"}
            },
            "required": ["posting_id"]
        }
    },
    {
        "type": "function",
        "name": "update_job_posting",
        "description": "Update job posting",
        "parameters": {
            "type": "object",
            "properties": {
                "posting_id": {"type": "integer"},
                "status": {"type": "string"}
            },
            "required": ["posting_id"]
        }
    },
    {
        "type": "function",
        "name": "delete_job_posting",
        "description": "Delete job posting",
        "parameters": {
            "type": "object",
            "properties": {
                "posting_id": {"type": "integer"}
            },
            "required": ["posting_id"]
        }
    }
]


# =========================
# 🚀 AGENT
# =========================
def run_hiring_agent(user_input: str, token: str, session=None):

    history = session.get("history", [])[-10:] if session else []

    history_text = ""
    for msg in history:
        if not msg.get("content"):
            continue

        role = msg["role"].upper()
        content = str(msg["content"])
        history_text += f"{role}: {content}\n"
    prompt = f"""
    You are a Hiring Assistant.

    You can perform these actions:

    1. Create hiring request
    2. Get all hiring requests
    3. Get hiring request by ID
    4. Update hiring request
    5. Delete hiring request

    =========================
    RULES
    =========================

    - You MUST use tools for ALL operations
    - NEVER respond without using a tool if data is needed
    - NEVER ask for data when user wants to retrieve

    =========================
    INTENT RULES
    =========================

    If user says:
    - "list hiring requests" → call get_hiring_requests
    - "get all hiring" → call get_hiring_requests
    - "show hiring requests" → call get_hiring_requests

    - "get hiring id X" → call get_hiring_request_by_id

    - "update hiring id X" → call update_hiring_request

    - "delete hiring id X" → call delete_hiring_request

    - "create hiring request" → follow create rules

    =========================
    CREATE RULE (ONLY FOR CREATE)
    =========================

    Required fields:
    - department_id
    - role_title
    - manager_id
    - required_skills
    - experience_level
    - budget_range

    If missing:
    → Ask ONLY missing fields

    If complete:
    → Call create_hiring_request

    =========================
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
        # LLM will ask user for missing fields
        return response.output_text, {}
    tool_name = output.name
    args = json.loads(output.arguments)

    print("TOOL:", tool_name)
    print("ARGS:", args)

    # =========================
    # 🔧 EXECUTE TOOL
    # =========================
    if tool_name == "create_hiring_request":
        result = create_hiring_request(args, token)

    elif tool_name == "get_hiring_requests":
        result = get_hiring_requests(token, args if args else None)

    elif tool_name == "get_hiring_request_by_id":
        result = get_hiring_request_by_id(args["hiring_id"], token)

    elif tool_name == "update_hiring_request":
        hiring_id = args["hiring_id"]
        data = {k: v for k, v in args.items() if k != "hiring_id"}
        result = update_hiring_request(hiring_id, data, token)

    elif tool_name == "delete_hiring_request":
        result = delete_hiring_request(args["hiring_id"], token)

    elif tool_name == "create_job_posting":
        result = create_job_posting(args, token)

    elif tool_name == "get_job_postings":
        result = get_job_postings(token)

    elif tool_name == "get_job_posting_by_id":
        result = get_job_posting_by_id(args["posting_id"], token)

    elif tool_name == "update_job_posting":
        posting_id = args["posting_id"]
        data = {k: v for k, v in args.items() if k != "posting_id"}
        result = update_job_posting(posting_id, data, token)

    elif tool_name == "delete_job_posting":
        result = delete_job_posting(args["posting_id"], token)

    else:
        return "❌ Unknown tool", {}

    # =========================
    # 🎨 FORMAT RESPONSE (same pattern as HR)
    # =========================
    format_prompt = f"""
You are a Hiring Assistant.

User Request:
{user_input}

Format the API response clearly.

STRICT RULES:
- DO NOT change data
- DO NOT hallucinate

FORMATTING:
- Lists → bullet points or table
- Single → structured readable format

API Response:
{json.dumps(result)}
"""

    format_response = client.responses.create(
        model=MODEL_NAME,
        input=format_prompt
    )

    return format_response.output_text, {}