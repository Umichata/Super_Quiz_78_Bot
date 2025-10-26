# Обработчики квиза

import logging
from aiogram import types, F
from aiogram.filters import Command
from ..data.quiz_data import quiz_data
from ..keyboards.builders import generate_options_keyboard, get_main_menu_keyboard
from ..database import update_quiz_state, get_quiz_state, save_quiz_result, get_user_stats, get_leaderboard

logger = logging.getLogger(__name__)

async def cmd_quiz(message: types.Message):
    """Начало нового квиза"""
    user_id = message.from_user.id
    await update_quiz_state(user_id, 0, 0)
    await get_question(message, user_id)

async def get_question(message: types.Message, user_id: int):
    """Отправка вопроса пользователю"""
    question_index, score = await get_quiz_state(user_id)
    
    if question_index >= len(quiz_data):
        await finish_quiz(message, user_id, score)
        return
    
    question_data = quiz_data[question_index]
    keyboard = generate_options_keyboard(question_data['options'], question_index)
    
    await message.answer(
        f"Вопрос {question_index + 1}/{len(quiz_data)}:\n"
        f"{question_data['question']}",
        reply_markup=keyboard
    )

async def handle_answer(callback: types.CallbackQuery):
    """Обработка ответа пользователя"""
    user_id = callback.from_user.id
    
    # Получаем данные пользователя ИЗ CALLBACK
    username = callback.from_user.username
    first_name = callback.from_user.first_name or ""
    last_name = callback.from_user.last_name or ""
    full_name = f"{first_name} {last_name}".strip()
    if not full_name and not username:
        full_name = f"User_{user_id}"
    
    question_index, score = await get_quiz_state(user_id)
    
    # Парсим данные из callback
    _, q_index, selected_option = callback.data.split('_')
    q_index = int(q_index)
    selected_option = int(selected_option)
    
    # Удаляем кнопки после ответа
    await callback.bot.edit_message_reply_markup(
        chat_id=user_id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    
    question_data = quiz_data[q_index]
    is_correct = selected_option == question_data['correct_option']
    
    if is_correct:
        score += 1
        await callback.message.answer("Верно!")
    else:
        correct_answer = question_data['options'][question_data['correct_option']]
        await callback.message.answer(
            f"Неправильно.\n"
            f"Правильный ответ: {correct_answer}\n"
            f"{question_data['explanation']}"
        )
    
    # Обновляем состояние
    question_index += 1
    await update_quiz_state(user_id, question_index, score)
    
    # Отправляем следующий вопрос или завершаем квиз
    if question_index < len(quiz_data):
        await get_question(callback.message, user_id)
    else:
        # Передаем данные пользователя в finish_quiz
        await finish_quiz(callback.message, user_id, score, username, full_name)
    
    await callback.answer()

async def finish_quiz(message: types.Message, user_id: int, score: int, username: str, full_name: str):
    """Завершение квиза и сохранение результата"""
    # Теперь получаем данные пользователя из аргументов
    await save_quiz_result(
        user_id=user_id,
        username=username,
        full_name=full_name,
        score=score
    )
    
    await message.answer(
        f"Квиз завершен!\n"
        f"Ваш результат: {score}/{len(quiz_data)}\n"
        f"Процент правильных ответов: {score/len(quiz_data)*100:.1f}%",
        reply_markup=get_main_menu_keyboard()
    )

async def cmd_stats(message: types.Message):
    """Показать статистику пользователя"""
    user_id = message.from_user.id
    stats = await get_user_stats(user_id)
    
    if stats:
        last_score, completed_at = stats
        await message.answer(
            f"Ваша статистика:\n"
            f"Последний результат: {last_score}/{len(quiz_data)}\n"
            f"Завершено: {completed_at}"
        )
    else:
        await message.answer("Вы еще не проходили квиз. Начните с команды /quiz")

async def cmd_leaderboard(message: types.Message):
    """Показать таблицу лидеров"""
    leaderboard = await get_leaderboard()
    
    if not leaderboard:
        await message.answer("Таблица лидеров пуста")
        return
    
    leaderboard_text = "Таблица лидеров:\n\n"
    for idx, (username, full_name, score) in enumerate(leaderboard, 1):
        # Используем полное имя, если есть, иначе username, иначе "Аноним"
        name = full_name
        if not name and username:
            name = f"@{username}"
        if not name:
            name = "Аноним"
        
        leaderboard_text += f"{idx}. {name}: {score}/{len(quiz_data)}\n"
    
    await message.answer(leaderboard_text)

# Регистрация обработчиков callback
def register_handlers(dp):
    """Регистрация всех обработчиков квиза"""
    dp.message.register(cmd_quiz, Command("quiz"))
    dp.message.register(cmd_quiz, F.text == "Начать квиз")
    dp.message.register(cmd_stats, Command("stats"))
    dp.message.register(cmd_stats, F.text == "Моя статистика")
    dp.message.register(cmd_leaderboard, Command("leaderboard"))
    dp.message.register(cmd_leaderboard, F.text == "Таблица лидеров")
    
    # Обработчик для всех ответов на вопросы
    dp.callback_query.register(handle_answer, F.data.startswith("answer_"))
