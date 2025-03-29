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


import base64
from typing import Union

import aiohttp
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.config import AppConfig as ac

app = FastAPI()


async def yandex_get_access(code: str, url='https://oauth.yandex.ru/token'):
    auth = base64.b64encode(f'{ac.ya_id}:{ac.ya_secret}'.encode('utf-8')).decode('utf-8')
    data = {'grant_type': 'authorization_code', 'code': code}
    async with aiohttp.ClientSession(headers={'Authorization': f'Basic {auth}'}) as session:
        r = await session.post(url, data=data)
        if r.status != 200:
            print(r.content)
            ...
            return
        json = await r.json()
        return json['access_token']

async def yandex_get_info(access_token: str, url='https://login.yandex.ru/info'):
    async with aiohttp.ClientSession(headers={'Authorization': f'OAuth {access_token}'}) as session:
        r = await session.get(url, params={'format': 'json'})
        if r.status != 200:
            print(r.content)
            ...
            return
        json = await r.json()
        return json['default_email']


def get_yandex_url():
    return f'https://oauth.yandex.ru/authorize?response_type=code&client_id={ac.ya_id}&redirect_uri={ac.ya_red_uri}'

@app.get("/auth/yandex")
async def auth_yandex():
    # return RedirectResponse(get_yandex_url())
    return get_yandex_url()

@app.get("/auth/yandex/callback")
async def auth_yandex_callback(code: str, cid: str): # error error_description
    access_token = await yandex_get_access(code)
    default_email = await yandex_get_info(access_token)
    return f'{default_email}'

