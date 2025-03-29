from datetime import datetime, timedelta, timezone

import jwt

from app.config import AppConfig as ac
from app.serializers.serializers import Token, TokenUser
from app.db.models import User

def get_tokens(user: User):
    token_user = TokenUser.model_validate(user)
    data = token_user.model_dump(mode='json')
    token = Token(
        access_token=create_token(data),
        refresh_token=create_token(data, refresh=True),
        token_type='bearer'
    )
    return token

def create_token(data: dict, refresh = False):
    to_encode = data.copy()
    delta = timedelta(days=ac.refresh_expire) if refresh else timedelta(minutes=ac.access_expire)
    expire = datetime.now(timezone.utc) + delta
    type = 'refresh' if refresh else 'access'
    to_encode.update({'exp': expire, 'type': type})
    encoded_jwt = jwt.encode(to_encode, ac.secret_key, algorithm=ac.algorithm)
    return encoded_jwt