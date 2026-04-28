from agents.base_agent import run_agent
from tools.hiring_tools import *


# =========================
# 🔥 TOOL SCHEMA
# =========================

tools = [

    # =========================
    # 🧾 HIRING REQUESTS
    # =========================
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
                "budget_range": {"type": "string"},
                "jd_text": {"type": "string"}
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
        "description": "Fetch all hiring requests created for recruitment (NOT employees)",
        "parameters": {"type": "object", "properties": {}}
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
        "description": "Update hiring request, manager status can be approved/rejected/pending, status can be open/closed",
        "parameters": {
            "type": "object",
            "properties": {
                "hiring_id": {"type": "integer"},
                "manager_approved": {"type": "boolean"},
                "status": {"type": "string"},
                "jd_text": {"type": "string"}
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
    # 📢 JOB POSTINGS
    # =========================
    {
        "type": "function",
        "name": "create_job_posting",
        "description": "Create job posting",
        "parameters": {
            "type": "object",
            "properties": {
                "hiring_request_id": {"type": "integer"},
                "posted_date": {"type": "string"},
                "closing_date": {"type": "string"}
            },
            "required": ["hiring_request_id"]
        }
    },
    {
        "type": "function",
        "name": "get_job_postings",
        "description": "Fetch job postings created from hiring requests (NOT roles, NOT employees)",
        "parameters": {"type": "object", "properties": {}}
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
                "status": {"type": "string"},
                "closing_date": {"type": "string"}
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
# 🧠 TOOL MAP
# =========================

def handle_update_hiring(args, token):
    hiring_id = args.get("hiring_id")
    data = {k: v for k, v in args.items() if k != "hiring_id"}
    return update_hiring_request(hiring_id, data, token)


def handle_update_job_posting(args, token):
    posting_id = args.get("posting_id")
    data = {k: v for k, v in args.items() if k != "posting_id"}
    return update_job_posting(posting_id, data, token)


tool_map = {

    # Hiring Requests
    "create_hiring_request": lambda args, token: create_hiring_request(args, token),
    "get_hiring_requests": lambda args, token: get_hiring_requests(token),
    "get_hiring_request_by_id": lambda args, token: get_hiring_request_by_id(args["hiring_id"], token),
    "update_hiring_request": handle_update_hiring,
    "delete_hiring_request": lambda args, token: delete_hiring_request(args["hiring_id"], token),

    # Job Postings
    "create_job_posting": lambda args, token: create_job_posting(args, token),
    "get_job_postings": lambda args, token: get_job_postings(token),
    "get_job_posting_by_id": lambda args, token: get_job_posting_by_id(args["posting_id"], token),
    "update_job_posting": handle_update_job_posting,
    "delete_job_posting": lambda args, token: delete_job_posting(args["posting_id"], token),
}


# =========================
# 🚀 ENTRY POINT
# =========================

def run_hiring_agent(user_input: str, token: str):
    return run_agent(user_input, tools, tool_map, token)