from utils.api_client import api_request


def login_api(email: str, password: str):
    return api_request(
        "POST",
        "/api/v1/auth/login",
        form_data={
            "username": email,
            "password": password
        }
    )


def register_api(token: str, password: str):
    return api_request(
        "POST",
        "/api/v1/auth/register",
        data={"token": token, "password": password}
    )


def forgot_password_api(email: str):
    return api_request(
        "POST",
        "/api/v1/auth/forgot-password",
        data={"email": email}
    )


def verify_otp_api(email: str, otp: str):
    return api_request(
        "POST",
        "/api/v1/auth/verify-otp",
        data={"email": email, "otp": otp}
    )


def reset_password_api(email: str, new_password: str):
    return api_request(
        "POST",
        "/api/v1/auth/reset-password",
        data={"email": email, "new_password": new_password}
    )


def logout_api(token: str):
    return api_request("POST", "/api/v1/auth/logout", token=token)


def change_password_api(token: str, old_password: str, new_password: str):
    return api_request(
        "POST",
        "/api/v1/auth/change-password",
        token=token,
        data={
            "old_password": old_password,
            "new_password": new_password
        }
    )