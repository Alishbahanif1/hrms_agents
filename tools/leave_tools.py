from utils.api_client import api_request

# =========================
# 🔥 LEAVE TYPES
# =========================

def create_leave_type(data, token):
    return api_request("POST", "/api/v1/leaves/types", token, data)

def get_leave_types(token, page=1):
    return api_request(
        "GET",
        "/api/v1/leaves/types",
        token,
        params={"page": page}
    )

def update_leave_type(leave_type_id, data, token):
    return api_request("PATCH", f"/api/v1/leaves/types/{leave_type_id}", token, data)

def delete_leave_type(leave_type_id, token):
    return api_request("DELETE", f"/api/v1/leaves/types/{leave_type_id}", token)


# =========================
# 🔥 LEAVE BALANCES
# =========================

def create_leave_balance(data, token):
    return api_request("POST", "/api/v1/leaves/balances", token, data)

def get_leave_balances(token, page=1):
    return api_request(
        "GET",
        "/api/v1/leaves/balances",
        token,
        params={"page": page}
    )

def get_employee_balances(employee_id, token):
    return api_request("GET", f"/api/v1/leaves/balances/{employee_id}", token)

def update_leave_balance(balance_id, data, token):
    return api_request("PATCH", f"/api/v1/leaves/balances/{balance_id}", token, data)


# =========================
# 🔥 LEAVE REQUESTS
# =========================

def create_leave_request(data, token):
    return api_request("POST", "/api/v1/leaves/requests", token, data)

def get_leave_requests(token, page=1):
    return api_request(
        "GET",
        "/api/v1/leaves/requests",
        token,
        params={"page": page}
    )

def get_leave_request_by_id(leave_id, token):
    return api_request("GET", f"/api/v1/leaves/requests/{leave_id}", token)

def update_leave_request(leave_id, data, token):
    return api_request("PATCH", f"/api/v1/leaves/requests/{leave_id}", token, data)

def delete_leave_request(leave_id, token):
    return api_request("DELETE", f"/api/v1/leaves/requests/{leave_id}", token)