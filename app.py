import streamlit as st
import uuid

from agents.master_agent import run_master_agent
from core.config import ACCESS_TOKEN

token = ACCESS_TOKEN

st.set_page_config(page_title="HR AI Assistant", page_icon="🤖")

st.title("🤖 HR AI Assistant")
st.markdown("Context-aware HR system")

# session id
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# display history
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
            response = run_master_agent(
                user_input,
                token,
                st.session_state.session_id
            )
        except Exception as e:
            response = f"❌ Error: {str(e)}"

    st.session_state.messages.append({
        "role": "assistant",
        "content": str(response)
    })

    with st.chat_message("assistant"):
        st.markdown(str(response))