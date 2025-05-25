from fastapi import FastAPI, HTTPException, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app import database, models
from app.models import JWTTokenResponse
import pyotp
import jwt
from datetime import datetime, timedelta
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

app = FastAPI()

# Secret and JWT config
SECRET_KEY = "your_secret_key"  # Replace with a secure one or load from .env
ALGORITHM = "HS256"

# OAuth2 token scheme for Swagger Auth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@app.post("/login", response_model=models.TokenResponse)
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = database.get_user(form_data.username)
    if not user or not database.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"otp_required": True, "username": form_data.username}


def create_tokens(username: str):
    now = datetime.utcnow()

    access_payload = {
        "sub": username,
        "type": "access",
        "exp": now + timedelta(minutes=10)
    }

    refresh_payload = {
        "sub": username,
        "type": "refresh",
        "exp": now + timedelta(days=1)
    }

    access_token = jwt.encode(access_payload, SECRET_KEY, algorithm=ALGORITHM)
    refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm=ALGORITHM)

    return access_token, refresh_token


@app.post("/verify-otp", response_model=JWTTokenResponse)
def verify_otp(username: str = Form(...), otp: str = Form(...)):
    user = database.get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ define TOTP properly
    totp = pyotp.TOTP(user.totp_secret)

    if not totp.verify(otp):
        raise HTTPException(status_code=401, detail="Invalid OTP")

    access_token, refresh_token = create_tokens(username)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


from fastapi import Query

@app.get("/protected")
def protected_route(
    scheme: str = Query(..., description="Auth scheme, e.g., Bearer"),
    token: str = Query(..., description="JWT token")
):
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid scheme")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"message": f"Welcome, {payload['sub']}! Token is valid."}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/otp", response_class=HTMLResponse)
async def otp_page(request: Request, username: str):
    return templates.TemplateResponse("otp.html", {"request": request, "username": username})

