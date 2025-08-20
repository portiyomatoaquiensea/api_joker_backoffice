import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DTAPL = {
        "host": os.getenv("DB_HOST_DTAPL"),
        "port": os.getenv("DB_PORT_DTAPL"),
        "user": os.getenv("DB_USERNAME_DTAPL"),
        "password": os.getenv("DB_PASSWORD_DTAPL"),
        "database": os.getenv("DB_NAME_DTAPL"),
        "ssl": os.getenv("DB_SSL_DTAPL") == "true",
    }

    REALTIME = {
        "host": os.getenv("DB_HOST_REALTIME"),
        "port": os.getenv("DB_PORT_REALTIME"),
        "user": os.getenv("DB_USERNAME_REALTIME"),
        "password": os.getenv("DB_PASSWORD_REALTIME"),
        "database": os.getenv("DB_NAME_REALTIME"),
        "ssl": os.getenv("DB_SSL_REALTIME") == "true",
    }

settings = Settings()
