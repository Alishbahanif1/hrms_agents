import requests
import streamlit as st
from core.config import API_BASE_URL

BASE_URL = f"{API_BASE_URL}/api/v1/auth" # 🔴 replace this


# =========================
# 🔐 LOGIN (FORM-DATA)
# =========================
def login_api(email: str, password: str):
    url = f"{BASE_URL}/login"

    data = {
        "username": email,   # ⚠️ required by OAuth2PasswordRequestForm
        "password": password
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=data, headers=headers)

    return response.json(), response.status_code


# =========================
# 📝 REGISTER
# =========================
def register_api(token: str, password: str):
    url = f"{BASE_URL}/register"

    payload = {
        "token": token,
        "password": password
    }

    response = requests.post(url, json=payload)

    return response.json(), response.status_code


# =========================
# 📩 FORGOT PASSWORD (SEND OTP)
# =========================
def forgot_password_api(email: str):
    url = f"{BASE_URL}/forgot-password"

    payload = {"email": email}

    response = requests.post(url, json=payload)

    return response.json(), response.status_code


# =========================
# 🔢 VERIFY OTP
# =========================
def verify_otp_api(email: str, otp: str):
    url = f"{BASE_URL}/verify-otp"

    payload = {
        "email": email,
        "otp": otp
    }

    response = requests.post(url, json=payload)

    return response.json(), response.status_code


# =========================
# 🔁 RESET PASSWORD
# =========================
def reset_password_api(email: str, new_password: str):
    url = f"{BASE_URL}/reset-password"

    payload = {
        "email": email,
        "new_password": new_password
    }

    response = requests.post(url, json=payload)

    return response.json(), response.status_code


# =========================
# 🚪 LOGOUT
# =========================
def logout_api(token: str):
    url = f"{BASE_URL}/logout"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(url, headers=headers)

    return response.json(), response.status_code

# =========================
# 🔑 CHANGE PASSWORD
# =========================
def change_password_api(token: str, old_password: str, new_password: str):
    url = f"{BASE_URL}/change-password"

    payload = {
        "old_password": old_password,
        "new_password": new_password
    }

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json(), response.status_code