"""Users Service Module."""

from sqlmodel import Session, select
from models import User
from security.password import hash_password, verify_password
from typing import Optional


class UserService:
    def __init__(self, db: Session):
        """Initialize UserService with a database session."""
        self.db = db

    def create_user(self, username: str, password: str) -> User:
        """Create a new user."""
        hashed_password = hash_password(password)
        user = User(username=username, password=hashed_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user(self, user_id: int) -> Optional[User]:
        """Retrieve a user by ID."""
        return self.db.get(User, user_id)

    def update_user(
        self, user_id: int, username: Optional[str], password: Optional[str]
    ) -> Optional[User]:
        """Update a user's information."""
        user = self.db.get(User, user_id)
        if not user:
            return None
        if username:
            user.username = username
        if password:
            user.password = hash_password(password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        """Delete a user by ID."""
        user = self.db.get(User, user_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True
