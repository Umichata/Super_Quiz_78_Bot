# Файл конфигурации
from dotenv import load_dotenv
import os
from dataclasses import dataclass

load_dotenv()

@dataclass
class Config:
    BOT_TOKEN: str = os.getenv('TOKEN')
    DB_NAME: str = "quiz_bot.db"

config = Config()