import streamlit as st
from agents.master_agent import run_master_agent
from core.config import ACCESS_TOKEN

token = ACCESS_TOKEN

# 🔹 Page config
st.set_page_config(page_title="HR AI Assistant", page_icon="🤖")

# 🔹 Title
st.title("🤖 HR AI Assistant")
st.markdown("Create employees using natural language")

# 🔹 Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🔹 Show history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 🔹 Input
user_input = st.chat_input("Type your request...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 🔥 Call agent safely
    with st.spinner("Thinking..."):
        try:
            response = run_master_agent(user_input, token)
        except Exception as e:
            response = f"❌ Error: {str(e)}"

    # Show bot response
    st.session_state.messages.append({
        "role": "assistant",
        "content": str(response)
    })

    with st.chat_message("assistant"):
        st.markdown(str(response))