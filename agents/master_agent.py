import json
import uuid
from collections import defaultdict, deque

# =========================
# LLM / Azure
# =========================
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from core.config import AZURE_ENDPOINT, HR_RAG_AGENT_NAME, HR_RAG_AGENT_VERSION, MODEL_NAME

# =========================
# Agents
# =========================
from agents.hr_agent import run_hr_agent
from agents.hiring_agent import run_hiring_agent
from agents.leave_agent import run_leave_agent
from agents.employee_lifecycle_agent import run_employee_lifecycle_agent
from agents.hr_rag_agent import run_hr_agent as run_hr_rag

# =========================
# Azure client
# =========================
project_client = AIProjectClient(
    endpoint=AZURE_ENDPOINT,
    credential=DefaultAzureCredential(),
)
openai_client = project_client.get_openai_client()

# =========================
# 🧠 MEMORY (last 10 messages)
# =========================
conversation_memory = defaultdict(lambda: deque(maxlen=10))


def update_memory(session_id: str, user_input: str, response: str):
    conversation_memory[session_id].append({
        "user": user_input,
        "assistant": response
    })


def get_memory(session_id: str):
    return list(conversation_memory[session_id])


# =========================
# Router
# =========================
def detect_module(user_input: str):
    """
    Uses LLM to detect module and query type.
    Returns: (module:str, query_type:str)
    """
    trace_id = str(uuid.uuid4())
    print(f"[{trace_id}] ROUTER START")

    try:
        response = openai_client.responses.create(
            model=MODEL_NAME,
            input=f"""
        You are a routing assistant for an HR system.
        you can route to either knowledge assistant or action agents to perform diffrent hr action
        

        Your job is to:
        1. Select the correct module
        2. Select query type

        ---

        MODULE DEFINITIONS:

        - hr:
          employees, departments, roles, policy realted question

        - hiring:
          hiring requests, job postings, recruitment

        - leave:
          leave, leave types, leave requests, leave balances, vacation, sick leave

        - lifecycle:
          onboarding, training, resignations, clearance

        - sales:
          sales-related queries

        - admin:
          system administration

        ---

        QUERY TYPES:

        - action:
          create, update, delete, get, list, fetch, retrieve

        - knowledge:
          explain, what is, policy, rules, guidelines, information related to any policy

        ---

        STRICT RULES:
        STRICT RULES:

        1. If the query is about POLICY, RULES, GUIDELINES, or INFORMATION
           (keywords: "policy", "rules", "what is", "explain", "guidelines", "information"):
           → module MUST be "hr"
           → type MUST be "knowledge"

        2. If the query is about performing an ACTION
           (keywords: "create", "add", "update", "delete", "apply", "request", "submit"):
           → type MUST be "action"

        3. If the query is about LEAVE ACTIONS:
           (e.g., "apply leave", "request leave", "check leave balance")
           → module MUST be "leave"
           → type MUST be "action"

        4. If the query contains:
           "employee", "department", "role"
           → module = "hr"

        5. If the query contains:
           "hiring", "job", "posting", "recruitment"
           → module = "hiring"

        6. If the query contains:
           "onboarding", "training", "resignation", "clearance"
           → module = "lifecycle"

        7. IMPORTANT OVERRIDE:
           If both "leave" AND "policy" appear in the query:
           → module MUST be "hr"
           → type = "knowledge"

        8. If the user input is greeting or casual:
           → return:
           {{
             "module": "conversation",
             "type": "general"
           }}

        9. If nothing matches:
           → return:
           {{
             "module": "unknown",
             "type": "general"
           }}

        ---
        If the user input is:
        - Greeting (hi, hello, hey)
        - Casual conversation
        → return:
        {{
          "module": "conversation",
          "type": "general"
        }}
        If the query does NOT match any module:
        → return:
        {{
          "module": "unknown",
          "type": "general"
        }}

        User: {user_input}

        Return ONLY JSON:
        {{
          "module": "...",
          "type": "..."
        }}
        do not answer any other question except whats defined above 
        """
        )

        text = response.output_text.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        print(f"[{trace_id}] ROUTER OUTPUT:", text)

        try:
            data = json.loads(text)
            return data.get("module", "hr"), data.get("type", "knowledge")
        except Exception:
            return "hr", "knowledge"

    except Exception as e:
        print(f"[{trace_id}] ROUTER ERROR:", str(e))
        return "hr", "knowledge"

def build_context(session_id: str, user_input: str):
    history = conversation_memory[session_id]

    formatted = ""
    for item in history:
        formatted += f"User: {item['user']}\nAssistant: {item['assistant']}\n"

    return f"""
Previous conversation:
{formatted}

Current user:
{user_input}
"""
# =========================
# MASTER EXECUTION
# =========================
def run_master_agent(user_input: str, token: str = None, session_id: str = "default"):
    trace_id = str(uuid.uuid4())
    print(f"[{trace_id}] MASTER START")
    print(f"[{trace_id}] USER INPUT:", user_input)

    contextual_input = build_context(session_id, user_input)
    module, query_type = detect_module(contextual_input)
    print(f"[{trace_id}] ROUTED TO: {module} ({query_type})")

    try:
        if module == "hr":
            if query_type == "knowledge":
                print(f"[{trace_id}] USING RAG AGENT")
                result = run_hr_rag(contextual_input)
            else:
                print(f"[{trace_id}] USING BACKEND HR AGENT")
                result = run_hr_agent(contextual_input, token)

        elif module == "hiring":
            result = run_hiring_agent(contextual_input, token)

        elif module == "leave":
            result = run_leave_agent(contextual_input, token)

        elif module == "lifecycle":
            result = run_employee_lifecycle_agent(contextual_input, token)
            # 
        elif module=="conversation":
                response = openai_client.responses.create(
                model=MODEL_NAME,
                input=f"""
            
            You are a friendly HR assistant.

            you greet people very well and tell them that you can handle hr tasks like creating employee, creating departments and listing them etc

            User: {user_input}

            Respond naturally:
            - Mention you handle HR tasks (employees, hiring, leaves, onboarding)
            - Keep it conversational and human-like and short
            """
            )
                return response.output_text

        elif module == "unknown":
            response = openai_client.responses.create(
                model=MODEL_NAME,
                input=f"""
            You are a friendly HR assistant.

            The user asked something outside your capabilities.

            User: {user_input}

            Respond naturally:
            - Politely say you can't help with this
            - Mention you handle HR tasks
            """
            )
            return response.output_text

        else:
            response = openai_client.responses.create(
                model=MODEL_NAME,
                input=f"""
            You are a friendly HR assistant.

            User: {user_input}

            Respond naturally.
            """
            )
            return response.output_text

        # =========================
        # 🧠 SAVE MEMORY (ONLY CHANGE)
        # =========================
        update_memory(session_id, user_input, str(result))

        print(f"[{trace_id}] RESULT:", result)
        return result

    except Exception as e:
        print(f"[{trace_id}] ERROR:", str(e))
        return "⚠️ Something went wrong"


# =========================
# Placeholder
# =========================
def extract_entities(text: str):
    return []