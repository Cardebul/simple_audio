from pydantic import UUID4, BaseModel, ConfigDict


class TokenUser(BaseModel):
    id: UUID4
    email: str
    is_superuser: bool

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel): email: str


class User(BaseModel): email: str

class Audio(BaseModel):
    id: UUID4
    name: str
    path: str

    model_config = ConfigDict(from_attributes=True)



