from agents.base_agent import run_agent
from tools.leave_tools import *


# =========================
# 🔥 TOOL SCHEMA
# =========================
tools = [

    # =========================
    # 🧾 LEAVE TYPES
    # =========================
    {
        "type": "function",
        "name": "create_leave_type",
        "description": "Create leave type",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "default_allocation": {"type": "integer"},
                "is_active": {"type": "boolean"}
            },
            "required": ["name", "default_allocation", "is_active"]
        }
    },
    {
        "type": "function",
        "name": "get_leave_types",
        "description": "Get all leave types",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "type": "function",
        "name": "get_leave_type_by_id",
        "description": "Get leave type by ID",
        "parameters": {
            "type": "object",
            "properties": {"leave_type_id": {"type": "integer"}},
            "required": ["leave_type_id"]
        }
    },
    {
        "type": "function",
        "name": "update_leave_type",
        "description": "Update leave type",
        "parameters": {
            "type": "object",
            "properties": {
                "leave_type_id": {"type": "integer"},
                "name": {"type": "string"},
                "default_allocation": {"type": "integer"},
                "is_active": {"type": "boolean"}
            },
            "required": ["leave_type_id"]
        }
    },
    {
        "type": "function",
        "name": "delete_leave_type",
        "description": "Delete leave type",
        "parameters": {
            "type": "object",
            "properties": {"leave_type_id": {"type": "integer"}},
            "required": ["leave_type_id"]
        }
    },

    # =========================
    # 📊 LEAVE BALANCES
    # =========================
    {
        "type": "function",
        "name": "create_leave_balance",
        "description": "Create leave balance for employee",
        "parameters": {
            "type": "object",
            "properties": {
                "employee_id": {"type": "integer"},
                "leave_type_id": {"type": "integer"},
                "total_leaves": {"type": "integer"}
            },
            "required": ["employee_id", "leave_type_id", "total_leaves"]
        }
    },
    {
        "type": "function",
        "name": "get_leave_balances",
        "description": "Get all leave balances",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "type": "function",
        "name": "get_employee_balances",
        "description": "Get leave balances of an employee",
        "parameters": {
            "type": "object",
            "properties": {"employee_id": {"type": "integer"}},
            "required": ["employee_id"]
        }
    },
    {
        "type": "function",
        "name": "update_leave_balance",
        "description": "Update leave balance",
        "parameters": {
            "type": "object",
            "properties": {
                "balance_id": {"type": "integer"},
                "total_leaves": {"type": "integer"},
                "used_leaves": {"type": "integer"},
                "is_active": {"type": "boolean"}
            },
            "required": ["balance_id"]
        }
    },

    # =========================
    # 📝 LEAVE REQUESTS
    # =========================
    {
        "type": "function",
        "name": "create_leave_request",
        "description": "Create leave request",
        "parameters": {
            "type": "object",
            "properties": {
                "leave_type_id": {"type": "integer"},
                "start_date": {
                    "type": "string",
                    "description": "Date in YYYY-MM-DD format"
                },
                "end_date": {
                    "type": "string",
                    "description": "Date in YYYY-MM-DD format"
                },
                "reason": {"type": "string"}
            },
            "required": ["leave_type_id", "start_date", "end_date"]
        }
    },
    {
        "type": "function",
        "name": "get_leave_requests",
        "description": "Get all leave requests",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "type": "function",
        "name": "get_leave_request_by_id",
        "description": "Get leave request by ID",
        "parameters": {
            "type": "object",
            "properties": {"leave_id": {"type": "integer"}},
            "required": ["leave_id"]
        }
    },
    {
        "type": "function",
        "name": "update_leave_request",
        "description": "Update leave request status",
        "parameters": {
            "type": "object",
            "properties": {
                "leave_id": {"type": "integer"},
                "status": {
                    "type": "string",
                    "enum": ["Pending", "Approved", "Rejected", "Cancelled"]
                }
            },
            "required": ["leave_id"]
        }
    },
    {
        "type": "function",
        "name": "delete_leave_request",
        "description": "Delete leave request",
        "parameters": {
            "type": "object",
            "properties": {"leave_id": {"type": "integer"}},
            "required": ["leave_id"]
        }
    }
]

# =========================
# 🧠 TOOL MAP
# =========================

tool_map = {

    # =========================
    # LEAVE TYPES
    # =========================
    "create_leave_type": lambda args, token: create_leave_type(args, token),
    "get_leave_types": lambda args, token: get_leave_types(token),
    "get_leave_type_by_id": lambda args, token: get_leave_type(args["leave_type_id"], token),
    "update_leave_type": lambda args, token: update_leave_type(args["leave_type_id"], args, token),
    "delete_leave_type": lambda args, token: delete_leave_type(args["leave_type_id"], token),

    # =========================
    # LEAVE BALANCES
    # =========================
    "create_leave_balance": lambda args, token: create_leave_balance(args, token),
    "get_leave_balances": lambda args, token: get_leave_balances(token),
    "get_employee_balances": lambda args, token: get_employee_balances(args["employee_id"], token),
    "update_leave_balance": lambda args, token: update_leave_balance(args["balance_id"], args, token),

    # =========================
    # LEAVE REQUESTS
    # =========================
    "create_leave_request": lambda args, token: create_leave_request(args, token),
    "get_leave_requests": lambda args, token: get_leave_requests(token),
    "get_leave_request_by_id": lambda args, token: get_leave_request(args["leave_id"], token),
    "update_leave_request": lambda args, token: update_leave_request(args["leave_id"], args, token),
    "delete_leave_request": lambda args, token: delete_leave_request(args["leave_id"], token),
}


# =========================
# 🚀 ENTRY
# =========================

def run_leave_agent(user_input: str, token: str):
    return run_agent(user_input, tools, tool_map, token)