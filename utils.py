"""Utility Functions."""

import os
from logutils import get_logger

logger = get_logger(__name__)


def get_env_var(env_var: str, default: str = None, strict: bool = False) -> str:
    """
    Get the environment variable or return the default value.

    Args:
        env_var (str): The name of the environment variable.
        default (str | None): The default value to return if the environment variable is not set.
        strict (bool | False): If True, raise an exception if the environment
            variable is not set or empty.
    """
    try:
        value = os.environ[env_var] if strict else os.environ.get(env_var) or default
        if strict and (value is None or value.strip() == ""):
            raise ValueError(f"Environment variable {env_var} is not set or empty.")
        return value
    except KeyError as e:
        logger.error("Environment variable %s not found: %s", env_var, e)
        raise
    except ValueError as e:
        logger.error("Error retrieving environment variable %s: %s", env_var, e)
        raise
