from datetime import datetime as dt

from pydantic import UUID4, BaseModel, ConfigDict


class TokenUser(BaseModel):
    id: UUID4
    email: str
    is_superuser: bool
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel): email: str


class User(BaseModel): email: str


class Audio(BaseModel):
    id: UUID4
    get_name: str
    path: str

    model_config = ConfigDict(from_attributes=True)


class SUser(BaseModel):
    id: UUID4
    created_at: dt
    updated_at: dt

    email: str
    is_superuser: bool
    is_active: bool


class SUserPatch(BaseModel):
    is_active: bool



