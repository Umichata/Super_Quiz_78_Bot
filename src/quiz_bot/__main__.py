# Точка входа

import asyncio
import logging
from .bot import quiz_bot

async def main():
    """Основная функция запуска бота"""
    try:
        await quiz_bot.start()
    except KeyboardInterrupt:
        logging.info("Бот остановлен пользователем")
    except Exception as e:
        logging.error(f"Бот остановлен ошибкой: {e}")

if __name__ == "__main__":
    asyncio.run(main())