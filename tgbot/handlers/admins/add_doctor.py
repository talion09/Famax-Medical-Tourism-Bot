from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.filters.is_admin import IsAdmin
from tgbot.handlers.users.start import bot_start
from tgbot.keyboards.default.cancel import cancel
from tgbot.states.users import Admin


async def admin(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.insert(KeyboardButton(text="Группы"))
    markup.insert(KeyboardButton(text="Админы"))
    markup.insert(KeyboardButton(text="Врачи"))
    markup.insert(KeyboardButton(text="Назад"))
    await message.answer("Что вы хотите сделать ?", reply_markup=markup)


async def administrat(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.insert(KeyboardButton(text="Добавить врача"))
    markup.insert(KeyboardButton(text="Удалить врача"))
    markup.insert(KeyboardButton(text="Назад"))
    await message.answer("Что вы хотите сделать ?", reply_markup=markup)


async def delete_doc(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    specialists = []
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for id, full_name, specialist, uz_specialist, photo_id, ru_text, uz_text in await db.select_all_doctors():
        if specialist not in specialists:
            specialists.append(specialist)
            markup.insert(KeyboardButton(text=full_name))
    markup.insert(KeyboardButton(text="Отменить"))
    await message.answer("Которого врача удалить ?", reply_markup=markup)
    await Admin.Delete_doc.set()


# Admin.Delete_doc
async def delete_which_doc(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    doc_name = message.text
    doc = await db.select_doctor(full_name=doc_name)
    if message.text == "Отменить":
        await state.reset_state()
        await admin(message)
    else:
        try:
            doc.get("specialist")
            await db.delete_doctor(full_name=doc_name)
            await message.answer(f"Врач {doc_name} был удален!")
            await bot_start(message, state)
        except:
            await message.answer(f"Врач {doc_name} не существует!")
            await bot_start(message, state)


async def cancel_admin(message: types.Message, state: FSMContext):
    await state.reset_state()
    await admin(message)


async def add_doc(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    await message.answer("Введите полное Фамилие и Имя врача", reply_markup=cancel)
    await Admin.Add_doc.set()


# Add_doc
async def add_which_doc(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    doc = message.text
    doctor = await db.select_doctor(full_name=doc)
    try:
        doctor.get("specialist")
        await message.answer("Этот врач уже добавлен в базу данных!")
        await state.reset_state()
        await admin(message)
    except:
        await state.update_data(full_name=doc)
        await message.answer(f"Какой специалист врач {doc}? (Травматолог, Онколог)", reply_markup=cancel)
        await Admin.Add_doc_specialist.set()


# Add_doc_specialist
async def add_which_doc_uz(message: types.Message, state: FSMContext):
    data = await state.get_data()
    doc = data.get("full_name")
    specialist = message.text
    await state.update_data(specialist=specialist)
    await message.answer(f"Какой специалист врач {doc} на узбекском? (Travmatolog, Onkolog)", reply_markup=cancel)
    await Admin.Add_doc_specialist_uz.set()


# Add_doc_specialist_uz
async def add_doc_photo(message: types.Message, state: FSMContext):
    specialist_uz = message.text
    await state.update_data(specialist_uz=specialist_uz)
    await message.answer(f"Отправьте фото", reply_markup=cancel)
    await Admin.Add_doc_photo.set()


# Add_doc_photo
async def add_doc_text_ru(message: types.Message, state: FSMContext):
    m_photo_id = message.photo[-1].file_id
    await state.update_data(m_photo_id=m_photo_id)
    await message.answer(f"Отправьте резюме врача на русском языке", reply_markup=cancel)
    await Admin.Add_doc_text.set()


# Add_doc_text
async def add_doc_text_uz(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(ru_text=text)
    await message.answer(f"Отправьте резюме врача на узбекском языке", reply_markup=cancel)
    await Admin.Add_doc_uz_text.set()


# Add_doc_uz_text
async def add_doctor(message: types.Message, state: FSMContext):
    uz_text = message.text
    await state.update_data(uz_text=uz_text)
    data = await state.get_data()
    full_name = data.get("full_name")
    specialist = data.get("specialist")
    specialist_uz = data.get("specialist_uz")
    m_photo_id = data.get("m_photo_id")
    ru_text = data.get("ru_text")
    text = f"Врач: {full_name}\n" \
           f"Специалист: {specialist}\n" \
           f"Специалист на узбекском: {specialist_uz}\n" \
           f"Резюме врача на русском языке: \n{ru_text}\n\n" \
           f"Резюме врача на узбекском языке: \n{uz_text}\n\n" \

    await message.bot.send_photo(message.chat.id, m_photo_id)
    await message.answer(text)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.insert(KeyboardButton(text="Отменить"))
    markup.insert(KeyboardButton(text="Верно"))
    await message.answer(f"Все верно?", reply_markup=markup)
    await Admin.Add_doc_confirm.set()


# Add_doc_confirm
async def add_doctor_confirm(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    full_name = data.get("full_name")
    specialist = data.get("specialist")
    specialist_uz = data.get("specialist_uz")
    m_photo_id = data.get("m_photo_id")
    ru_text = data.get("ru_text")
    uz_text = data.get("uz_text")
    await db.add_doctor(full_name, specialist, specialist_uz, m_photo_id, ru_text, uz_text)
    await message.answer(f"Врач добавлен в базу данных")
    await bot_start(message, state)


def register_add_doctor(dp: Dispatcher):
    dp.register_message_handler(admin, IsAdmin(), text="Администрация")
    dp.register_message_handler(administrat, IsAdmin(), text="Врачи")
    dp.register_message_handler(delete_doc, IsAdmin(), text="Удалить врача")
    dp.register_message_handler(delete_which_doc, IsAdmin(), state=Admin.Delete_doc)
    dp.register_message_handler(add_doc, IsAdmin(), text="Добавить врача")

    dp.register_message_handler(add_which_doc, IsAdmin(), state=Admin.Add_doc)
    dp.register_message_handler(add_which_doc_uz, IsAdmin(), state=Admin.Add_doc_specialist)
    dp.register_message_handler(add_doc_photo, IsAdmin(), state=Admin.Add_doc_specialist_uz)
    dp.register_message_handler(add_doc_text_ru, IsAdmin(), state=Admin.Add_doc_photo, content_types=types.ContentTypes.PHOTO)
    dp.register_message_handler(add_doc_text_uz, IsAdmin(), state=Admin.Add_doc_text)
    dp.register_message_handler(add_doctor, IsAdmin(), state=Admin.Add_doc_uz_text)
    dp.register_message_handler(add_doctor_confirm, IsAdmin(), text="Верно", state=Admin.Add_doc_confirm)




