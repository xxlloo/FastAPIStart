from typing import Optional

from fastapi import Form
from pydantic import BaseModel


class User(BaseModel):
    username: Optional[str]
    password: Optional[str]
    phone: Optional[str]
    hashed_password: Optional[str]
    email: Optional[str]


class UserLoginByUserName(BaseModel):
    username: Optional[str] = Form(None, max_length=50)
    password: Optional[str] = Form(None, max_length=50)


class Register(UserLoginByUserName):
    email: Optional[str] = Form(None, max_length=50)


class UserLoginByEmail(BaseModel):
    email: Optional[str]
    password: Optional[str]


class UserLoginByPhone(BaseModel):
    phone: Optional[str]
    password: Optional[str]


class UserLoginByWechat(BaseModel):
    pass


class UserLoginResponse(BaseModel):
    access_token: Optional[str]
    refresh_token: Optional[str]
    token_type: Optional[str]
