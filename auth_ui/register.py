import streamlit as st
from utils.auth_api import register_api   # ✅ fixed import


def show_register():
    # =========================
    # 🎨 STYLE
    # =========================
    st.markdown(
        """
        <style>
        .register-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 80vh;
        }
        .register-card {
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0px 4px 20px rgba(0,0,0,0.1);
            width: 350px;
            background-color: #ffffff;
        }
        .register-title {
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
    # 📝 UI
    # =========================
    st.markdown('<div class="register-title">📝 Register</div>', unsafe_allow_html=True)

    invite_token = st.text_input("Invite Token")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    col1, col2 = st.columns([1, 1])

    register_clicked = col1.button("Register")
    back_clicked = col2.button("Back to Login")

    # =========================
    # 🧠 LOGIC
    # =========================
    if register_clicked:
        if not invite_token or not password or not confirm_password:
            st.error("All fields are required")

        elif password != confirm_password:
            st.error("Passwords do not match")

        else:
            with st.spinner("Creating account..."):
                response = register_api(invite_token, password)

            if response["success"]:
                st.success("✅ Account created successfully!")

                st.session_state["auth_page"] = "login"
                st.rerun()

            else:
                error_msg = response.get("error") or "Registration failed"

                if isinstance(error_msg, dict):
                    error_msg = error_msg.get("detail") or str(error_msg)

                st.error(error_msg)

    # =========================
    # 🔙 NAVIGATION
    # =========================
    if back_clicked:
        st.session_state["auth_page"] = "login"
        st.rerun()