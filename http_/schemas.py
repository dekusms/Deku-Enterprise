"""API Schemas."""

from typing import Optional
from sqlmodel import SQLModel


class v1:
    class UserCreateRequest(SQLModel):
        username: str
        password: str

    class UserResponse(SQLModel):
        id: int
        username: str
        created_at: Optional[str] = None  # Added for documentation/response

    class UserUpdateRequest(SQLModel):
        username: Optional[str] = None
        password: Optional[str] = None

    class ExchangeCreateRequest(SQLModel):
        name: str
        type: str
        vhost: str
        durable: bool = True

    class ExchangeCreateResponse(SQLModel):
        name: str
        type: str
        vhost: str
        durable: bool
        created_at: Optional[str] = None  # Added for documentation/response
