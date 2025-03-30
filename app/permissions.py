from fastapi import HTTPException

from app.config import AppConfig as ac
from app.db.models import User as mUser


async def su_permission(user: mUser):
    if (user.email in ac.su_default_emails): return
    raise HTTPException(
        status_code=403,
        detail='have not permission for this operation'
    )