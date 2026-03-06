from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from src.keyboards.inline import get_main_menu
from src.models.user import create_user

router=Router()

@router.message(Command("start"))
async def cmd_start(message:Message):
    user_id=message.from_user.id
    username=message.from_user.username or "Unknown"
    first_name=message.from_user.first_name or "User"

    await create_user(user_id,username,first_name)

    await message.answer(
        f" Привет, {first_name}!\n\n"
        "Я твой AI-Ассистент.\n"
        "Я могу:\n"
        " Отвечать на вопросы по твоим документам\n"
        " Анализировать изображения\n"
        " Помогать с текстами\n\n"
        "Выбери действие:",
        reply_markup=get_main_menu()
    )