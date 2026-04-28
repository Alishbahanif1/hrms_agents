import streamlit as st
import pandas as pd

from agents.master_agent import run_master_agent

from utils.auth_manager import load_token, is_logged_in, get_token, logout
from auth_ui.login import show_login
from auth_ui.register import show_register
from auth_ui.forget_password import show_forgot_password
from auth_ui.change_password import show_change_password

# HR
from tools.hr_tools import get_employees, get_departments, get_roles

# Leave
from tools.leave_tools import (
    get_leave_types,
    get_leave_requests,
    get_leave_balances
)

# Hiring
from tools.hiring_tools import (
    get_hiring_requests,
    get_job_postings
)

# Lifecycle
from tools.employee_lifecycle_tools import (
    list_onboarding,
    list_trainings,
    list_resignations
)

# =========================
# 🔹 CONFIG
# =========================
st.set_page_config(page_title="HR AI Assistant", page_icon="🤖")

load_token()

# =========================
# 🔐 AUTH
# =========================
if "auth_page" not in st.session_state:
    st.session_state["auth_page"] = "login"

if not is_logged_in():
    if st.session_state["auth_page"] == "login":
        show_login()
    elif st.session_state["auth_page"] == "register":
        show_register()
    elif st.session_state["auth_page"] == "forgot":
        show_forgot_password()
    st.stop()

# =========================
# 🧠 STATE
# =========================
if "page" not in st.session_state:
    st.session_state["page"] = "💬 Chat"

if "pagination" not in st.session_state:
    st.session_state["pagination"] = {}

# =========================
# 🚪 SIDEBAR
# =========================
st.sidebar.title("📊 HR System")

page = st.sidebar.radio(
    "Navigate",
    [
        "💬 Chat",
        "👤 Employees",
        "🏢 Departments",
        "🧩 Roles",
        "🧾 Leave Types",
        "📊 Leave Balances",
        "📝 Leave Requests",
        "📢 Hiring Requests",
        "📌 Job Postings",
        "🚀 Onboarding",
        "🎓 Trainings",
        "📄 Resignations",
        "🔑 Change Password"
    ]
)

st.session_state["page"] = page

if st.sidebar.button("🚪 Logout"):
    logout()
    st.rerun()

# =========================
# 🔀 ROUTING
# =========================
if page == "🔑 Change Password":
    show_change_password()
    st.stop()

# =========================
# 📊 TABLE RENDER WITH PAGINATION
# =========================
token = get_token()

def get_page(key):
    return st.session_state["pagination"].get(key, 1)

def set_page(key, value):
    st.session_state["pagination"][key] = value

def render_table(title, response, key):
    st.title(title)

    if not response:
        st.error("Empty response")
        return

    rows = []
    meta = {}

    try:
        if response.get("success"):
            inner = response.get("data", {})
            inner_data = inner.get("data", {})

            if "items" in inner_data:
                rows = inner_data["items"]
                meta = inner_data

    except Exception as e:
        st.error(f"Parsing error: {str(e)}")
        return

    if not rows:
        st.warning("No data available")
        return

    df = pd.DataFrame(rows)

    drop_cols = ["created_by", "updated_by", "deleted_by", "deleted_at"]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    if "is_active" in df.columns:
        df["is_active"] = df["is_active"].map({
            True: "✅ Active",
            False: "❌ Inactive"
        })

    st.dataframe(df, use_container_width=True, hide_index=True)

    # =========================
    # 🔥 PAGINATION UI
    # =========================
    current = meta.get("page", 1)
    total_pages = meta.get("pages", 1)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("⬅️ Previous", key=f"{key}_prev"):
            if current > 1:
                set_page(key, current - 1)
                st.rerun()

    with col2:
        st.markdown(f"**Page {current} / {total_pages}**")

    with col3:
        if st.button("➡️ Next", key=f"{key}_next"):
            if current < total_pages:
                set_page(key, current + 1)
                st.rerun()

# =========================
# 👤 HR
# =========================
if page == "👤 Employees":
    render_table("Employees", get_employees(token, page=get_page("employees")), "employees")
    st.stop()

if page == "🏢 Departments":
    render_table("Departments", get_departments(token, page=get_page("departments")), "departments")
    st.stop()

if page == "🧩 Roles":
    render_table("Roles", get_roles(token, page=get_page("roles")), "roles")
    st.stop()

# =========================
# 🧾 LEAVE
# =========================
if page == "🧾 Leave Types":
    render_table("Leave Types", get_leave_types(token, page=get_page("leave_types")), "leave_types")
    st.stop()

if page == "📊 Leave Balances":
    render_table("Leave Balances", get_leave_balances(token, page=get_page("leave_balances")), "leave_balances")
    st.stop()

if page == "📝 Leave Requests":
    render_table("Leave Requests", get_leave_requests(token, page=get_page("leave_requests")), "leave_requests")
    st.stop()

# =========================
# 📢 HIRING
# =========================
if page == "📢 Hiring Requests":
    render_table("Hiring Requests", get_hiring_requests(token, page=get_page("hiring")), "hiring")
    st.stop()

if page == "📌 Job Postings":
    render_table("Job Postings", get_job_postings(token, page=get_page("jobs")), "jobs")
    st.stop()

# =========================
# 🚀 LIFECYCLE
# =========================
if page == "🚀 Onboarding":
    render_table("Onboarding", list_onboarding(token, page=get_page("onboarding")), "onboarding")
    st.stop()

if page == "🎓 Trainings":
    render_table("Trainings", list_trainings(token, page=get_page("training")), "training")
    st.stop()

if page == "📄 Resignations":
    render_table("Resignations", list_resignations(token, page=get_page("resignations")), "resignations")
    st.stop()

# =========================
# 🤖 CHAT
# =========================
st.title("🤖 HR AI Assistant")
st.markdown("Manage employees, onboarding, leaves, and more using natural language.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your request...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Thinking..."):
        try:
            response = run_master_agent(user_input, token)
        except Exception as e:
            response = {"success": False, "error": str(e)}

    if isinstance(response, dict):
        if response.get("success"):
            content = str(response.get("data"))
        else:
            error = response.get("error")
            if isinstance(error, dict):
                error = error.get("detail") or str(error)
            content = f"❌ {error}"
    else:
        content = str(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": content
    })

    with st.chat_message("assistant"):
        st.markdown(content)