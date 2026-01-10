from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.core import security
from app.schemas.token import TokenData
from app.schemas.user import User
from app.services import user_service # Zakładam, że tu przeniesiemy logikę DB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # lub "/api/auth/token" zależnie od routingu

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    
    # Tutaj odwołujemy się do serwisu, który pobiera usera z "bazy"
    user = user_service.get_user_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user