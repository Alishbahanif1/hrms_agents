# API_BASE_URL = "https://capstone-mari-production-bc2a.up.railway.app"
# # API_BASE_URL = "https://unconserved-abortedly-long.ngrok-free.dev"
# # put your real token here (or load dynamically later)
# # API_BASE_URL="http://127.0.0.1:8000"
# ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJlbXBsb3llZV9pZCI6MSwiZXhwIjoxNzc0NjAwOTgxfQ.GDyDHFyV9_UtbUz7a82iW4ADXDvaKmXzsIy2P7RJG3s"
# # Azure
# AZURE_ENDPOINT = "https://fr1sweden.services.ai.azure.com/api/projects/proj-default"
# MODEL_NAME = "gpt-4o"
# AGENT_NAME = "hr-agent"
# HR_RAG_AGENT_NAME="hrRagAgent"
# HR_RAG_AGENT_VERSION="10"
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
MODEL_NAME = os.getenv("MODEL_NAME")
AGENT_NAME = os.getenv("AGENT_NAME")
HR_RAG_AGENT_NAME = os.getenv("HR_RAG_AGENT_NAME")
HR_RAG_AGENT_VERSION = os.getenv("HR_RAG_AGENT_VERSION")