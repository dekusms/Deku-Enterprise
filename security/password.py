"""Password Security Module."""

from passlib.hash import argon2
from config import DEFAULT_PASSWORD_POLICY
from logutils import get_logger
from security.password_validation_tests import run_password_validation_tests

logger = get_logger(__name__)


def hash_password(password: str) -> str:
    """Hash a password using Argon2."""
    return argon2.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its Argon2 hash."""
    return argon2.verify(plain_password, hashed_password)


def validate_password(password: str, policy: dict = None) -> tuple[bool, str]:
    """
    Validate a password against a password policy and check if it's pwned.

    Args:
        password (str): The password to validate.
        policy (dict): The password policy to enforce.

    Returns:
        tuple: A tuple (err, message). If err is False, validation passed.
    """
    if not policy:
        policy = DEFAULT_PASSWORD_POLICY

    tests = run_password_validation_tests(password, policy)

    for test in tests:
        err, message = test()
        if err:
            return err, message

    return False, "Password is valid."
