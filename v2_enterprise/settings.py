from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os


class Settings(BaseSettings):

    class Config(SettingsConfigDict):
        env_file = '.env'
        env_file_encoding = "utf-8"

    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: str
    RABBITMQ_VHOST: str
    RABBITMQ_HEARTBEAT: str
    RABBITMQ_CONNECTION_ATTEMPT_DELAY: str
    RABBITMQ_QUEUE: str

    TC_BOT_USER: str
    TC_BOT_PASS: str
    TC_URL: str

    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_DRIVER_SYNC: str
    DB_DRIVER_ASYNC: str
    DB_USER: str
    DB_PASSWORD: str

    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    # old method: saving to cache
    CONTACTS: str = os.path.join(BASE_DIR, "contacts", "contacts_logins.json")
    CONTACTS_NAMES: str = os.path.join(BASE_DIR, "contacts", "contacts_names.json")
    DUTIES_FILE: str = r'\\example.corp.server.com\path\shedule.xlsx'

    @property
    def rabbit_mq_connection_string(self):
        return f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/"

    @property
    def db_connection_string(self):
        return f""


setting = Settings()
