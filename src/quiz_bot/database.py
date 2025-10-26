# Модуль базы данных

import aiosqlite
from .config import config

async def create_tables():
    """Создание таблиц базы данных"""
    async with aiosqlite.connect(config.DB_NAME) as db:
        # Таблица для состояния квиза
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (
            user_id INTEGER PRIMARY KEY,
            question_index INTEGER,
            score INTEGER DEFAULT 0
        )''')
        
        # Таблица для статистики пользователей
        await db.execute('''CREATE TABLE IF NOT EXISTS user_stats (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            full_name TEXT,
            last_score INTEGER,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        await db.commit()

async def get_quiz_state(user_id):
    """Получение состояния квиза пользователя"""
    async with aiosqlite.connect(config.DB_NAME) as db:
        async with db.execute(
            'SELECT question_index, score FROM quiz_state WHERE user_id = ?', 
            (user_id,)
        ) as cursor:
            result = await cursor.fetchone()
            if result:
                return result[0], result[1]
            return 0, 0

async def update_quiz_state(user_id, question_index, score):
    """Обновление состояния квиза"""
    async with aiosqlite.connect(config.DB_NAME) as db:
        await db.execute(
            'INSERT OR REPLACE INTO quiz_state (user_id, question_index, score) VALUES (?, ?, ?)',
            (user_id, question_index, score)
        )
        await db.commit()

async def save_quiz_result(user_id, username, full_name, score):
    """Сохранение результата квиза"""
    async with aiosqlite.connect(config.DB_NAME) as db:
        # Используем INSERT OR REPLACE с PRIMARY KEY на user_id
        await db.execute(
            '''INSERT OR REPLACE INTO user_stats 
               (user_id, username, full_name, last_score, completed_at) 
               VALUES (?, ?, ?, ?, datetime('now'))''',
            (user_id, username, full_name, score)
        )
        await db.commit()

async def get_user_stats(user_id):
    """Получение статистики пользователя"""
    async with aiosqlite.connect(config.DB_NAME) as db:
        async with db.execute(
            'SELECT last_score, completed_at FROM user_stats WHERE user_id = ?',
            (user_id,)
        ) as cursor:
            return await cursor.fetchone()

async def get_leaderboard(limit=10):
    """Получение таблицы лидеров"""
    async with aiosqlite.connect(config.DB_NAME) as db:
        async with db.execute(
            '''SELECT username, full_name, last_score 
               FROM user_stats 
               ORDER BY last_score DESC 
               LIMIT ?''',
            (limit,)
        ) as cursor:
            return await cursor.fetchall()