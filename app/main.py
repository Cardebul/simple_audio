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
from typing import Annotated

from fastapi import Depends, FastAPI

from app.dependencies import get_current_user, is_refresh
from app.orm.orm import user_get_or_create
from app.serializers.serializers import Token, TokenUser, User
from app.utils import create_token, get_tokens
from app.yandex_utils import yandex_get_access, yandex_get_info, yandex_get_url

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
    current_user: Annotated[User, Depends(get_current_user)],
    is_refresh: Annotated[bool, Depends(is_refresh)],
) -> Token:
    return get_tokens(current_user)

@app.get("/users/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user

