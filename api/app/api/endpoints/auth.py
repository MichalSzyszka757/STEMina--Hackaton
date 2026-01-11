from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any

from app.core import security
from app.core.database import SessionDep
from app.services import user_service
from app.schemas.token import Token

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_access_token(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = user_service.get_user_by_username(session, form_data.username)
    
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    access_token = security.create_access_token(subject=user.email_address)
    return {"access_token": access_token, "token_type": "bearer"}