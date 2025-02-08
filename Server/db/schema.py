from pydantic import BaseModel
from datetime import date


class UserModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    bdate: date
    user_id: str
    password: str


class LoginModel(BaseModel):
    user_id: str
    password: str


class BlogsModel(BaseModel):
    blogs_title: str
    blogs_description: str
    # created_by_user_id: int


class TokenModel(BaseModel):
    access_token: str
    token_type: str
