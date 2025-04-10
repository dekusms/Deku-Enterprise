"""API Schemas"""

from typing import Optional
from pydantic import BaseModel


class UserCreateRequestV1(BaseModel):
    username: str
    password: str


class UserCreateResponseV1(BaseModel):
    username: str
    password: str


class ExchangeCreateRequestV1(BaseModel):
    name: str
    type: str
    vhost: str
    durable: bool = True


class ExchangeCreateResponseV1(BaseModel):
    name: str


class ErrorResponse(BaseModel):
    """Response model for errors."""

    error: str
