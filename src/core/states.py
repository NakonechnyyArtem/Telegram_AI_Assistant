from aiogram.fsm.state import State, StatesGroup

class SettingsState(StatesGroup):
    waiting_for_name=State()
    waiting_for_setting=State()
