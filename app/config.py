import os

from dotenv import load_dotenv

load_dotenv()

class AppConfig:
    pg_user = os.getenv('POSTGRES_USER')
    pg_pass = os.getenv('POSTGRES_PASSWORD')
    pg_host = os.getenv('DB_HOST')
    pg_port = os.getenv('DB_PORT')
    pg_db = os.getenv('POSTGRES_DB')

    secret_key = os.getenv('SECRET_KEY')
    algorithm = os.getenv('ALGORITHM')
    access_expire = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
    refresh_expire = int(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS'))

    ya_id = os.getenv('YANDEX_CLIENT_ID')
    ya_secret = os.getenv('YANDEX_CLIENT_SECRET')
    ya_red_uri = os.getenv('REDIRECT_URI')

    debug = False if os.getenv('DEBUG') != 'True' else True