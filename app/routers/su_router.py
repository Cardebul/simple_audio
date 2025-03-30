
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import exceptions as exc
from app.db.models import Audio as mAudio
from app.db.models import User as mUser
from app.dependencies import get_current_user, get_session
from app.permissions import su_permission
from app.serializers.serializers import Audio, SUser, SUserPatch

router = APIRouter(prefix='/user', tags=['su'])


@router.get("/{id}", response_model=SUser)
async def user_get(
    current_user: Annotated[mUser, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    id: uuid.UUID
):
    await su_permission(current_user)
    q = await session.execute(select(mUser).where(mUser.id == id))
    user = q.scalar_one_or_none()
    if user: return user
    raise exc.not_found


@router.delete("/{id}")
async def user_delete(
    current_user: Annotated[mUser, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    id: uuid.UUID
):
    await su_permission(current_user)
    q = await session.execute(select(mUser).where(mUser.id == id))
    user = q.scalar_one_or_none()
    if not user: raise exc.not_found
    if user.is_superuser: raise exc.su_not_allowed
    # before delete
    session.delete(user)
    await session.commit()
    return ''

@router.patch("/{id}", response_model=SUser)
async def user_patch(
    current_user: Annotated[mUser, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    id: uuid.UUID,
    user_data: SUserPatch,
):
    await su_permission(current_user)
    q = await session.execute(select(mUser).where(mUser.id == id))
    user = q.scalar_one_or_none()
    if not user: raise exc.not_found
    if user.is_superuser: raise exc.su_not_allowed
    user.is_active = user_data.is_active
    await session.commit()
    await session.refresh(user)
    return user

@router.get("/{id}/audio", response_model=list[Audio])
async def user_audio_get(
    current_user: Annotated[mUser, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    id: uuid.UUID
):
    await su_permission(current_user)
    q = await session.execute(select(mUser).where(mUser.id == id))
    if not q.scalar_one_or_none(): raise exc.not_found
    q = await session.execute(select(mAudio).where(mAudio.user_id == id))
    audio = q.scalars().all()
    return audio