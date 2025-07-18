import logging
import pdb
from typing import Optional
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .models import AuthUser
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login",auto_error=False)

def get_current_user(token:Optional[str]=Depends(oauth2_scheme),db: Session = Depends(get_db)):
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Authorization token is missing. Please log in and provide a valid token.",
        )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        logging.basicConfig(level=logging.DEBUG)
        logging.debug(type(payload['user_id']))
        userId:int = payload.get('user_id')
        if userId is None:
            raise HTTPException(detail="Invalid credentials",status_code=401)
    except JWTError:
        raise JWTError()
    user = db.query(AuthUser).filter(AuthUser.id==userId).first()
    if user is None :
        raise HTTPException(detail="User not found",status_code=401)
    return user