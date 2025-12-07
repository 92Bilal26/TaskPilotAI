"""Authentication routes"""
from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from config import settings
from db import get_session
from models import User

router = APIRouter(prefix="/auth", tags=["authentication"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(request: SignupRequest, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == request.email)
    if session.exec(statement).first():
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(email=request.email, name=request.name, emailVerified=True)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"access_token": create_token(user.id), "refresh_token": create_token(user.id, settings.JWT_REFRESH_EXPIRY_SECONDS), "token_type": "bearer"}

@router.post("/signin", response_model=TokenResponse)
async def signin(request: SigninRequest, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == request.email)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": create_token(user.id), "refresh_token": create_token(user.id, settings.JWT_REFRESH_EXPIRY_SECONDS), "token_type": "bearer"}

@router.post("/refresh", response_model=TokenResponse)
async def refresh(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        return {"access_token": create_token(user_id), "refresh_token": create_token(user_id, settings.JWT_REFRESH_EXPIRY_SECONDS), "token_type": "bearer"}
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
