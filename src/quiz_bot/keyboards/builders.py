# Клавиатуры

from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import types

def generate_options_keyboard(answer_options, question_index):
    """Генерация инлайн-клавиатуры с вариантами ответов"""
    builder = InlineKeyboardBuilder()
    
    for index, option in enumerate(answer_options):
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=f"answer_{question_index}_{index}")
        )
    
    builder.adjust(1)
    return builder.as_markup()

def get_main_menu_keyboard():
    """Главное меню бота"""
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать квиз"))
    builder.add(types.KeyboardButton(text="Моя статистика"))
    builder.add(types.KeyboardButton(text="Таблица лидеров"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)