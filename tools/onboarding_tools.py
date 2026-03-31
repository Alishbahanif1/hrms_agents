# =========================
# 📦 IMPORTS
# =========================
import requests
from core.config import API_BASE_URL


# =========================
# 🔁 COMMON RESPONSE HANDLER
# =========================
def handle_response(response, url):
    """
    Common function to handle API responses
    Keeps logs + standardizes output
    """
    print("\n====================")
    print("URL:", url)
    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)
    print("====================\n")

    try:
        data = response.json()
    except:
        data = {"raw": response.text}

    # ✅ Success
    if response.status_code in [200, 201]:
        return {"success": True, "data": data}

    # ⚠️ Validation error
    elif response.status_code == 422:
        return {"success": False, "error": "Validation error", "details": data}

    # 🔐 Auth issues
    elif response.status_code in [401, 403]:
        return {"success": False, "error": "Unauthorized", "details": data}

    # ❌ Generic error
    return {
        "success": False,
        "error": "API error",
        "status_code": response.status_code,
        "details": data
    }


# =========================
# 🔥 CREATE ONBOARDING
# =========================
def create_onboarding(data, token):
    """
    Create onboarding record
    """
    url = f"{API_BASE_URL}/api/v1/onboarding"

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
# 🔥 GET ALL ONBOARDINGS
# =========================
def get_onboardings(token):
    """
    Fetch all onboarding records
    """
    url = f"{API_BASE_URL}/api/v1/onboarding"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        return handle_response(response, url)

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


# =========================
# 🔥 GET ONBOARDING BY ID
# =========================
def get_onboarding_by_id(onboarding_id, token):
    """
    Fetch single onboarding record
    """
    url = f"{API_BASE_URL}/api/v1/onboarding/{onboarding_id}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        return handle_response(response, url)

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


# =========================
# 🔥 UPDATE ONBOARDING
# =========================
def update_onboarding(onboarding_id, data, token):
    """
    Update onboarding record
    """
    url = f"{API_BASE_URL}/api/v1/onboarding/{onboarding_id}"

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
# 🔥 DELETE ONBOARDING
# =========================
def delete_onboarding(onboarding_id, token):
    """
    Delete onboarding record
    """
    url = f"{API_BASE_URL}/api/v1/onboarding/{onboarding_id}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.delete(url, headers=headers, timeout=10)
        return handle_response(response, url)

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}