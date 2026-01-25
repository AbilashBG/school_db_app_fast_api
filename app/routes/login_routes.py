from fastapi import APIRouter, HTTPException
from jose import jwt, JWTError # type: ignore
from datetime import datetime, timedelta

router = APIRouter(prefix="/login", tags=["Login"])

# configurations for JWT
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = "secret_key_test"

# Utility functions for token creation
def create_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"username":username, "expire": int(expire.timestamp())}
    # header.payload.signature
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Utility function to verify token
def verify_token(token: str):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["username"]
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid or expired token")


# login route ******************************************************
@router.post("/login")
def login(username: str, password: str):
    # Placeholder logic for user authentication
    if username == "admin" and password == "password":
        token = create_token(username)
        return {"token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@router.get("/secure-data")
def get_secure_data(token: str):
    username = verify_token(token)
    return {"message": f"Hello, {username}. This is secure data."}  