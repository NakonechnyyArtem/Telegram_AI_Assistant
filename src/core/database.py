import asyncpg
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class Database:
    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = int(os.getenv("DB_PORT", 5432))
        self.user = os.getenv("DB_USER", "postgres")
        self.password = os.getenv("DB_PASSWORD", "mypassword")
        self.database = os.getenv("DB_NAME", "mybot_db")
        self.pool: Optional[asyncpg.Pool] = None

    async def create_pool(self):
        """Создание пула соединений"""
        if self.pool is None:
            self.pool = await asyncpg.create_pool(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                min_size=5,
                max_size=20
            )
            print("✅ Пул соединений с БД создан")

    async def close_pool(self):
        """Закрытие пула соединений"""
        if self.pool:
            await self.pool.close()
            print("🔌 Пул соединений закрыт")

    async def init_tables(self):
        """Создание таблиц"""
        async with self.pool.acquire() as conn:
            # Создаем расширение для векторного поиска (RAG)
            await conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")

            # Таблица пользователей
            await conn.execute("""
                               CREATE TABLE IF NOT EXISTS users
                               (
                                   user_id
                                   BIGINT
                                   PRIMARY
                                   KEY,
                                   username
                                   VARCHAR
                               (
                                   255
                               ),
                                   first_name VARCHAR
                               (
                                   255
                               ),
                                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                   last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                   );
                               """)

            # Таблица истории сообщений
            await conn.execute("""
                               CREATE TABLE IF NOT EXISTS message_history
                               (
                                   id
                                   SERIAL
                                   PRIMARY
                                   KEY,
                                   user_id
                                   BIGINT
                                   REFERENCES
                                   users
                               (
                                   user_id
                               ),
                                   message_text TEXT,
                                   message_type VARCHAR
                               (
                                   50
                               ),
                                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                   );
                               """)

            print("✅ Таблицы созданы")

    async def add_user(self, user_id: int, username: str, first_name: str):
        """Добавление пользователя"""
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO users (user_id, username, first_name)
                VALUES ($1, $2, $3) ON CONFLICT (user_id) DO
                UPDATE
                    SET last_activity = CURRENT_TIMESTAMP
                """,
                user_id, username, first_name
            )

    async def get_user(self, user_id: int):
        """Получение пользователя"""
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(
                "SELECT * FROM users WHERE user_id = $1",
                user_id
            )

db = Database()