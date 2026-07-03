from pydantic import BaseModel

class PasswordCreate(BaseModel):
    website: str
    username: str
    password: str
    notes: str | None = None


class PasswordUpdate(BaseModel):
    website: str | None = None
    username: str | None = None
    password: str | None = None
    notes: str | None = None

class PasswordResponse(BaseModel):
    user_id: int
    website: str
    username: str
    notes: str | None = None

    class Config:
        from_attributes = True