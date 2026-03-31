import json
from core.config import MODEL_NAME, AZURE_ENDPOINT
from agents.hr_agent import run_hr_agent
from agents.onboarding_agent import run_onboarding_agent

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# 🔹 Azure client
project_client = AIProjectClient(
    endpoint=AZURE_ENDPOINT,
    credential=DefaultAzureCredential()
)

client = project_client.get_openai_client()


# =========================
# 🧠 ROUTER
# =========================
def detect_module(user_input: str):

    response = client.responses.create(
        model=MODEL_NAME,
        input=f"""
Classify user request into one module.

Modules:
- hr → employees, hiring, salary, leave
- onboarding → onboarding, new employee setup, joining process
- sales → customers, orders
- admin → operations

Return ONLY JSON:
{{ "module": "hr" }}

User: {user_input}
"""
    )

    text = response.output_text.strip()

    print("ROUTER OUTPUT:", text)

    try:
        data = json.loads(text)
        return data.get("module", "hr")
    except:
        return "hr"


# =========================
# 🚀 MASTER EXECUTION
# =========================
def run_master_agent(user_input: str, token: str):

    module = detect_module(user_input)

    print("ROUTED TO:", module)

    if module == "hr":
        return run_hr_agent(user_input, token)
    
    elif module == "onboarding":
        return run_onboarding_agent(user_input, token)

    elif module == "sales":
        return "🚧 Sales module coming soon"

    elif module == "admin":
        return "🚧 Admin module coming soon"

    return "❌ Could not determine module"