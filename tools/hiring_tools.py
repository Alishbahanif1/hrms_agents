import requests
from core.config import API_BASE_URL


# =========================
# 🔹 COMMON HANDLER
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


# =========================================================
# 🔥 HIRING REQUESTS
# =========================================================

# CREATE
def create_hiring_request(data, token):
    url = f"{API_BASE_URL}/api/v1/hiring/"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        return handle_response(response, url)

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


# GET ALL
def get_hiring_requests(token, params=None):
    url = f"{API_BASE_URL}/api/v1/hiring/"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        return handle_response(response, url)

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


# GET BY ID
def get_hiring_request_by_id(hiring_id, token):
    url = f"{API_BASE_URL}/api/v1/hiring/{hiring_id}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        return handle_response(response, url)

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


# UPDATE
def update_hiring_request(hiring_id, data, token):
    url = f"{API_BASE_URL}/api/v1/hiring/{hiring_id}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.patch(url, json=data, headers=headers, timeout=10)
        return handle_response(response, url)

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


# DELETE
def delete_hiring_request(hiring_id, token):
    url = f"{API_BASE_URL}/api/v1/hiring/{hiring_id}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.delete(url, headers=headers, timeout=10)
        return handle_response(response, url)

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


# =========================================================
# 🔥 JOB POSTINGS
# =========================================================

# CREATE
def create_job_posting(data, token):
    url = f"{API_BASE_URL}/api/v1/hiring/job-posting"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        return handle_response(response, url)

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


# GET ALL
def get_job_postings(token, params=None):
    url = f"{API_BASE_URL}/api/v1/hiring/job-posting"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        return handle_response(response, url)

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


# GET BY ID
def get_job_posting_by_id(posting_id, token):
    url = f"{API_BASE_URL}/api/v1/hiring/job-posting/{posting_id}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        return handle_response(response, url)

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


# UPDATE
def update_job_posting(posting_id, data, token):
    url = f"{API_BASE_URL}/api/v1/hiring/job-posting/{posting_id}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.patch(url, json=data, headers=headers, timeout=10)
        return handle_response(response, url)

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


# DELETE
def delete_job_posting(posting_id, token):
    url = f"{API_BASE_URL}/api/v1/hiring/job-posting/{posting_id}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.delete(url, headers=headers, timeout=10)
        return handle_response(response, url)

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}