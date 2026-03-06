from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Помощь", callback_data="help")
    builder.button(text="Настройки", callback_data="settings")
    builder.button(text="Статистика", callback_data="stats")
    builder.adjust(2, 1)
    return builder.as_markup()

def get_settings_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Изменить имя", callback_data="edit_name")
    builder.button(text="Уведомления", callback_data="notifications")
    builder.button(text="Назад", callback_data="back_to_main")
    builder.adjust(1)
    return builder.as_markup()

def get_back_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Назад", callback_data="back_to_main")
    return builder.as_markup()