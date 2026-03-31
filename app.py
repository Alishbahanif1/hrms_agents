import streamlit as st
from agents.master_agent import run_master_agent

from utils.auth_manager import load_token, is_logged_in, get_token, logout
from auth_ui.login import show_login
from auth_ui.register import show_register
from auth_ui.forget_password import show_forgot_password
from auth_ui.change_password import show_change_password

# 🔹 Page config
st.set_page_config(page_title="HR AI Assistant", page_icon="🤖")

# 🔄 Load token FIRST
load_token()

# =========================
# 🔐 AUTH ROUTING
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
# 🧠 PAGE STATE (IMPORTANT)
# =========================

if "page" not in st.session_state:
    st.session_state["page"] = "chat"

# =========================
# 🚪 SIDEBAR
# =========================

st.sidebar.title("Menu")

if st.sidebar.button("💬 Chat"):
    st.session_state["page"] = "chat"
    st.rerun()

if st.sidebar.button("🔑 Change Password"):
    st.session_state["page"] = "change_password"
    st.rerun()

# 🧠 Logout confirmation state
if "confirm_logout" not in st.session_state:
    st.session_state["confirm_logout"] = False


# 🚪 Logout button
if st.sidebar.button("🚪 Logout"):
    st.session_state["confirm_logout"] = True


# ⚠️ Confirmation UI
if st.session_state["confirm_logout"]:
    st.sidebar.warning("Are you sure you want to logout?")

    col1, col2 = st.sidebar.columns(2)

    if col1.button("✅ Yes"):
        logout()
        st.session_state["confirm_logout"] = False
        st.rerun()

    if col2.button("❌ No"):
        st.session_state["confirm_logout"] = False
        st.rerun()

# =========================
# 🔀 PAGE ROUTING
# =========================

if st.session_state["page"] == "change_password":
    show_change_password()
    st.stop()

# =========================
# 🤖 MAIN APP (CHAT)
# =========================

token = get_token()

st.title("🤖 HR AI Assistant")
st.markdown("Create employees using natural language")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 🔹 Show history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 🔹 Input
user_input = st.chat_input("Type your request...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Thinking..."):
        try:
            response = run_master_agent(user_input, token)
        except Exception as e:
            response = f"❌ Error: {str(e)}"

    st.session_state.messages.append({
        "role": "assistant",
        "content": str(response)
    })

    with st.chat_message("assistant"):
        st.markdown(str(response))