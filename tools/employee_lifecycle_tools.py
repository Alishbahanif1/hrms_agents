from utils.api_client import api_request

# =========================
# Onboarding
# =========================

def list_onboarding(token, page=1):
    return api_request(
        "GET",
        "/api/v1/onboarding/",
        token,
        params={"page": page}
    )

def get_onboarding(onboarding_id, token):
    return api_request("GET", f"/api/v1/onboarding/{onboarding_id}", token)

def update_onboarding(onboarding_id, data, token):
    return api_request("PATCH", f"/api/v1/onboarding/{onboarding_id}", token, data)

def delete_onboarding(onboarding_id, token):
    return api_request("DELETE", f"/api/v1/onboarding/{onboarding_id}", token)


# =========================
# Trainings
# =========================

def list_trainings(token, page=1):
    return api_request(
        "GET",
        "/api/v1/trainings/",
        token,
        params={"page": page}
    )

def get_training(training_id, token):
    return api_request("GET", f"/api/v1/trainings/{training_id}", token)

def create_training(data, token):
    return api_request("POST", "/api/v1/trainings/", token, data)

def update_training(training_id, data, token):
    return api_request("PATCH", f"/api/v1/trainings/{training_id}", token, data)

def delete_training(training_id, token):
    return api_request("DELETE", f"/api/v1/trainings/{training_id}", token)

def get_training_assignments(training_id, token):
    return api_request(
        "GET",
        f"/api/v1/trainings/{training_id}/assignments",
        token
    )


# =========================
# Resignations
# =========================

def list_resignations(token, page=1):
    return api_request(
        "GET",
        "/api/v1/resignations/",
        token,
        params={"page": page}
    )

def get_resignation(resignation_id, token):
    return api_request("GET", f"/api/v1/resignations/{resignation_id}", token)

def create_resignation(data, token):
    return api_request("POST", "/api/v1/resignations/", token, data)

def update_resignation(resignation_id, data, token):
    return api_request("PATCH", f"/api/v1/resignations/{resignation_id}", token, data)

def delete_resignation(resignation_id, token):
    return api_request("DELETE", f"/api/v1/resignations/{resignation_id}", token)


# =========================
# Clearance
# =========================

def list_clearance(token, page=1):
    return api_request(
        "GET",
        "/api/v1/resignations/clearance/",
        token,
        params={"page": page}
    )

def get_clearance(resignation_id, token):
    return api_request("GET", f"/api/v1/resignations/clearance/{resignation_id}", token)

def update_clearance(resignation_id, data, token):
    return api_request("PATCH", f"/api/v1/resignations/clearance/{resignation_id}", token, data)

def delete_clearance(resignation_id, token):
    return api_request("DELETE", f"/api/v1/resignations/clearance/{resignation_id}", token)