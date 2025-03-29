import uuid
from datetime import datetime as dt
from typing import List

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Uuid, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)

    updated_at: Mapped[dt] = mapped_column(DateTime(), default=func.now(), onupdate=func.now())
    created_at: Mapped[dt] = mapped_column(DateTime(), default=func.now())


class User(Base):
    __tablename__ = 'user'

    is_superuser: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=False)
    email: Mapped[str] = mapped_column(String(length=100), unique=True, nullable=False)
    audio: Mapped[List['Audio']] = relationship(back_populates='user')


class Audio(Base):
    __tablename__ = 'audio'

    name: Mapped[str] = mapped_column(String(length=512), nullable=False)
    path: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user: Mapped['User'] = relationship(back_populates='audio')


