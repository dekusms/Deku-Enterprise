"""Database Configuration Module."""

from sqlmodel import SQLModel, create_engine, Session
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as session:
        yield session
