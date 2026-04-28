from utils.api_client import api_request


# =========================
# 👤 EMPLOYEES
# =========================

def create_employee(data, token):
    return api_request("POST", "/api/v1/employees/", token, data)


def get_employees(token, page=1):
    return api_request(
        "GET",
        "/api/v1/employees/",
        token,
        params={"page": page}
    )


def get_employee_by_id(employee_id, token):
    return api_request("GET", f"/api/v1/employees/{employee_id}", token)


def update_employee(employee_id, data, token):
    return api_request("PATCH", f"/api/v1/employees/{employee_id}", token, data)


def delete_employee(employee_id, token):
    return api_request("DELETE", f"/api/v1/employees/{employee_id}", token)


# =========================
# 🏢 DEPARTMENTS
# =========================

def create_department(data, token):
    return api_request("POST", "/api/v1/departments/", token, data)


def get_departments(token, page=1):
    return api_request(
        "GET",
        "/api/v1/departments/",
        token,
        params={"page": page}
    )


def get_department_by_id(department_id, token):
    return api_request("GET", f"/api/v1/departments/{department_id}", token)


def update_department(department_id, data, token):
    return api_request("PATCH", f"/api/v1/departments/{department_id}", token, data)


def delete_department(department_id, token):
    return api_request("DELETE", f"/api/v1/departments/{department_id}", token)


# =========================
# 🧩 ROLES
# =========================

def create_role(data, token):
    return api_request("POST", "/api/v1/roles/", token, data)


def get_roles(token, page=1):
    return api_request(
        "GET",
        "/api/v1/roles/",
        token,
        params={"page": page}
    )


def get_role_by_id(role_id, token):
    return api_request("GET", f"/api/v1/roles/{role_id}", token)


def update_role(role_id, data, token):
    return api_request("PATCH", f"/api/v1/roles/{role_id}", token, data)


def delete_role(role_id, token):
    return api_request("DELETE", f"/api/v1/roles/{role_id}", token)