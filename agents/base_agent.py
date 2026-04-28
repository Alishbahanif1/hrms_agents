import json
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from core.config import AZURE_ENDPOINT, MODEL_NAME


# =========================
# 🔹 Azure Client
# =========================
project_client = AIProjectClient(
    endpoint=AZURE_ENDPOINT,
    credential=DefaultAzureCredential()
)

client = project_client.get_openai_client()


# =========================
# 🚀 GENERIC AGENT RUNNER
# =========================
def run_agent(user_input: str, tools, tool_map, token: str):

    response = client.responses.create(
        model=MODEL_NAME,
        input=user_input,
        tools=tools,
        tool_choice="auto"
    )

    print("RAW RESPONSE:", response.output)

    while True:

        # =========================
        # 🔍 COLLECT ALL TOOL CALLS
        # =========================
        tool_calls = [
            item for item in response.output
            if getattr(item, "type", "") == "function_call"
        ]

        # =========================
        # 🧠 NO TOOL CALLS → DONE
        # =========================
        if not tool_calls:
            return response.output_text

        tool_outputs = []

        # =========================
        # ⚙️ EXECUTE ALL TOOLS
        # =========================
        for call in tool_calls:
            tool_name = call.name
            args = json.loads(call.arguments or "{}")

            print("TOOL:", tool_name)
            print("ARGS:", args)

            if tool_name not in tool_map:
                result = {"success": False, "error": "Unknown tool"}
            else:
                try:
                    result = tool_map[tool_name](args, token)
                except Exception as e:
                    result = {"success": False, "error": str(e)}

            print("TOOL RESULT:", result)

            tool_outputs.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": json.dumps(result)
            })

        # =========================
        # 🔁 SEND ALL RESULTS BACK
        # =========================
        response = client.responses.create(
            model=MODEL_NAME,
            previous_response_id=response.id,
            input=tool_outputs
        )