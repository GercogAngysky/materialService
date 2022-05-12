from pydantic import BaseModel



class BaseUser(BaseModel):
    
    username: str = None
    email: str = None
    role: str = None


class UserCreate(BaseUser):

    password: str = None


class User(BaseUser):

    id: int = None

    class Config:
        orm_mode = True


class Token(BaseModel):

    access_token: str
    token_type: str = "bearer"
    