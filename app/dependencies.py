from typing import Annotated, AsyncGenerator

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from app import exceptions as exc
from app.config import AppConfig as ac
from app.db.session import async_session
from app.orm.orm import user_get
from app.serializers.serializers import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='')


async def _get_current_user(token, refresh = False):
    try:
        payload = jwt.decode(token, ac.secret_key, algorithms=[ac.algorithm])
        is_active, email, id = payload.get('is_active'), payload.get('email'), payload.get('id')
        if None in [email, id, is_active]: raise exc.credentials_exception
        _assert = 'refresh' if refresh else 'access'
        assert payload.get('type') == _assert
        token_data = TokenData(email=email)
    except AssertionError: raise exc.invalid_token_type
    except InvalidTokenError: raise exc.credentials_exception
    user = await user_get(email=token_data.email, id=id, is_active=is_active)
    if user is None: raise exc.credentials_exception
    return user

async def get_current_user_refresh(token: Annotated[str, Depends(oauth2_scheme)]):
    return await _get_current_user(token, refresh=True)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    return await _get_current_user(token)

async def get_session() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session