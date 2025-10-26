# Основной файл бота

import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from .config import config
from .database import create_tables
from .handlers.start import cmd_start, cmd_help
from .handlers.quiz import register_handlers

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class QuizBot:
    def __init__(self):
        self.bot = Bot(
            token=config.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        self.dp = Dispatcher()
    
    def register_handlers(self):
        """Регистрация всех обработчиков"""
        self.dp.message.register(cmd_start, Command("start"))
        self.dp.message.register(cmd_help, Command("help"))
        
        # Регистрация обработчиков квиза
        register_handlers(self.dp)
    
    async def start(self):
        """Запуск бота"""
        logger.info("Starting quiz bot...")
        
        # Создание таблиц БД
        await create_tables()
        
        # Регистрация обработчиков
        self.register_handlers()
        
        # Запуск поллинга
        await self.dp.start_polling(self.bot)

# Создание экземпляра бота для импорта
quiz_bot = QuizBot()