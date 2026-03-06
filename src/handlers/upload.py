import os
import asyncio
from pathlib import Path
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from src.core.states import SettingsState
from src.keyboards.inline import get_back_keyboard
from src.services.file_parser import FileParser
from src.core import database

router = Router()

FILES_DIR = Path("files")
FILES_DIR.mkdir(exist_ok=True)


@router.message(Command("upload"))
async def cmd_upload(message: Message):
    await message.answer(
        " **Загрузка файла**\n\n"
        "Отправьте мне файл одним из форматов:\n"
        "  PDF\n"
        "  DOCX\n"
        "  TXT\n\n"
        "Я извлеку текст и сохраню его в базу знаний.",
        parse_mode="Markdown",
        reply_markup=get_back_keyboard()
    )


@router.callback_query(F.data == "upload")
async def upload_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        " **Загрузка файла**\n\n"
        "Отправьте мне файл одним из форматов:\n"
        "  PDF\n"
        "  DOCX\n"
        "  TXT",
        parse_mode="Markdown",
        reply_markup=get_back_keyboard()
    )
    await callback.answer()


@router.message(F.document)
async def handle_document(message: Message, state: FSMContext):
    document = message.document
    file_name = document.file_name
    file_size = document.file_size
    mime_type = document.mime_type

    allowed_types = ['application/pdf', 'text/plain',
                     'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                     'application/msword']

    if mime_type not in allowed_types:
        await message.answer(
            " Неподдерживаемый тип файла.\n"
            "Пожалуйста, отправьте PDF, DOCX или TXT.",
            reply_markup=get_back_keyboard()
        )
        return

    await message.answer(" Загружаю файл...")

    file = await database.bot.get_file(document.file_id)
    file_path = FILES_DIR / f"{message.from_user.id}_{file_name}"

    await database.bot.download_file(file.file_path, file_path)

    await message.answer(" Извлекаю текст...")
    extracted_text = await FileParser.parse_file(str(file_path), mime_type)

    if not extracted_text or extracted_text.startswith("Ошибка"):
        await message.answer(f" {extracted_text}")
        return

    await database.db.save_file(
        user_id=message.from_user.id,
        filename=file_name,
        file_type=mime_type,
        file_size=file_size,
        file_path=str(file_path),
        extracted_text=extracted_text
    )

    await message.answer(
        f" **Файл обработан!**\n\n"
        f" Имя: {file_name}\n"
        f" Размер: {file_size / 1024:.2f} KB\n"
        f" Символов: {len(extracted_text)}\n\n"
        "Теперь вы можете задать вопрос по этому документу!",
        parse_mode="Markdown",
        reply_markup=get_back_keyboard()
    )