import requests
from core.config import API_BASE_URL


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
# 🔥 RESIGNATION
# =========================
def create_resignation(data, token):
    url = f"{API_BASE_URL}/api/v1/resignations/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    return handle_response(requests.post(url, json=data, headers=headers), url)


def get_resignations(token, params=None):
    url = f"{API_BASE_URL}/api/v1/resignations/"
    headers = {"Authorization": f"Bearer {token}"}
    return handle_response(requests.get(url, headers=headers, params=params), url)


def get_resignation_by_id(resignation_id, token):
    url = f"{API_BASE_URL}/api/v1/resignations/{resignation_id}"
    headers = {"Authorization": f"Bearer {token}"}
    return handle_response(requests.get(url, headers=headers), url)


def update_resignation(resignation_id, data, token):
    url = f"{API_BASE_URL}/api/v1/resignations/{resignation_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    return handle_response(requests.patch(url, json=data, headers=headers), url)


def delete_resignation(resignation_id, token):
    url = f"{API_BASE_URL}/api/v1/resignations/{resignation_id}"
    headers = {"Authorization": f"Bearer {token}"}
    return handle_response(requests.delete(url, headers=headers), url)


# =========================
# 🔥 CLEARANCE
# =========================
def get_clearance_list(token):
    url = f"{API_BASE_URL}/api/v1/resignations/clearance/"
    headers = {"Authorization": f"Bearer {token}"}
    return handle_response(requests.get(url, headers=headers), url)


def update_clearance(resignation_id, data, token):
    url = f"{API_BASE_URL}/api/v1/resignations/clearance/{resignation_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    return handle_response(requests.patch(url, json=data, headers=headers), url)