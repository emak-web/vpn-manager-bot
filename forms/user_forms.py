from aiogram.fsm.state import State, StatesGroup

class GetConfig(StatesGroup):
    index = State()