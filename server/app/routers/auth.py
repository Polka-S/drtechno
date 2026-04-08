from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.db import get_db
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.security import create_access_token
from app.services.auth import authenticate_user, register_user
from app.schemas import UserCreate, UserBase
from app.dependencies import get_current_user
from app.models import User


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.get("/me", response_model=UserBase)
def get_current_user(current_user: User = Depends(get_current_user)) -> UserBase:
    return current_user

@router.post("/register", response_model=UserBase)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = register_user(db, user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    response = JSONResponse(content={
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "isSuperuser": user.is_superuser,
    })
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=False,   # True в production с HTTPS
    )
    return response

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=False,   # True в production с HTTPS
    )
    return response

@router.post("/logout")
def logout():
    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie("access_token")
    return response