from aiogram.fsm.state import State, StatesGroup

class Anouncement(StatesGroup):
    announcement = State()
    confirm = State()


class GetConfig(StatesGroup):
    index = State()


class GetUsersConfig(StatesGroup):
    user = State()
    index = State()


class CreateNewConfig(StatesGroup):
    user = State()
    restart_server = State()
    send_file = State()


class RegenerateConfigs(StatesGroup):
    confirm = State()


class RestartServer(StatesGroup):
    confirm = State()


class RestartWireguard(StatesGroup):
    confirm = State()


class AddUser(StatesGroup):
    username = State()
    confirm = State()


class RemoveUser(StatesGroup):
    username = State()
    confirm = State()
