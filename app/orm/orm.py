import uuid
from typing import Union

from sqlalchemy import select

from app.db.models import User
from app.db.session import async_session


async def user_get_or_create(email: str):
    async with async_session() as session:
        stmt = select(User).filter(User.email == email)
        q = await session.execute(stmt)
        if user := q.scalar_one_or_none(): return user
        user = User(email=email, is_superuser=False)
        session.add(user)
        await session.commit()
        return user

async def user_get(email: str, id: Union[str, uuid.UUID]):
    id = uuid.UUID(id) if isinstance(id, str) else id
    async with async_session() as session:
        q = await session.execute(select(User).where(User.id == id, User.email == email))
        return q.scalar_one_or_none()
        