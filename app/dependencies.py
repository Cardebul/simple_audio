from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from app.config import AppConfig as ac
from app.orm.orm import user_get
from app.serializers.serializers import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='')

async def is_refresh(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, ac.secret_key, algorithms=[ac.algorithm])
        assert payload.get('type') == 'refresh'
        return True
    except InvalidTokenError: raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Could not validate credentials"
    )
    except AssertionError: raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid token type"
    )

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, ac.secret_key, algorithms=[ac.algorithm])
        print(payload)
        email, id = payload.get('email'), payload.get('id')
        if None in [email, id]:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = await user_get(email=token_data.email, id=id)
    if user is None:
        raise credentials_exception
    return user
