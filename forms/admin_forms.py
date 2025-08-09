from aiogram.fsm.state import State, StatesGroup


class CreatePeer(StatesGroup):
    name = State()
    tg_username = State()
    confirm = State()


class GenerateConfig(StatesGroup):
    name = State()


class DeletePeer(StatesGroup):
    name = State()
    confirm = State()
