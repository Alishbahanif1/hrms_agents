import json
from agents.base_agent import run_agent
from tools.employee_lifecycle_tools import *

# =========================
# Tool Definitions for LLM
# =========================
tools = [
    # Onboarding
    {
        "type": "function",
        "name": "list_onboarding",
        "description": "List all onboarding records",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "type": "function",
        "name": "get_onboarding",
        "description": "Get onboarding details by ID",
        "parameters": {"type": "object", "properties": {"onboarding_id": {"type": "integer"}}, "required": ["onboarding_id"]}
    },
    {
        "type": "function",
        "name": "update_onboarding",
        "description": "Update onboarding record",
        "parameters": {"type": "object", "properties": {"onboarding_id": {"type": "integer"}}, "required": ["onboarding_id"]}
    },
    {
        "type": "function",
        "name": "delete_onboarding",
        "description": "Delete onboarding record",
        "parameters": {"type": "object", "properties": {"onboarding_id": {"type": "integer"}}, "required": ["onboarding_id"]}
    },

    # Trainings
    {
        "type": "function",
        "name": "list_trainings",
        "description": "List all trainings",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "type": "function",
        "name": "get_training",
        "description": "Get training details by ID",
        "parameters": {"type": "object", "properties": {"training_id": {"type": "integer"}}, "required": ["training_id"]}
    },
    {
    "type": "function",
    "name": "create_training",
    "description": "Create a training for an employee",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "Title of the training"
            },
            "training_date": {
                "type": "string",
                "description": "Date in YYYY-MM-DD format"
            },
            "employee_id": {
                "type": "integer",
                "description": "Employee ID to assign training"
            }
        },
        "required": ["title", "training_date", "employee_id"]
    }
},
{
    "type": "function",
    "name": "get_training_assignments",
    "description": "Get employees assigned to a specific training",
    "parameters": {
        "type": "object",
        "properties": {
            "training_id": {"type": "integer", "description": "ID of the training"}
        },
        "required": ["training_id"]
    }
},
    {
        "type": "function",
        "name": "update_training",
        "description": "Update a training",
        "parameters": {"type": "object", "properties": {"training_id": {"type": "integer"}}, "required": ["training_id"]}
    },
    {
        "type": "function",
        "name": "delete_training",
        "description": "Delete a training",
        "parameters": {"type": "object", "properties": {"training_id": {"type": "integer"}}, "required": ["training_id"]}
    },

    # Resignations
    {
        "type": "function",
        "name": "list_resignations",
        "description": "List all resignations",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "type": "function",
        "name": "get_resignation",
        "description": "Get resignation by ID",
        "parameters": {"type": "object", "properties": {"resignation_id": {"type": "integer"}}, "required": ["resignation_id"]}
    },
    {
        "type": "function",
        "name": "create_resignation",
        "description": "Create a resignation",
        "parameters": {
            "type": "object",
            "properties": {
                "resignation_date": {
                    "type": "string",
                    "description": "Resignation date in YYYY-MM-DD format"
                },
                "notice_end_date": {
                    "type": "string",
                    "description": "Notice period end date in YYYY-MM-DD format"
                }
            },
            "required": ["resignation_date", "notice_end_date"]
        }
    },
    {
    "type": "function",
    "name": "update_resignation",
    "description": "Update a resignation",
    "parameters": {
        "type": "object",
        "properties": {
            "resignation_id": {
                "type": "integer",
                "description": "ID of resignation"
            },
            "manager_approved": {
                "type": "boolean",
                "description": "Whether manager approved"
            },
            "status": {
                "type": "string",
                "description": "Status like Approved, Pending, Rejected"
            }
        },
        "required": ["resignation_id"]
    }
    },
    {
        "type": "function",
        "name": "delete_resignation",
        "description": "Delete a resignation",
        "parameters": {"type": "object", "properties": {"resignation_id": {"type": "integer"}}, "required": ["resignation_id"]}
    },

    # Clearance
    {
        "type": "function",
        "name": "list_clearance",
        "description": "List all clearance records",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "type": "function",
        "name": "get_clearance",
        "description": "Get clearance by resignation ID",
        "parameters": {"type": "object", "properties": {"resignation_id": {"type": "integer"}}, "required": ["resignation_id"]}
    },
    {
        "type": "function",
        "name": "update_clearance",
        "description": "Update clearance details",
        "parameters": {"type": "object", "properties": {"resignation_id": {"type": "integer"}}, "required": ["resignation_id"]}
    },
    {
        "type": "function",
        "name": "delete_clearance",
        "description": "Delete a clearance record",
        "parameters": {"type": "object", "properties": {"resignation_id": {"type": "integer"}}, "required": ["resignation_id"]}
    }
]

# =========================
# Tool Map
# =========================
tool_map = {
    # Onboarding
    "list_onboarding": lambda args, token: list_onboarding(token),
    "get_onboarding": lambda args, token: get_onboarding(args["onboarding_id"], token),
    "update_onboarding": lambda args, token: update_onboarding(args["onboarding_id"], args, token),
    "delete_onboarding": lambda args, token: delete_onboarding(args["onboarding_id"], token),

    # Trainings
    "list_trainings": lambda args, token: list_trainings(token),
    "get_training": lambda args, token: get_training(args["training_id"], token),
    "create_training": lambda args, token: create_training({
    "title": args["title"],
    "training_date": args["training_date"],
    "assign_to": {
        "employees": args.get("employees", []),
        "departments": args.get("departments", []),
        "roles": args.get("roles", []),
        "managers": args.get("managers", []),
        "all_employees": args.get("all_employees", False)
    }
    }, token),
    "update_training": lambda args, token: update_training(args["training_id"], args, token),
    "delete_training": lambda args, token: delete_training(args["training_id"], token),
    "get_training_assignments": lambda args, token: get_training_assignments(args["training_id"], token),
    # Resignations
    "list_resignations": lambda args, token: list_resignations(token),
    "get_resignation": lambda args, token: get_resignation(args["resignation_id"], token),
    "create_resignation": lambda args, token: create_resignation(args, token),
    "update_resignation": lambda args, token: update_resignation(args["resignation_id"], args, token),
    "delete_resignation": lambda args, token: delete_resignation(args["resignation_id"], token),

    # Clearance
    "list_clearance": lambda args, token: list_clearance(token),
    "get_clearance": lambda args, token: get_clearance(args["resignation_id"], token),
    "update_clearance": lambda args, token: update_clearance(args["resignation_id"], args, token),
    "delete_clearance": lambda args, token: delete_clearance(args["resignation_id"], token),
}

# =========================
# Entry Point
# =========================
def run_employee_lifecycle_agent(user_input: str, token: str):
    print("USER INPUT:", user_input)
    from agents.base_agent import run_agent
    return run_agent(user_input, tools, tool_map, token)