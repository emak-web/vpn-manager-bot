from aiogram.filters.callback_data import CallbackData


class ChooseUserCallbackFactory(CallbackData, prefix='user'):
    user_id: int
    fullname: str