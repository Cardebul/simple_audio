
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User as mUser
from app.dependencies import get_current_user, get_session
from app.permissions import su_permission
from app.serializers.serializers import SUser, User

router = APIRouter(prefix='/users', tags=['users'])


@router.get("", response_model=list[SUser])
async def users(
    current_user: Annotated[mUser, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    await su_permission(current_user)
    q = await session.execute(select(mUser))
    users = q.scalars().all()
    return users


@router.get("/me", response_model=User)
async def read_users_me(
    current_user: Annotated[mUser, Depends(get_current_user)],
):
    return current_user
