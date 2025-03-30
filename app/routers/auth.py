from typing import Annotated

from fastapi import APIRouter, Depends

from app.db.models import User as mUser
from app.dependencies import get_current_user, is_refresh
from app.orm.orm import user_get_or_create
from app.serializers.serializers import Token
from app.utils.token_utils import get_tokens
from app.utils.yandex_utils import (yandex_get_access, yandex_get_info,
                                    yandex_get_url)

router = APIRouter(prefix='/auth', tags=['auth'])


@router.get("/yandex")
async def auth_yandex():

    return yandex_get_url() # or redirect

@router.get("/yandex/callback")
async def auth_yandex_callback(code: str, cid: str) -> Token: # error error_description
    ya_access_token = await yandex_get_access(code)
    ya_email = await yandex_get_info(ya_access_token)
    user = await user_get_or_create(email=ya_email)
    return get_tokens(user)

@router.get("/refresh")
async def auth_refresh(
    current_user: Annotated[mUser, Depends(get_current_user)],
    is_refresh: Annotated[bool, Depends(is_refresh)],
) -> Token:
    return get_tokens(current_user)