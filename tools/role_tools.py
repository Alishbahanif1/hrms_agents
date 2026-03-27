import requests
from core.config import API_BASE_URL


# =========================
# 🔹 Common handler
# =========================
def handle_response(response, url):
    print("\n====================")
    print("URL:", url)
    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)
    print("====================\n")

    try:
        data = response.json()
    except:
        data = {"raw": response.text}

    if response.status_code in [200, 201]:
        return {"success": True, "data": data}

    elif response.status_code in [401, 403]:
        return {"success": False, "error": "Unauthorized", "details": data}

    return {
        "success": False,
        "error": "API error",
        "status_code": response.status_code,
        "details": data
    }


# =========================
# 🔥 CREATE
# =========================
def create_role(data, token):
    url = f"{API_BASE_URL}/api/v1/roles/"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=data, headers=headers)
    return handle_response(response, url)


# =========================
# 🔥 GET ALL
# =========================
def get_roles(token, params=None):
    url = f"{API_BASE_URL}/api/v1/roles/"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers, params=params)
    return handle_response(response, url)


# =========================
# 🔥 GET BY ID
# =========================
def get_role_by_id(role_id, token):
    url = f"{API_BASE_URL}/api/v1/roles/{role_id}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    return handle_response(response, url)


# =========================
# 🔥 UPDATE
# =========================
def update_role(role_id, data, token):
    url = f"{API_BASE_URL}/api/v1/roles/{role_id}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.patch(url, json=data, headers=headers)
    return handle_response(response, url)


# =========================
# 🔥 DELETE
# =========================
def delete_role(role_id, token):
    url = f"{API_BASE_URL}/api/v1/roles/{role_id}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.delete(url, headers=headers)
    return handle_response(response, url)