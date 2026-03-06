from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from src.keyboards.inline import get_back_keyboard

router = Router()


@router.message(Command("help"))
@router.callback_query(F.data == "help")
async def cmd_help(event: Message | CallbackQuery):
    text = (
        " **Помощь**\n\n"
        "**Команды:**\n"
        "/start - Запустить бота\n"
        "/help - Показать эту справку\n"
        "/settings - Настройки профиля\n"
        "/upload - Загрузить документ (скоро)\n\n"
        "**Как работать:**\n"
        "1. Загрузи документ через /upload\n"
        "2. Задай вопрос по документу\n"
        "3. Получи ответ от AI\n\n"
    )

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text, reply_markup=get_back_keyboard(), parse_mode="Markdown")
        await event.answer()
    else:
        await event.answer(text, reply_markup=get_back_keyboard(), parse_mode="Markdown")