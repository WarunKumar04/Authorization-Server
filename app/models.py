from pydantic import BaseModel

class TokenResponse(BaseModel):
    otp_required: bool
    username: str

class LoginRequest(BaseModel):
    username: str
    password: str

class JWTTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

