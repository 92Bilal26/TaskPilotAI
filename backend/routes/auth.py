"""Authentication routes"""
from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from pydantic import BaseModel, EmailStr
from bcrypt import hashpw, gensalt, checkpw
from datetime import datetime, timedelta
from jose import jwt
from config import settings
from db import get_session
from models import User

router = APIRouter(prefix="/auth", tags=["authentication"])

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str

class SigninRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

def create_token(user_id: str, expires_in: int = settings.JWT_EXPIRY_SECONDS) -> str:
    expire = datetime.utcnow() + timedelta(seconds=expires_in)
    to_encode = {"user_id": user_id, "exp": expire}
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(request: SignupRequest, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == request.email)
    if session.exec(statement).first():
        raise HTTPException(status_code=409, detail="Email already registered")

    # Hash the password before storing
    hashed_password = hash_password(request.password)

    user = User(email=request.email, name=request.name, emailVerified=True)
    # Store hashed password in the database
    user.password_hash = hashed_password
    session.add(user)
    session.commit()
    session.refresh(user)
    return {
        "access_token": create_token(user.id),
        "refresh_token": create_token(user.id, settings.JWT_REFRESH_EXPIRY_SECONDS),
        "token_type": "bearer"
    }

@router.post("/signin", response_model=TokenResponse)
async def signin(request: SigninRequest, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == request.email)
    user = session.exec(statement).first()
    if not user or not hasattr(user, 'password_hash') or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {
        "access_token": create_token(user.id),
        "refresh_token": create_token(user.id, settings.JWT_REFRESH_EXPIRY_SECONDS),
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=TokenResponse)
async def refresh(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        return {
            "access_token": create_token(user_id),
            "refresh_token": create_token(user_id, settings.JWT_REFRESH_EXPIRY_SECONDS),
            "token_type": "bearer"
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
