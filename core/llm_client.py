from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from core.config import AZURE_ENDPOINT

# Single shared client (GLOBAL)
project_client = AIProjectClient(
    endpoint=AZURE_ENDPOINT,
    credential=DefaultAzureCredential()
)

client = project_client.get_openai_client()