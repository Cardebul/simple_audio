import base64

import aiohttp
from fastapi import HTTPException, status

from app.config import AppConfig as ac


def _get_error(json):
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=json,
    )

def yandex_get_url():
    return (
        'https://oauth.yandex.ru/authorize?'
        f'response_type=code&client_id={ac.ya_id}&redirect_uri={ac.ya_red_uri}'
    )

async def yandex_get_access(code: str, url='https://oauth.yandex.ru/token'):
    auth = base64.b64encode(f'{ac.ya_id}:{ac.ya_secret}'.encode('utf-8')).decode('utf-8')
    data = {'grant_type': 'authorization_code', 'code': code}
    async with aiohttp.ClientSession(headers={'Authorization': f'Basic {auth}'}) as session:
        r = await session.post(url, data=data)
        json = await r.json()
        if r.status != 200: raise _get_error(json)
        return json['access_token']

async def yandex_get_info(access_token: str, url='https://login.yandex.ru/info'):
    async with aiohttp.ClientSession(headers={'Authorization': f'OAuth {access_token}'}) as session:
        r = await session.get(url, params={'format': 'json'})
        json = await r.json()
        if r.status != 200: raise _get_error(json)
        return json['default_email']
