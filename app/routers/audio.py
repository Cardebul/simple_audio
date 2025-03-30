import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import exceptions as exc
from app.db.models import Audio as mAudio
from app.db.models import User as mUser
from app.dependencies import get_current_user, get_session
from app.serializers.serializers import Audio
from app.utils.audio_utils import _upload_audio

router = APIRouter(prefix='/audio', tags=['audio'])


@router.post("/upload", response_model=Audio)
async def upload_audio(
    current_user: Annotated[mUser, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    file: Annotated[UploadFile, File(description='Audio only. Formats: MP3, WAV, OGG. Max size 1GB')],
    name: Annotated[str, Form()] = "",
):
    full_path, full_name, id = await _upload_audio(file, name)
    audio = mAudio(id=id, name=full_name, path=full_path, user_id=current_user.id)
    session.add(audio)
    await session.commit()
    return audio

@router.post("/download/{id}", response_class=FileResponse)
async def download_audio(
    current_user: Annotated[mUser, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    id: uuid.UUID,
):
    q = await session.execute(select(mAudio).where(mAudio.id == id, mAudio.user_id == current_user.id))
    file = q.scalar_one_or_none()

    if not file: raise exc.not_found
    return FileResponse(
        path=file.path,
        filename=file.get_name
    )

@router.get("/me", response_model=list[Audio])
async def audio_me(
    current_user: Annotated[mUser, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    q = await session.execute(select(mAudio).where(mAudio.user_id == current_user.id))
    audio = q.scalars().all()
    return audio

