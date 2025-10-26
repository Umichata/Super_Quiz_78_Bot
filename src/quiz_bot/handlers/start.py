# Обработчики команд

from aiogram import types
from aiogram.filters import Command
from ..keyboards.builders import get_main_menu_keyboard

async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    await message.answer(
        "Добро пожаловать в квиз по Python!\n"
        "Проверьте свои знания языка программирования Python.",
        reply_markup=get_main_menu_keyboard()
    )

async def cmd_help(message: types.Message):
    """Обработчик команды /help"""
    help_text = """
Доступные команды:
/start - начать работу
/quiz - начать квиз
/stats - моя статистика
/leaderboard - таблица лидеров
/help - помощь

Или используйте кнопки меню
    """
    await message.answer(help_text.strip())