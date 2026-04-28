from utils.api_client import api_request


# =========================
# 🧾 HIRING REQUESTS
# =========================

def create_hiring_request(data, token):
    return api_request("POST", "/api/v1/hiring/", token, data)


def get_hiring_requests(token, page=1):
    return api_request(
        "GET",
        "/api/v1/hiring/",
        token,
        params={"page": page}
    )


def get_hiring_request_by_id(hiring_id, token):
    return api_request("GET", f"/api/v1/hiring/{hiring_id}", token)


def update_hiring_request(hiring_id, data, token):
    return api_request("PATCH", f"/api/v1/hiring/{hiring_id}", token, data)


def delete_hiring_request(hiring_id, token):
    return api_request("DELETE", f"/api/v1/hiring/{hiring_id}", token)


# =========================
# 📢 JOB POSTINGS
# =========================

def create_job_posting(data, token):
    return api_request("POST", "/api/v1/hiring/job-posting", token, data)


def get_job_postings(token, page=1):
    return api_request(
        "GET",
        "/api/v1/hiring/job-posting",
        token,
        params={"page": page}
    )


def get_job_posting_by_id(posting_id, token):
    return api_request("GET", f"/api/v1/hiring/job-posting/{posting_id}", token)


def update_job_posting(posting_id, data, token):
    return api_request("PATCH", f"/api/v1/hiring/job-posting/{posting_id}", token, data)


def delete_job_posting(posting_id, token):
    return api_request("DELETE", f"/api/v1/hiring/job-posting/{posting_id}", token)