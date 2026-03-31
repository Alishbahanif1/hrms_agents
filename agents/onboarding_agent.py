# =========================
# 📦 IMPORTS
# =========================
import json
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# 🔹 Config
from core.config import AZURE_ENDPOINT, MODEL_NAME

# 🔹 (We will create these in next step)
from tools.onboarding_tools import (
    create_onboarding,
    get_onboardings,
    get_onboarding_by_id,
    update_onboarding,
    delete_onboarding
)


# =========================
# 🔌 AZURE CLIENT SETUP
# =========================
project_client = AIProjectClient(
    endpoint=AZURE_ENDPOINT,
    credential=DefaultAzureCredential()
)

client = project_client.get_openai_client()


# =========================
# 🛠️ TOOL SCHEMA
# =========================
# ⚠️ Keep generic for now (no backend deep dive)
tools = [
    {
        "type": "function",
        "name": "create_onboarding",
        "description": "Create onboarding record for employee",
        "parameters": {
            "type": "object",
            "properties": {
                "employee_id": {"type": "integer"},
                "start_date": {"type": "string"},
                "status": {"type": "string"}
            },
            "required": ["employee_id"]
        }
    },
    {
        "type": "function",
        "name": "get_onboardings",
        "description": "Get all onboarding records",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "type": "function",
        "name": "get_onboarding_by_id",
        "description": "Get onboarding by ID",
        "parameters": {
            "type": "object",
            "properties": {
                "onboarding_id": {"type": "integer"}
            },
            "required": ["onboarding_id"]
        }
    },
    {
    "type": "function",
    "name": "update_onboarding",
    "description": "Update onboarding record",
    "parameters": {
        "type": "object",
        "properties": {
            "onboarding_id": {"type": "integer"},
            "appointment_letter_generated": {"type": "boolean"},
            "email_created": {"type": "boolean"},
            "resources_allocated": {"type": "boolean"},
            "orientation_sent": {"type": "boolean"},
            "is_active": {"type": "boolean"}
        },
        "required": ["onboarding_id"]
    }
},
    {
        "type": "function",
        "name": "delete_onboarding",
        "description": "Delete onboarding record",
        "parameters": {
            "type": "object",
            "properties": {
                "onboarding_id": {"type": "integer"}
            },
            "required": ["onboarding_id"]
        }
    }
]


# =========================
# 🚀 MAIN FUNCTION
# =========================
def run_onboarding_agent(user_input: str, token: str):

    # 🔹 Send user input to model
    response = client.responses.create(
        model=MODEL_NAME,
        input=user_input,
        tools=tools,
        tool_choice="auto"
    )

    output = response.output[0]

    # =========================
    # 🔁 HANDLE TOOL CALL
    # =========================
    if output.type == "function_call":

        tool_name = output.name
        # 🔹 Safe JSON parsing
        try:
            args = json.loads(output.arguments or "{}")
        except Exception as e:
            return f"❌ Failed to parse arguments: {str(e)}"

        print("TOOL:", tool_name)
        print("ARGS:", args)

        # 🔹 Route to correct function
        if tool_name == "create_onboarding":
            result = create_onboarding(args, token)

        elif tool_name == "get_onboardings":
            result = get_onboardings(token)

        elif tool_name == "get_onboarding_by_id":
            result = get_onboarding_by_id(args["onboarding_id"], token)

        elif tool_name == "update_onboarding":
            onboarding_id = args.get("onboarding_id")
            data = {k: v for k, v in args.items() if k != "onboarding_id"}

            if not data:
                return "❌ Please specify fields to update"

            result = update_onboarding(onboarding_id, data, token)

        elif tool_name == "delete_onboarding":
            result = delete_onboarding(args["onboarding_id"], token)

        else:
            return "❌ Unknown tool"

        # =========================
        # 🔁 SEND TOOL RESULT BACK TO LLM
        # =========================
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

    # 🔹 If no tool used
    return response.output_text