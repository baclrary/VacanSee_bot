import os

required_env_vars = ["DB_USER", "DB_PASS", "DB_NAME", "DB_HOST"]


def get_database_url():
    missing_env_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_env_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_env_vars)}")

    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")

    return f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
