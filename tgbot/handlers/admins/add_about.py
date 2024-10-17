from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.filters.is_admin import IsAdmin, IsGroup
from tgbot.handlers.users.start import bot_start
from tgbot.states.about import About
from tgbot.keyboards.default.cancel import cancel


async def add_about(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.insert(KeyboardButton(text="О нас"))
    markup.insert(KeyboardButton(text="Контакты"))
    markup.insert(KeyboardButton(text="Назад"))
    await message.answer("Что Вы хотите изменить?", reply_markup=markup)


async def add_about_def(message: types.Message):
    db = message.bot.get("db")
    await db.add_about(about_id=112, photo_id="AgACAgIAAxkBAANqZAtrhQIPX2OE78JWm8MCL0DsvnQAAufBMRtxgGFIEgKglCMFcJoBAAMCAAN5AAMvBA",
                       photo_id_uz="AgACAgIAAxkBAANqZAtrhQIPX2OE78JWm8MCL0DsvnQAAufBMRtxgGFIEgKglCMFcJoBAAMCAAN5AAMvBA",
                       about="О нас", about_uz="Biz haqimizda", contacts="Контакты", contacts_uz="Kontaktlar")
    await message.answer("Функция проведена успешна")


async def about_ru(message: types.Message):
    await message.answer("Введите текст <b>О нас</b> для русскоязычных пользователей", reply_markup=cancel)
    await About.About_ru.set()


# About.About_ru
async def about_uz(message: types.Message, state: FSMContext):
    await message.answer("Введите текст <b>О нас</b> для узбекоязычных пользователей", reply_markup=cancel)
    await state.update_data(about_ru=message.text)
    await About.About_uz.set()


# About.About_uz
async def about_photo(message: types.Message, state: FSMContext):
    await message.answer("Отправьте фото <b>О нас</b> для русскоязычных пользователей", reply_markup=cancel)
    await state.update_data(about_uz=message.text)
    await About.Photo.set()


# About.Photo
async def about_photo_uz(message: types.Message, state: FSMContext):
    await message.answer("Отправьте фото <b>О нас</b> для узбекоязычных пользователей", reply_markup=cancel)
    await state.update_data(about_photo=message.photo[-1].file_id)
    await About.Photo_uz.set()


# About.Photo_uz
async def about_confirm(message: types.Message, state: FSMContext):
    await state.update_data(about_photo_uz=message.photo[-1].file_id)
    data = await state.get_data()
    about_ru = data.get("about_ru")
    about_uz = data.get("about_uz")
    about_photo = data.get("about_photo")
    await message.bot.send_photo(message.from_user.id, photo=about_photo, caption=about_ru)
    await message.bot.send_photo(message.from_user.id, photo=message.photo[-1].file_id, caption=about_uz)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.insert(KeyboardButton(text="Отменить"))
    markup.insert(KeyboardButton(text="Верно"))
    await message.answer(f"Все верно?", reply_markup=markup)
    await About.Confirm.set()


# About.Confirm
async def about_confirm1(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    about_ru = data.get("about_ru")
    about_uz = data.get("about_uz")
    about_photo = data.get("about_photo")
    about_photo_uz = data.get("about_photo_uz")
    await message.bot.send_photo(message.from_user.id, photo=about_photo, caption=about_ru)
    await message.bot.send_photo(message.from_user.id, photo=about_photo_uz, caption=about_uz)
    await db.update_about(about_id=112, photo_id=about_photo)
    await db.update_about(about_id=112, photo_id_uz=about_photo_uz)
    await db.update_about(about_id=112, about=about_ru)
    await db.update_about(about_id=112, about_uz=about_uz)
    await message.answer("Отлично, <b>О нас</b> добавлено в базу данных!")
    await bot_start(message, state)


async def contacts_ru(message: types.Message):
    await message.answer("Введите текст <b>Контакты</b> для русскоязычных пользователей", reply_markup=cancel)
    await About.Contact_ru.set()


# About.Contact_ru
async def contacts_uz(message: types.Message, state: FSMContext):
    await message.answer("Введите текст <b>Контакты</b> для узбекоязычных пользователей", reply_markup=cancel)
    await state.update_data(contacts_ru=message.text)
    await About.Contact_uz.set()


# About.Contact_ru
async def contacts_confirm(message: types.Message, state: FSMContext):
    await state.update_data(contacts_uz=message.text)
    data = await state.get_data()
    contacts_ru = data.get("contacts_ru")
    await message.answer(contacts_ru)
    await message.answer(message.text)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.insert(KeyboardButton(text="Отменить"))
    markup.insert(KeyboardButton(text="Верно"))
    await message.answer(f"Все верно?", reply_markup=markup)
    await About.Confirm1.set()


# About.Confirm1
async def contacts_confirm1(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    contacts_ru = data.get("contacts_ru")
    contacts_uz = data.get("contacts_uz")
    await message.answer(contacts_ru)
    await message.answer(contacts_uz)
    await db.update_about(about_id=112, contacts=contacts_ru)
    await db.update_about(about_id=112, contacts_uz=contacts_uz)
    await message.answer("Отлично, <b>Контакты</b> добавлено в базу данных!")
    await bot_start(message, state)



def register_add_about(dp: Dispatcher):
    dp.register_message_handler(add_about, IsAdmin(), text="О компании")
    dp.register_message_handler(add_about_def, IsAdmin(), Command("add_about_def"))
    dp.register_message_handler(about_ru, IsAdmin(), text="О нас")
    dp.register_message_handler(about_uz, IsAdmin(), state=About.About_ru)
    dp.register_message_handler(about_photo, IsAdmin(), state=About.About_uz)
    dp.register_message_handler(about_photo_uz, IsAdmin(), state=About.Photo, content_types=types.ContentType.PHOTO)
    dp.register_message_handler(about_confirm, IsAdmin(), state=About.Photo_uz, content_types=types.ContentType.PHOTO)
    dp.register_message_handler(about_confirm1, IsAdmin(), text="Верно", state=About.Confirm)

    dp.register_message_handler(contacts_ru, IsAdmin(), text="Контакты")
    dp.register_message_handler(contacts_uz, IsAdmin(), state=About.Contact_ru)
    dp.register_message_handler(contacts_confirm, IsAdmin(), state=About.Contact_uz)
    dp.register_message_handler(contacts_confirm1, IsAdmin(), state=About.Confirm1)


