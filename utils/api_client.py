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

    return {
        "success": response.status_code in [200, 201],
        "status_code": response.status_code,
        "data": data if response.status_code in [200, 201] else None,
        "error": None if response.status_code in [200, 201] else data
    }


def api_request(method, path, token=None, data=None, form_data=None,params=None):
    url = f"{API_BASE_URL}{path}"

    headers = {}

    if token:
        headers["Authorization"] = f"Bearer {token}"
    if data:
        headers["Content-Type"] = "application/json"
    if form_data:
        response = requests.request(
            method,
            url,
            data=form_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30
        )
    else:
        if data:
            headers["Content-Type"] = "application/json"

        response = requests.request(
            method,
            url,
            json=data,
            params=params,
            headers=headers,
            timeout=30
        )

    return handle_response(response, url)