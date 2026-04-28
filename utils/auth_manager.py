import streamlit as st
import extra_streamlit_components as stx
from datetime import datetime, timedelta
from utils.auth_api import logout_api


# =========================
# 🍪 SINGLE COOKIE MANAGER INSTANCE
# =========================
def get_cookie_manager():
    if "cookie_manager" not in st.session_state:
        st.session_state["cookie_manager"] = stx.CookieManager()
    return st.session_state["cookie_manager"]


# =========================
# 🔐 SAVE TOKEN
# =========================
def save_token(token: str):
    # ✅ Save in session
    st.session_state["token"] = token
    st.session_state["logged_in"] = True

    # ✅ Save in URL
    st.query_params["auth_token"] = token

    # ✅ FORCE rerun so auth routing updates immediately
    st.rerun()


# =========================
# 🔄 LOAD TOKEN FROM COOKIE
# =========================
def load_token():
    # ✅ If already in session → use it
    if "token" in st.session_state:
        st.session_state["logged_in"] = True
        return

    # ✅ Try to load from URL params
    token = st.query_params.get("auth_token")

    if token:
        st.session_state["token"] = token
        st.session_state["logged_in"] = True
    else:
        st.session_state["logged_in"] = False

# =========================
# 🚪 LOGOUT
# =========================
def logout():
    token = st.session_state.get("token")

    if token:
        try:
            logout_api(token)
        except Exception:
            pass

    # ✅ Clear session
    st.session_state.pop("token", None)
    st.session_state["logged_in"] = False

    # ✅ Remove from URL
    if "auth_token" in st.query_params:
        del st.query_params["auth_token"]


# =========================
# ✅ CHECK LOGIN
# =========================
def is_logged_in():
    return st.session_state.get("logged_in", False)


# =========================
# 🔑 GET TOKEN
# =========================
def get_token():
    return st.session_state.get("token")