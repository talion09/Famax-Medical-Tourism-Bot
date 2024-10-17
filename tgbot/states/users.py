from aiogram.dispatcher.filters.state import StatesGroup, State


class User(StatesGroup):
    Lang = State()
    Name = State()
    Phone = State()
    Next = State()


class Custom(StatesGroup):
    Lang = State()
    Name = State()
    Phone = State()


class Admin(StatesGroup):
    Delete_doc = State()
    Add_doc = State()
    Add_doc_specialist = State()
    Add_doc_specialist_uz = State()
    Add_doc_photo = State()
    Add_doc_text = State()
    Add_doc_uz_text = State()
    Add_doc_confirm = State()

    Change_doc_photo = State()
    Change_doc_text = State()
    Change_doc_uz_text = State()
    Change_doc_confirm = State()

    Delete_admin = State()
    Add_admin = State()

    Custom_doc = State()


class Consul(StatesGroup):
    Confirm = State()
    Specialist = State()





