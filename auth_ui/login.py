import streamlit as st
from utils.api_client import login_api
from utils.auth_manager import save_token


def show_login():
    # =========================
    # 🎨 STYLE
    # =========================
    st.markdown(
        """
        <style>
        .login-title {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # =========================
    # 🪪 LOGIN UI
    # =========================
    st.markdown('<div class="login-title">🔐 Login</div>', unsafe_allow_html=True)

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns([1, 1])

    login_clicked = col1.button("Login")
    register_clicked = col2.button("Sign Up")

    forgot_clicked = st.button("Forgot Password?")

    # =========================
    # 🔐 LOGIN LOGIC
    # =========================
    if login_clicked:
        if not email or not password:
            st.error("Please fill all fields")
        else:
            with st.spinner("Logging in..."):
                response, status = login_api(email, password)

            if status == 200:
                data = response.get("data")

                if data and "access_token" in data:
                    token = data["access_token"]

                    # ✅ SET PAGE BEFORE saving token
                    st.session_state["page"] = "chat"

                    # ✅ This handles rerun internally
                    save_token(token)

                    st.success("Login successful 🎉")

                else:
                    st.error(f"Unexpected response format: {response}")

            else:
                error_msg = (
                    response.get("detail")
                    or response.get("message")
                    or str(response)
                )
                st.error(error_msg)

    # =========================
    # 🔁 NAVIGATION
    # =========================
    if register_clicked:
        st.session_state["auth_page"] = "register"
        st.rerun()

    if forgot_clicked:
        st.session_state["auth_page"] = "forgot"
        st.rerun()