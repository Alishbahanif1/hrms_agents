import requests
from core.config import API_BASE_URL


# 🔹 Common request handler (reusable)
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

    elif response.status_code == 422:
        return {"success": False, "error": "Validation error", "details": data}

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
def create_employee(data, token):
    url = f"{API_BASE_URL}/api/v1/employees"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        return handle_response(response, url)

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


# =========================
# 🔥 GET ALL
# =========================
def get_employees(token):
    url = f"{API_BASE_URL}/api/v1/employees"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        return handle_response(response, url)

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


# =========================
# 🔥 GET BY ID
# =========================
def get_employee_by_id(employee_id, token):
    url = f"{API_BASE_URL}/api/v1/employees/{employee_id}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        return handle_response(response, url)

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


# =========================
# 🔥 UPDATE
# =========================
def update_employee(employee_id, data, token):
    url = f"{API_BASE_URL}/api/v1/employees/{employee_id}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print("\n====================")
    print("URL:", url)
    print("BODY:", data)

    response = requests.patch(url, json=data, headers=headers)

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)
    print("====================\n")

    return response.json()

# =========================
# 🔥 DELETE
# =========================
def delete_employee(employee_id, token):
    url = f"{API_BASE_URL}/api/v1/employees/{employee_id}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.delete(url, headers=headers, timeout=10)
        return handle_response(response, url)

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}