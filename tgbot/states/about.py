from aiogram.dispatcher.filters.state import StatesGroup, State


class About(StatesGroup):
    About_ru = State()
    About_uz = State()
    Photo = State()
    Photo_uz = State()
    Confirm = State()

    Contact_ru = State()
    Contact_uz = State()
    Confirm1 = State()