# 🤖 HRMS Multi-Agent System

AI-powered HR assistant built with:
- Streamlit UI
- Azure OpenAI (Agents + Tool Calling)
- Multi-agent architecture (Master + HR)

---

## 🚀 Features

- Create employee using natural language
- Get all employees
- Get employee by ID
- Update employee
- Delete employee
- Master agent routing (HR / Sales / Admin ready)

---

## 🧠 Architecture



User Input
     │
     ▼
Master Agent (Intent Classification using LLM)
     │
     ├── Employee Agent → Employee Endpoints
     ├── Department Agent → Department Endpoints
     ├── Hiring Agent → Hiring Endpoints
     ├── Roles Agent → Roles Endpoints
     ├── Leave Agent → Leave Endpoints
     ├── Training Agent → Training Endpoints
     ├── Onboarding Agent → Onboarding Endpoints
     ├── Resignation Agent → Resignation Endpoints
     ├── Clearance Agent → Clearance Endpoints
     └── Format Agent → Response formatting