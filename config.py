from fastapi import HTTPException, status
import os
import sys
import base64
import json
from dotenv import load_dotenv

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


def decode(variable):
    """Decodes a Platform.sh environment variable.
    Args:
        variable (string):
            Base64-encoded JSON (the content of an environment variable).
    Returns:
        An dict (if representing a JSON object), or a scalar type.
    Raises:
        JSON decoding error.

    Taken from:
    https://github.com/platformsh-templates/django4/blob/master/myapp/settings.py
    """
    try:
        if sys.version_info[1] > 5:
            return json.loads(base64.b64decode(variable))
        else:
            return json.loads(base64.b64decode(variable).decode('utf-8'))
    except json.decoder.JSONDecodeError:
        print('Error decoding JSON, code %d', json.decoder.JSONDecodeError)





class Settings:
    PROJECT_NAME: str = "FastAPI Users Test"
    PROJECT_VERSION: str = "1.0.0"
    PLATFORMSH_DB_RELATIONSHIP = 'postgresqldatabase'

    # Import some Platform.sh settings from the environment.
    if (os.getenv('PLATFORM_APPLICATION_NAME') is not None):
        DEBUG = False
        if (os.getenv('PLATFORM_APP_DIR') is not None):
            STATIC_ROOT = os.path.join(os.getenv('PLATFORM_APP_DIR'), 'static')
            if (os.getenv('PLATFORM_PROJECT_ENTROPY') is not None):
                SECRET_KEY = os.getenv('PLATFORM_PROJECT_ENTROPY')
                # Database service configuration, post-build only.
                if (os.getenv('PLATFORM_ENVIRONMENT') is not None):
                # Using Platform.sh
                    platform_relationships = decode(os.environ.get("PLATFORM_RELATIONSHIPS", "{}"))
                    db_settings = platform_relationships[PLATFORMSH_DB_RELATIONSHIP][0]

                    POSTGRES_HOST = db_settings["host"]
                    POSTGRES_PORT = db_settings["port"]
                    POSTGRES_USER = db_settings["username"]
                    POSTGRES_PASSWORD = db_settings['password']
                    POSTGRES_DB = db_settings['path']
    else:
        POSTGRES_USER: str = os.getenv("POSTGRES_USER")
        POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
        POSTGRES_HOST: str = os.getenv("POSTGRES_SERVER", "localhost")
        POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
        POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tdd")
        SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

    ALGORITHM = "HS256"
    DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"



settings = Settings()
