from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from src.core.states import SettingsState
from src.keyboards.inline import get_settings_menu, get_back_keyboard, get_main_menu
from src.models.user import get_user, update_user_name

router=Router()

@router.message(Command("settings"))
@router.callback_query(F.data=="settings")
async def cmd_settings(event: Message | CallbackQuery):
    user_id=event.from_user.id
    user_data=await get_user(user_id)

    text=(
        " **Настройки**\n\n"
        f" Имя: {user_data['first_name'] if user_data else 'Не задано'}\n"
        f" ID: {user_id}\n\n"
        "Выберите действие:"
    )

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text, reply_markup=get_settings_menu(), parse_mode="Markdown")
        await event.answer()
    else:
        await event.answer(text, reply_markup=get_settings_menu(), parse_mode="Markdown")

@router.callback_query(F.data == "edit_name")
async def edit_name_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        " Введите новое имя:",
        reply_markup=get_back_keyboard()
    )
    await state.set_state(SettingsState.waiting_for_name)
    await callback.answer()

@router.message(SettingsState.waiting_for_name)
async def process_name_update(message: Message, state: FSMContext):
    new_name = message.text.strip()
    if len(new_name) < 2:
        await message.answer(" Имя должно быть не менее 2 символов")
        return

    await update_user_name(message.from_user.id, new_name)
    await state.clear()

    await message.answer(
        f" Имя обновлено на: {new_name}",
        reply_markup=get_back_keyboard()
    )
@router.callback_query(F.data == "notifications")
async def notifications_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        " **Уведомления**\n\n"
        "Функционал в разработке.\n"
        "Здесь можно будет настроить:\n"
        " Включение/выключение уведомлений\n"
        " Время тихого режима\n"
        " Типы событий для уведомлений",
        reply_markup=get_back_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        " Главное меню:",
        reply_markup=get_main_menu()
    )
    await callback.answer()