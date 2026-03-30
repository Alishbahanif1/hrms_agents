import json
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

from core.config import AZURE_ENDPOINT, MODEL_NAME
from tools.hiring_tools import *

from tools.department_tools import get_departments

project_client = AIProjectClient(
    endpoint=AZURE_ENDPOINT,
    credential=DefaultAzureCredential()
)

client = project_client.get_openai_client()


# =========================
# 🔥 TOOL SCHEMA
# =========================
tools = [
    # Hiring Requests
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
            "required": [
                "department_id",
                "role_title",
                "manager_id",
                "required_skills",
                "experience_level",
                "budget_range"
            ]
        }
    },
    {
        "type": "function",
        "name": "get_hiring_requests",
        "description": "Get hiring requests",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "type": "function",
        "name": "get_hiring_request_by_id",
        "description": "Get hiring request by ID",
        "parameters": {
            "type": "object",
            "properties": {"hiring_id": {"type": "integer"}},
            "required": ["hiring_id"]
        }
    },
    {
        "type": "function",
        "name": "update_hiring_request",
        "description": "Update hiring request",
        "parameters": {
            "type": "object",
            "properties": {"hiring_id": {"type": "integer"}},
            "required": ["hiring_id"]
        }
    },
    {
        "type": "function",
        "name": "delete_hiring_request",
        "description": "Delete hiring request",
        "parameters": {
            "type": "object",
            "properties": {"hiring_id": {"type": "integer"}},
            "required": ["hiring_id"]
        }
    },

    # Job Posting
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
        "description": "Get job postings",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "type": "function",
        "name": "get_job_posting_by_id",
        "description": "Get job posting by ID",
        "parameters": {
            "type": "object",
            "properties": {"posting_id": {"type": "integer"}},
            "required": ["posting_id"]
        }
    },
    {
        "type": "function",
        "name": "update_job_posting",
        "description": "Update job posting",
        "parameters": {
            "type": "object",
            "properties": {"posting_id": {"type": "integer"}},
            "required": ["posting_id"]
        }
    },
    {
        "type": "function",
        "name": "delete_job_posting",
        "description": "Delete job posting",
        "parameters": {
            "type": "object",
            "properties": {"posting_id": {"type": "integer"}},
            "required": ["posting_id"]
        }
    }
]


# =========================
# 🚀 AGENT
# =========================
def run_hiring_agent(user_input: str, token: str, session=None):

    # =========================
    # 🧠 BUILD CONTEXT
    # =========================
    history = session.get("history", [])[-10:] if session else []

    history_text = ""
    for msg in history:
        if not msg.get("content"):
            continue
        history_text += f"{msg['role'].upper()}: {msg['content']}\n"

    # =========================
    # 🎯 MAIN PROMPT
    # =========================
    prompt = f"""
You are a hiring assistant.

STRICT RULES:
- You MUST use tools for ALL actions
- NEVER respond without tool usage
- NEVER guess IDs (department_id, hiring_id, posting_id)

DECISION RULES:

Hiring Requests:
- "create hiring request" → create_hiring_request
- "list hiring requests" → get_hiring_requests
- "hiring details" → get_hiring_request_by_id
- "update hiring request" → update_hiring_request
- "delete hiring request" → delete_hiring_request

Job Postings:
- "create job posting" → create_job_posting
- "list job postings" → get_job_postings
- "job posting details" → get_job_posting_by_id

IMPORTANT:
- If user says "create hiring request" → MUST call create_hiring_request DIRECTLY
- DO NOT call get_hiring_requests before creating
- DO NOT check existing data unless explicitly asked

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
        "hiring_id": None,
        "posting_id": None
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
    # 🧠 SMART PRE-PROCESSING (KEY FIX)
    # =========================
    # Handle department name → ID resolution
    if tool_name == "create_hiring_request" and "department_id" not in args:

        departments = get_departments(token).get("data", [])

        for dept in departments:
            if dept["name"].lower() in user_input.lower():
                args["department_id"] = dept["id"]
                print("AUTO-RESOLVED DEPARTMENT:", dept["id"])
                break

        # 🔥 NOW CONTINUE EXECUTION (THIS WAS MISSING)
        result = create_hiring_request(args, token)

    if session and session.get("pending_hiring"):
        if user_input.lower() in ["yes", "yes please", "go ahead"]:

            args = session["pending_hiring"]
            print("EXECUTING SAVED ACTION:", args)

            result = create_hiring_request(args, token)

            session.pop("pending_hiring", None)

            return json.dumps(result, indent=2), {}

    # =========================
    # 🔧 TOOL EXECUTION
    # =========================
    if tool_name == "create_hiring_request":
        result = create_hiring_request(args, token)

    elif tool_name == "get_hiring_requests":
        result = get_hiring_requests(token, args)

    elif tool_name == "get_hiring_request_by_id":
        result = get_hiring_request_by_id(args["hiring_id"], token)
        meta["hiring_id"] = args["hiring_id"]

    elif tool_name == "update_hiring_request":
        hid = args["hiring_id"]
        data = {k: v for k, v in args.items() if k != "hiring_id"}
        result = update_hiring_request(hid, data, token)
        meta["hiring_id"] = hid

    elif tool_name == "delete_hiring_request":
        result = delete_hiring_request(args["hiring_id"], token)
        meta["hiring_id"] = args["hiring_id"]

    # =========================
    # 📌 JOB POSTINGS
    # =========================
    elif tool_name == "create_job_posting":
        result = create_job_posting(args, token)

    elif tool_name == "get_job_postings":
        result = get_job_postings(token, args)

    elif tool_name == "get_job_posting_by_id":
        result = get_job_posting_by_id(args["posting_id"], token)
        meta["posting_id"] = args["posting_id"]

    elif tool_name == "update_job_posting":
        pid = args["posting_id"]
        data = {k: v for k, v in args.items() if k != "posting_id"}
        result = update_job_posting(pid, data, token)
        meta["posting_id"] = pid

    elif tool_name == "delete_job_posting":
        result = delete_job_posting(args["posting_id"], token)
        meta["posting_id"] = args["posting_id"]

    else:
        return "❌ Unknown tool", meta

    # =========================
    # 🎨 FORMAT RESPONSE (HR STYLE)
    # =========================
    format_prompt = f"""
You are a hiring assistant.

User Request:
{user_input}

Format the API response accordingly.

STRICT RULES:
- DO NOT change or invent data
- DO NOT skip fields

FORMATTING RULES:
- If multiple records → show list/table
- If single record → structured readable format
- Keep response clean and readable

DATA LIMIT RULE:
- If more than 10 records → show only first 10

API Response:
{json.dumps(result)}
"""

    format_response = client.responses.create(
        model=MODEL_NAME,
        input=format_prompt
    )

    return format_response.output_text, meta