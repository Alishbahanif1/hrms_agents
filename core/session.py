SESSION = {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJlbXBsb3llZV9pZCI6MSwiZXhwIjoxNzc0MzY0NzkwfQ.IRdb5MPTbsrRPoCKAgLIDvk6hUj5q_JWnj-t3iswTX0"
}

def set_token(token: str):
    SESSION["token"] = token

def get_token():
    return SESSION.get("token")