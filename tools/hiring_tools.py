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
# 🔥 HIRING REQUEST
# =========================
def create_hiring_request(data, token):
    url = f"{API_BASE_URL}/api/v1/hiring/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    return handle_response(requests.post(url, json=data, headers=headers), url)


def get_hiring_requests(token, params=None):
    url = f"{API_BASE_URL}/api/v1/hiring/"
    headers = {"Authorization": f"Bearer {token}"}
    return handle_response(requests.get(url, headers=headers, params=params), url)


def get_hiring_request_by_id(hiring_id, token):
    url = f"{API_BASE_URL}/api/v1/hiring/{hiring_id}"
    headers = {"Authorization": f"Bearer {token}"}
    return handle_response(requests.get(url, headers=headers), url)


def update_hiring_request(hiring_id, data, token):
    url = f"{API_BASE_URL}/api/v1/hiring/{hiring_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    return handle_response(requests.patch(url, json=data, headers=headers), url)


def delete_hiring_request(hiring_id, token):
    url = f"{API_BASE_URL}/api/v1/hiring/{hiring_id}"
    headers = {"Authorization": f"Bearer {token}"}
    return handle_response(requests.delete(url, headers=headers), url)


# =========================
# 🔥 JOB POSTING
# =========================
def create_job_posting(data, token):
    url = f"{API_BASE_URL}/api/v1/hiring/job-posting"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    return handle_response(requests.post(url, json=data, headers=headers), url)


def get_job_postings(token, params=None):
    url = f"{API_BASE_URL}/api/v1/hiring/job-posting"
    headers = {"Authorization": f"Bearer {token}"}
    return handle_response(requests.get(url, headers=headers, params=params), url)


def get_job_posting_by_id(posting_id, token):
    url = f"{API_BASE_URL}/api/v1/hiring/job-posting/{posting_id}"
    headers = {"Authorization": f"Bearer {token}"}
    return handle_response(requests.get(url, headers=headers), url)


def update_job_posting(posting_id, data, token):
    url = f"{API_BASE_URL}/api/v1/hiring/job-posting/{posting_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    return handle_response(requests.patch(url, json=data, headers=headers), url)


def delete_job_posting(posting_id, token):
    url = f"{API_BASE_URL}/api/v1/hiring/job-posting/{posting_id}"
    headers = {"Authorization": f"Bearer {token}"}
    return handle_response(requests.delete(url, headers=headers), url)