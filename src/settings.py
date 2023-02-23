from starlette.config import Config


config = Config(".env")

def get_db_url(user, passwd, host, db):
    return f"postgres://{user}:{passwd}@{host}:35432/{db}"


TG_BOT_TOKEN = config("TG_BOT_TOKEN", cast=str, default="")

ACCESS_TOKEN_EXPIRE_MINUTES = 60 
ALGORITHM = "HS256"

default_key = "8267343f61522a153a2e21b3c509f0ee81e6c2e7783465f245742fbfc38df342"
SECRET_KEY = config("TC_SECRET_KEY", cast=str, default=default_key)

POSTGRESQL_USERNAME = config("TC_POSTGRESQL_USERNAME", cast=str, default="")
POSTGRESQL_PASSWORD = config("TC_POSTGRESQL_PASSWORD", cast=str, default="")
POSTGRESQL_HOSTNAME = config("TC_POSTGRESQL_HOSTNAME", cast=str, default="")
POSTGRESQL_DATABASE = config("TC_POSTGRESQL_DATABASE", cast=str, default="")
POSTGRESQL_URL = get_db_url(POSTGRESQL_USERNAME, POSTGRESQL_PASSWORD, 
                            POSTGRESQL_HOSTNAME, POSTGRESQL_DATABASE)

WEBHOOK_HOST = "https://1def-37-252-80-171.eu.ngrok.io"
WEBHOOK_URL_PATH = "/messages/"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_URL_PATH}"

DATABASE_CONFIG = {
    "connections": {"default": POSTGRESQL_URL},
    "apps": {
        "models": {
            "models": ["src.users.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}