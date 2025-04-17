"""Application configuration settings."""

from utils import get_env_var

DB_HOST = get_env_var("DB_HOST", "localhost")
DB_USER = get_env_var("DB_USER", "root")
DB_PASSWORD = get_env_var("DB_PASSWORD")
DB_NAME = get_env_var("DB_NAME", "dekusms")
DB_DIALECT = get_env_var("DB_DIALECT", "sqlite")

if DB_DIALECT == "mysql":
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
elif DB_DIALECT == "sqlite":
    DATABASE_URL = f"sqlite:///./{DB_NAME}.db"
else:
    raise ValueError(f"Unsupported DB_DIALECT: {DB_DIALECT}")

DEFAULT_PASSWORD_POLICY = {
    "min_length": 8,
    "min_uppercase": 1,
    "min_numbers": 1,
    "min_special": 1,
    "allowed_specials": "!@#$%^*-_=+.,",
    "min_entropy": 0.5,
    "check_pwned": True,
}
