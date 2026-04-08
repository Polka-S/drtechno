from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.services.auth import get_user_by_email
from app.core.security import decode_access_token
from app.core.db import get_db
from app.models import User


async def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="No subject")
    
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user