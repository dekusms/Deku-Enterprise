"""Database Models."""

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True, index=True)
    username: str = Field(max_length=50, unique=True, nullable=False)
    password: str = Field(max_length=255, nullable=False)
