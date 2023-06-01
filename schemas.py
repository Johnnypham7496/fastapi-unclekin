from pydantic import BaseModel


class UserModel(BaseModel):
    id: int
    username: str
    email: str
    role: str


    class Config:
        orm_mode = True


class MessageModel(BaseModel):
    detail: str