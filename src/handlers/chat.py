from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command
from src.services.ai_client import GeminiClient
from src.core.database import db

router = Router()
ai_client = GeminiClient()


@router.message(~F.command)
async def handle_message(message: Message):
    try:
        user_id = message.from_user.id
        user_text = message.text

        if not user_text:
            return

        await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

        context = await get_rag_context(user_id, user_text)

        await message.answer("Думаю...")
        response = await ai_client.ask(user_text, context)

        await save_message_history(user_id, user_text, response)

        await message.answer(
            f"**Ответ AI:**\n\n{response}",
            parse_mode="Markdown"
        )

    except Exception as e:
        print(f"Ошибка в handle_message: {e}")
        await message.answer(f"Произошла ошибка при обработке: {type(e).__name__}")


async def get_rag_context(user_id: int, query: str, limit: int = 3) -> str:
    try:
        async with db.pool.acquire() as conn:
            files = await conn.fetch(
                """
                SELECT filename, extracted_text
                FROM uploaded_files
                WHERE user_id = $1
                  AND extracted_text IS NOT NULL
                    LIMIT $2
                """,
                user_id, limit
            )

        if not files:
            return None

        context = "Документы пользователя:\n\n"
        for file in files:
            context += f"Файл: {file['filename']}\n"
            context += f"{file['extracted_text'][:1000]}...\n\n"

        return context
    except Exception as e:
        print(f"Ошибка получения контекста: {e}")
        return None


async def save_message_history(user_id: int, user_message: str, ai_response: str):
    try:
        async with db.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO message_history (user_id, message_text, message_type)
                VALUES ($1, $2, $3)
                """,
                user_id, f"User: {user_message} | AI: {ai_response}", "chat"
            )
    except Exception as e:
        print(f"Ошибка сохранения истории: {e}")