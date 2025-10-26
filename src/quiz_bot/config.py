# Файл конфигурации

import os
from dataclasses import dataclass

@dataclass
class Config:
    BOT_TOKEN: str = "8039540070:AAHG1N8mHrMVbiV3-SjLKw3o4SD1Qvmc77M"
    DB_NAME: str = "quiz_bot.db"

config = Config()