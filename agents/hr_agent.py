import json
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

from core.config import AZURE_ENDPOINT, MODEL_NAME
from tools.employee_tools import (
    create_employee,
    get_employees,
    get_employee_by_id,
    update_employee,
    delete_employee
)

# 🔹 Azure client
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
            "properties": {
                "employee_id": {"type": "integer"}
            },
            "required": ["employee_id"]
        }
    },
    {
        "type": "function",
        "name": "update_employee",
        "description": "Update employee fields",
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
        "description": "Delete employee",
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
# 🚀 MAIN FUNCTION
# =========================

def run_hr_agent(user_input: str, token: str):

    response = client.responses.create(
        model=MODEL_NAME,
        input=user_input,
        tools=tools,
        tool_choice="auto"
    )

    output = response.output[0]

    if output.type == "function_call":

        tool_name = output.name
        args = json.loads(output.arguments)

        print("TOOL:", tool_name)
        print("ARGS:", args)

        if tool_name == "create_employee":
            result = create_employee(args, token)

        elif tool_name == "get_employees":
            result = get_employees(token)

        elif tool_name == "get_employee_by_id":
            result = get_employee_by_id(args["employee_id"], token)

        elif tool_name == "update_employee":
            employee_id = args.get("employee_id")
            data = {k: v for k, v in args.items() if k != "employee_id"}

            if not data:
                return "❌ Please specify fields to update"

            # normalize
            field_map = {
                "name": "full_name",
                "fullname": "full_name"
            }

            normalized_data = {
                field_map.get(k, k): v for k, v in data.items()
            }

            result = update_employee(employee_id, normalized_data, token)

        elif tool_name == "delete_employee":
            result = delete_employee(args["employee_id"], token)

        else:
            return "❌ Unknown tool"

        # 🔁 Send tool result back to LLM
        final_response = client.responses.create(
            model=MODEL_NAME,
            previous_response_id=response.id,
            input=[
                {
                    "type": "function_call_output",
                    "call_id": output.call_id,
                    "output": json.dumps(result)
                }
            ]
        )

        return final_response.output_text

    return response.output_text