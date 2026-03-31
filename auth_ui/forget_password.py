import streamlit as st
from utils.api_client import (
    forgot_password_api,
    verify_otp_api,
    reset_password_api
)


def show_forgot_password():
    # =========================
    # 🎨 STYLE
    # =========================
    st.markdown(
        """
        <style>
        .forgot-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 80vh;
        }
        .forgot-card {
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0px 4px 20px rgba(0,0,0,0.1);
            width: 350px;
            background-color: #ffffff;
        }
        .forgot-title {
            text-align: center;
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # =========================
    # 🧠 INIT STEP STATE
    # =========================
    if "forgot_step" not in st.session_state:
        st.session_state["forgot_step"] = 1

    if "forgot_email" not in st.session_state:
        st.session_state["forgot_email"] = ""

    # =========================
    # 🧾 CARD
    # =======================

    # =========================
    # 🔹 STEP 1: ENTER EMAIL
    # =========================
    if st.session_state["forgot_step"] == 1:
        st.markdown('<div class="forgot-title">📩 Forgot Password</div>', unsafe_allow_html=True)

        email = st.text_input("Enter your email")

        if st.button("Send OTP"):
            if not email:
                st.error("Email is required")
            else:
                with st.spinner("Sending OTP..."):
                    response, status = forgot_password_api(email)

                if status == 200:
                    st.success("OTP sent to your email ✅")
                    st.session_state["forgot_email"] = email
                    st.session_state["forgot_step"] = 2
                    st.rerun()
                else:
                    st.error(response.get("detail") or response.get("message"))

    # =========================
    # 🔹 STEP 2: VERIFY OTP
    # =========================
    elif st.session_state["forgot_step"] == 2:
        st.markdown('<div class="forgot-title">🔢 Verify OTP</div>', unsafe_allow_html=True)

        otp = st.text_input("Enter OTP")

        if st.button("Verify OTP"):
            if not otp:
                st.error("OTP is required")
            else:
                with st.spinner("Verifying OTP..."):
                    response, status = verify_otp_api(
                        st.session_state["forgot_email"],
                        otp
                    )

                if status == 200:
                    st.success("OTP verified ✅")
                    st.session_state["forgot_step"] = 3
                    st.rerun()
                else:
                    st.error(response.get("detail") or response.get("message"))

    # =========================
    # 🔹 STEP 3: RESET PASSWORD
    # =========================
    elif st.session_state["forgot_step"] == 3:
        st.markdown('<div class="forgot-title">🔁 Reset Password</div>', unsafe_allow_html=True)

        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("Reset Password"):
            if not new_password or not confirm_password:
                st.error("All fields are required")

            elif new_password != confirm_password:
                st.error("Passwords do not match")

            else:
                with st.spinner("Resetting password..."):
                    response, status = reset_password_api(
                        st.session_state["forgot_email"],
                        new_password
                    )

                if status == 200:
                    st.success("Password reset successfully 🎉")

                    # Reset flow
                    st.session_state["forgot_step"] = 1
                    st.session_state["auth_page"] = "login"
                    st.rerun()
                else:
                    st.error(response.get("detail") or response.get("message"))

    # =========================
    # 🔙 BACK BUTTON
    # =========================
    if st.button("⬅ Back to Login"):
        st.session_state["forgot_step"] = 1
        st.session_state["auth_page"] = "login"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)