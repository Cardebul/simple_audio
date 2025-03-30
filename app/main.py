"""
Реализовать сервис по загрузке аудио-файлов от пользователей, используя FastAPI, SQLAlchemy и Docker. Пользователи могут давать файлам имя в самом API.
Авторизацию пользователей реализовать через Яндекс.
Файлы хранить локально, хранилище использовать не нужно.
Использовать асинхронный код.
БД - PostgreSQL 16.

Ожидаемый результат:

Готовое API с возможностью авторизации через Яндекс с последующей аутентификацией к запросам через внутренние токены API.
Доступные эндпоинты: авторизация через яндекс,
обновление внутреннего access_token; получение,
изменение данных пользователя, удаление пользователя от имени суперпользователя;
получение информации о аудио файлах пользователя: название файлов и путь в локальной хранилище.
Документация 

"""
import uuid
from typing import Annotated, Optional

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import select

from app.db.models import Audio as mAudio
from app.db.models import User as mUser
from app.db.session import async_session
from app.dependencies import get_current_user, is_refresh
from app.orm.orm import user_get_or_create
from app.serializers.serializers import Audio, Token, User
from app.utils.audio_utils import _upload_audio
from app.utils.token_utils import get_tokens
from app.utils.yandex_utils import yandex_get_access, yandex_get_info, yandex_get_url

app = FastAPI()


@app.get("/auth/yandex")
async def auth_yandex():
    return yandex_get_url() # or redirect

@app.get("/auth/yandex/callback")
async def auth_yandex_callback(code: str, cid: str) -> Token: # error error_description
    ya_access_token = await yandex_get_access(code)
    ya_email = await yandex_get_info(ya_access_token)
    user = await user_get_or_create(email=ya_email)
    return get_tokens(user)

@app.get("/auth/refresh")
async def auth_refresh(
    current_user: Annotated[mUser, Depends(get_current_user)],
    is_refresh: Annotated[bool, Depends(is_refresh)],
) -> Token:
    return get_tokens(current_user)

@app.get("/users/me", response_model=User)
async def read_users_me(
    current_user: Annotated[mUser, Depends(get_current_user)],
):
    return current_user

@app.post("/audio/upload", response_model=Audio)
async def upload_audio(
    current_user: Annotated[mUser, Depends(get_current_user)],
    file: Annotated[UploadFile, File(description='Audio only. Formats: MP3, WAV, OGG. Max size 1GB')],
    name: Annotated[str, Form()] = "",
):
    full_path, full_name, id = await _upload_audio(file, name)

    async with async_session() as session:
        audio = mAudio(id=id, name=full_name, path=full_path, user_id=current_user.id)
        session.add(audio)
        await session.commit()
    return audio

@app.post("/audio/download/{id}", response_class=FileResponse)
async def download_audio(
    current_user: Annotated[mUser, Depends(get_current_user)],
    id: uuid.UUID,
):
    async with async_session() as session:
        q = await session.execute(select(mAudio).where(mAudio.id == id, mAudio.user_id == current_user.id))
        file = q.scalar_one_or_none()

    if not file: raise HTTPException(
        status_code=404,
        detail='not found'
    )
    return FileResponse(
        path=file.path,
        filename=file.get_name
    )

@app.get("/audio/me", response_model=list[Audio])
async def read_users_me(
    current_user: Annotated[mUser, Depends(get_current_user)],
):
    async with async_session() as session:
        q = await session.execute(select(mAudio).where(mAudio.user_id == current_user.id))
        audio = q.scalars().all()
    return audio

