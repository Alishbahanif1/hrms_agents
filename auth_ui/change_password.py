import streamlit as st
from utils.auth_api import change_password_api   # ✅ correct import
from utils.auth_manager import get_token


def show_change_password():
    st.markdown("## 🔑 Change Password")

    old_password = st.text_input("Old Password", type="password")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")

    if st.button("Update Password"):
        # =========================
        # 🧠 VALIDATION
        # =========================
        if not old_password or not new_password or not confirm_password:
            st.error("All fields are required")

        elif new_password != confirm_password:
            st.error("Passwords do not match")

        else:
            token = get_token()

            # =========================
            # 🔁 API CALL
            # =========================
            with st.spinner("Updating password..."):
                response = change_password_api(
                    token,
                    old_password,
                    new_password
                )

            # =========================
            # 📤 RESPONSE HANDLING
            # =========================
            if response["success"]:
                st.success("✅ Password updated successfully")

            else:
                error = response.get("error")

                # Clean error message
                if isinstance(error, dict):
                    error = error.get("detail") or str(error)

                st.error(error or "Failed to update password")