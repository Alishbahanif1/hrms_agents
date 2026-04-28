from agents.base_agent import run_agent
from tools.hr_tools import *


# =========================
# 🔥 TOOLS (FIXED FORMAT)
# =========================

tools = [

    # =========================
    # 👤 EMPLOYEES
    # =========================
    {
        "type": "function",
        "name": "get_employees",
        "description": "Get all employees",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "type": "function",
        "name": "get_employee_by_id",
        "description": "Get employee by ID",
        "parameters": {
            "type": "object",
            "properties": {"employee_id": {"type": "integer"}},
            "required": ["employee_id"]
        }
    },
    {
        "type": "function",
        "name": "create_employee",
        "description": "Create employee",
        "parameters": {
            "type": "object",
            "properties": {
                "full_name": {"type": "string"},
                "email": {"type": "string"},
                "personal_email": {"type": "string"},
                "department_id": {"type": "integer"},
                "role_id": {"type": "integer"}
            },
            "required": ["full_name", "email", "personal_email", "department_id", "role_id"]
        }
    },
    {
        "type": "function",
        "name": "update_employee",
        "description": "Update employee",
        "parameters": {
            "type": "object",
            "properties": {
                "employee_id": {"type": "integer"},
                "full_name": {"type": "string"},
                "email": {"type": "string"},
                "personal_email": {"type": "string"},
                "department_id": {"type": "integer"},
                "role_id": {"type": "integer"}
            },
            "required": ["employee_id"]
        }
    },
    {
        "type": "function",
        "name": "delete_employee",
        "description": "Delete employee",
        "parameters": {
            "type": "object",
            "properties": {"employee_id": {"type": "integer"}},
            "required": ["employee_id"]
        }
    },

    # =========================
    # 🏢 DEPARTMENTS
    # =========================
    {
        "type": "function",
        "name": "get_departments",
        "description": "Get all departments",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "type": "function",
        "name": "get_department_by_id",
        "description": "Get department by ID",
        "parameters": {
            "type": "object",
            "properties": {"department_id": {"type": "integer"}},
            "required": ["department_id"]
        }
    },
    {
        "type": "function",
        "name": "create_department",
        "description": "Create department",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            },
            "required": ["name"]
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
            "properties": {"department_id": {"type": "integer"}},
            "required": ["department_id"]
        }
    },

    # =========================
    # 🧩 ROLES
    # =========================
    {
        "type": "function",
        "name": "get_roles",
        "description": "Get all roles",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "type": "function",
        "name": "get_role_by_id",
        "description": "Get role by ID",
        "parameters": {
            "type": "object",
            "properties": {"role_id": {"type": "integer"}},
            "required": ["role_id"]
        }
    },
    {
        "type": "function",
        "name": "create_role",
        "description": "Create role",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "level": {"type": "integer"},
                "description": {"type": "string"}
            },
            "required": ["title"]
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
                "description": {"type": "string"}
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
            "properties": {"role_id": {"type": "integer"}},
            "required": ["role_id"]
        }
    }
]


# =========================
# 🧠 TOOL MAP
# =========================

tool_map = {

    # Employees
    "get_employees": lambda args, token: get_employees(token),
    "get_employee_by_id": lambda args, token: get_employee(args["employee_id"], token),
    "create_employee": lambda args, token: create_employee(args, token),
    "update_employee": lambda args, token: update_employee(args["employee_id"], args, token),
    "delete_employee": lambda args, token: delete_employee(args["employee_id"], token),

    # Departments
    "get_departments": lambda args, token: get_departments(token),
    "get_department_by_id": lambda args, token: get_department(args["department_id"], token),
    "create_department": lambda args, token: create_department(args, token),
    "update_department": lambda args, token: update_department(args["department_id"], args, token),
    "delete_department": lambda args, token: delete_department(args["department_id"], token),

    # Roles
    "get_roles": lambda args, token: get_roles(token),
    "get_role_by_id": lambda args, token: get_role(args["role_id"], token),
    "create_role": lambda args, token: create_role(args, token),
    "update_role": lambda args, token: update_role(args["role_id"], args, token),
    "delete_role": lambda args, token: delete_role(args["role_id"], token),
}
# =========================
# 🚀 ENTRY
# =========================

def run_hr_agent(user_input: str, token: str):
    print("USER INPUT:", user_input)
    return run_agent(user_input, tools, tool_map, token)