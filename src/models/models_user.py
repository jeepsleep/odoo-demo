from pydantic import BaseModel, field_validator


class UserBaseModel(BaseModel):
    id: int
    name: str
    login: str
    email: str
    active: bool = True

    @field_validator('name', 'login', 'email')
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()

class UserOutModel(UserBaseModel):
    pass

class UserListOutModel(BaseModel):
    users: list[UserOutModel] 