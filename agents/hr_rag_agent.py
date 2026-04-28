from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

from core.config import (
    AZURE_ENDPOINT,
    HR_RAG_AGENT_NAME,
    HR_RAG_AGENT_VERSION
)

# =========================
# 🔹 Azure client
# =========================

project_client = AIProjectClient(
    endpoint=AZURE_ENDPOINT,
    credential=DefaultAzureCredential(),
)

openai_client = project_client.get_openai_client()


# =========================
# 🚀 ENTRY
# =========================

def run_hr_agent(user_input: str):
    try:

        response = openai_client.responses.create(
        input=user_input,  # ✅ simpler + matches playground
        extra_body={
            "agent_reference": {
                "name": HR_RAG_AGENT_NAME,
                "version": HR_RAG_AGENT_VERSION,
                "type": "agent_reference"
            }
        }
    )

        return response.output_text

    except Exception as e:
        return f"⚠️ HR agent failed: {str(e)}"