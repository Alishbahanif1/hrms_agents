import streamlit as st
from utils.api_client import change_password_api
from utils.auth_manager import get_token


def show_change_password():
    st.markdown("## 🔑 Change Password")

    old_password = st.text_input("Old Password", type="password")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")

    if st.button("Update Password"):
        if not old_password or not new_password or not confirm_password:
            st.error("All fields are required")

        elif new_password != confirm_password:
            st.error("Passwords do not match")

        else:
            token = get_token()

            with st.spinner("Updating password..."):
                response, status = change_password_api(
                    token,
                    old_password,
                    new_password
                )

            if status == 200:
                st.success("✅ Password updated successfully")

            else:
                error_msg = (
                    response.get("detail")
                    or response.get("message")
                    or str(response)
                )
                st.error(error_msg)