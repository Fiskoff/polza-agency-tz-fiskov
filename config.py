from os import getenv
import logging

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings


load_dotenv()


class TelegramConfig(BaseModel):
    token: str = getenv("TG_TOKEN")


class FastAPIConfig(BaseModel):
    host: str = getenv("SERVER_HOST")
    port: int = int(getenv("SERVER_PORT"))

    prefix: str = "/api"


class LogerConfig:
    loger_level = logging.DEBUG
    log_handlers_console = logging.StreamHandler()

    def configure_logging(self):
        logging.basicConfig(
            level=self.loger_level,
            datefmt= "%Y-%m-%d %H:%M:%S",
            format="[%(asctime)s.%(msecs)03d] %(module)20s:%(lineno)-4d %(levelname)8s - %(message)s",
            handlers=[self.log_handlers_console]
        )


class Settings(BaseSettings):
    tg: TelegramConfig = TelegramConfig()
    api: FastAPIConfig = FastAPIConfig()
    log: LogerConfig = LogerConfig()


settings = Settings()