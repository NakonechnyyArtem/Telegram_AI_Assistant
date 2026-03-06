from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from src.keyboards.inline import get_back_keyboard
from src.models.user import get_user_stats

router = Router()

@router.message(Command("stats"))
@router.callback_query(F.data == "stats")
async def cmd_stats(event: Message | CallbackQuery):
    user_id = event.from_user.id

    stats = await get_user_stats(user_id)

    if stats and stats['total_messages']:
        text = (
            " **Ваша статистика**\n\n"
            f" Сообщений: {stats['total_messages']}\n"
            f" Первый вход: {stats['first_seen'].strftime('%d.%m.%Y %H:%M') if stats['first_seen'] else 'Н/Д'}\n"
            f" Последняя активность: {stats['last_activity'].strftime('%d.%m.%Y %H:%M') if stats['last_activity'] else 'Н/Д'}"
        )
    else:
        text = " **Ваша статистика**\n\nПока нет данных"

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text, reply_markup=get_back_keyboard(), parse_mode="Markdown")
        await event.answer()
    else:
        await event.answer(text, reply_markup=get_back_keyboard(), parse_mode="Markdown")