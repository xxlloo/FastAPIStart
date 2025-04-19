from datetime import datetime

from sqlmodel import Field

from models.base import BaseModel


class Users(BaseModel, table=True):
    __tablename__ = "users"
    id: int = Field(
        default=None,
        primary_key=True,
        nullable=False,
        sa_column_kwargs={"comment": "用户ID"},
    )
    username: str = Field(..., index=True, sa_column_kwargs={"comment": "用户名"})
    email: str = Field(default=None, sa_column_kwargs={"comment": "邮箱"})
    phone: str = Field(default=None, sa_column_kwargs={"comment": "手机号"})
    password_hash: str = Field(..., sa_column_kwargs={"comment": "密码哈希值"})

    __table_args__ = {"comment": "用户信息表", "extend_existing": True}


class AuthProviders(BaseModel, table=True):
    __tablename__ = "auth_providers"
    id: int = Field(
        default=None,
        primary_key=True,
        nullable=False,
        sa_column_kwargs={"comment": "授权方式ID"},
    )
    provider_name: str = Field(
        ..., sa_column_kwargs={"comment": "授权方式名称，如'wechat', 'alipay', 'sso'"}
    )
    provider_display_name: str = Field(
        default=None,
        sa_column_kwargs={"comment": "授权方式展示名称，如'微信', '支付宝'"},
    )

    __table_args__ = {"comment": "授权平台表", "extend_existing": True}


class UserAuth(BaseModel, table=True):
    __tablename__ = "user_auth"
    id: int = Field(
        default=None,
        primary_key=True,
        nullable=False,
        sa_column_kwargs={"comment": "用户授权关系ID"},
    )
    user_id: int = Field(
        ...,
        foreign_key="users.id",
        sa_column_kwargs={"comment": "用户ID，外键关联`users`表"},
    )
    provider_id: int = Field(
        ...,
        foreign_key="auth_providers.id",
        sa_column_kwargs={"comment": "授权方式ID，外键关联`auth_providers`表"},
    )
    provider_user_id: str = Field(
        ..., sa_column_kwargs={"comment": "授权平台的用户ID，如微信、支付宝用户ID"}
    )
    access_token: str = Field(
        default=None, sa_column_kwargs={"comment": "授权平台的access_token"}
    )
    refresh_token: str = Field(
        default=None, sa_column_kwargs={"comment": "授权平台的refresh_token"}
    )
    expires_at: datetime = Field(
        default=None, sa_column_kwargs={"comment": "授权token的过期时间"}
    )

    __table_args__ = {
        "comment": "用户与授权平台之间的绑定关系",
        "extend_existing": True,
    }


class JwtToken(BaseModel, table=True):
    __tablename__ = "jwt_token"
    id: int = Field(
        default=None,
        primary_key=True,
        nullable=False,
        sa_column_kwargs={"comment": "JWT令牌ID"},
    )
    user_id: int = Field(
        ...,
        foreign_key="users.id",
        sa_column_kwargs={"comment": "用户ID，外键关联`users`表"},
    )
    token: str = Field(..., sa_column_kwargs={"comment": "JWT令牌"})
    expires_at: datetime = Field(
        default=None, sa_column_kwargs={"comment": "令牌过期时间"}
    )
    revoked: bool = Field(default=False, sa_column_kwargs={"comment": "令牌是否已撤销"})

    __table_args__ = {"comment": "JWT令牌管理表", "extend_existing": True}
