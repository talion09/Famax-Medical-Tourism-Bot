from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.filters.is_admin import IsAdmin
from tgbot.handlers.users.start import bot_start
from tgbot.keyboards.default.cancel import cancel
from tgbot.states.about import About
from tgbot.states.users import Admin


async def admin(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.insert(KeyboardButton(text="Группы"))
    markup.insert(KeyboardButton(text="О компании"))
    markup.insert(KeyboardButton(text="Админы"))
    markup.insert(KeyboardButton(text="Врачи"))
    markup.insert(KeyboardButton(text="Назад"))
    await message.answer("Что вы хотите сделать ?", reply_markup=markup)


async def cancel_admin(message: types.Message, state: FSMContext):
    await state.reset_state()
    await admin(message)


async def administrat(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.insert(KeyboardButton(text="Изменить врача"))
    markup.insert(KeyboardButton(text="Добавить врача"))
    markup.insert(KeyboardButton(text="Удалить врача"))
    markup.insert(KeyboardButton(text="Назад"))
    await message.answer("Что вы хотите сделать ?", reply_markup=markup)


# Изменить врача
async def custom_doc(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    doctors = []
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for id, full_name, specialist, uz_specialist, photo_id, ru_text, uz_text in await db.select_all_doctors():
        if full_name not in doctors:
            doctors.append(full_name)
            markup.insert(KeyboardButton(text=full_name))
    markup.insert(KeyboardButton(text="Отменить"))
    await message.answer("Которого врача изменить ?", reply_markup=markup)
    # await message.bot.send_location()
    await Admin.Custom_doc.set()


# Admin.Custom_doc
async def custom_which_doc(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    doc_name = message.text
    doc = await db.select_doctor(full_name=doc_name)
    if message.text == "Отменить":
        await state.reset_state()
        await admin(message)
    else:
        try:
            doc.get("id")
            await message.answer(f"Отправьте фото ({doc_name})", reply_markup=cancel)
            await state.update_data(full_name=doc_name)
            await Admin.Change_doc_photo.set()
        except:
            await state.reset_state()
            await custom_doc(message)


# Change_doc_photo
async def add_doc_text_ru(message: types.Message, state: FSMContext):
    m_photo_id = message.photo[-1].file_id
    await state.update_data(m_photo_id=m_photo_id)
    await message.answer(f"Отправьте резюме врача на русском языке", reply_markup=cancel)
    await Admin.Change_doc_text.set()


# Change_doc_text
async def add_doc_text_uz(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(ru_text=text)
    await message.answer(f"Отправьте резюме врача на узбекском языке", reply_markup=cancel)
    await Admin.Change_doc_uz_text.set()


# Change_doc_uz_text
async def add_doctor(message: types.Message, state: FSMContext):
    uz_text = message.text
    await state.update_data(uz_text=uz_text)
    data = await state.get_data()
    full_name = data.get("full_name")
    m_photo_id = data.get("m_photo_id")
    ru_text = data.get("ru_text")
    text = f"Врач: {full_name}\n" \
           f"Резюме врача на русском языке: \n{ru_text}\n\n" \
           f"Резюме врача на узбекском языке: \n{uz_text}\n\n" \

    await message.bot.send_photo(message.chat.id, m_photo_id)
    await message.answer(text)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.insert(KeyboardButton(text="Отменить"))
    markup.insert(KeyboardButton(text="Верно"))
    await message.answer(f"Все верно?", reply_markup=markup)
    await Admin.Change_doc_confirm.set()


# Change_doc_confirm
async def add_doctor_confirm(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    full_name = data.get("full_name")
    m_photo_id = data.get("m_photo_id")
    ru_text = data.get("ru_text")
    uz_text = data.get("uz_text")
    await db.update_doctor(full_name=full_name, photo_id=m_photo_id)
    await db.update_doctor(full_name=full_name, ru_text=ru_text)
    await db.update_doctor(full_name=full_name, uz_text=uz_text)

    await message.answer(f"Врач обновлен в базе данных")
    await bot_start(message, state)


def register_custom_doctor(dp: Dispatcher):
    dp.register_message_handler(admin, IsAdmin(), text="Администрация")
    dp.register_message_handler(administrat, IsAdmin(), text="Врачи")
    dp.register_message_handler(custom_doc, IsAdmin(), text="Изменить врача")

    dp.register_message_handler(custom_which_doc, IsAdmin(), state=Admin.Custom_doc)
    dp.register_message_handler(add_doc_text_ru, IsAdmin(), state=Admin.Change_doc_photo, content_types=types.ContentTypes.PHOTO)
    dp.register_message_handler(add_doc_text_uz, IsAdmin(), state=Admin.Change_doc_text)
    dp.register_message_handler(add_doctor, IsAdmin(), state=Admin.Change_doc_uz_text)
    dp.register_message_handler(add_doctor_confirm, IsAdmin(), text="Верно", state=Admin.Change_doc_confirm)
    dp.register_message_handler(cancel_admin, IsAdmin(), text="Отменить", state=[Admin, About])




