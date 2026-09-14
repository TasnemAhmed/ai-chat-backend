from pydantic import BaseModel

# =========================
# Data received from client
# =========================


class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str