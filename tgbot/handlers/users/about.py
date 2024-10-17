from aiogram import types, Dispatcher
from tgbot.handlers.users.start import admins_list, ru_language


async def about_us(message: types.Message):
    db = message.bot.get("db")
    menu = await admins_list(message)
    select = await db.select_about(about_id=112)
    about = select.get("about")
    about_uz = select.get("about_uz")
    photo_id = select.get("photo_id")
    photo_id_uz = select.get("photo_id_uz")
    if await ru_language(message):
        await message.bot.send_photo(message.chat.id, photo_id, about, reply_markup=menu)
    else:
        await message.bot.send_photo(message.chat.id, photo_id_uz, about_uz, reply_markup=menu)


async def about_contacts(message: types.Message):
    db = message.bot.get("db")
    select = await db.select_about(about_id=112)
    contacts = select.get("contacts")
    contacts_uz = select.get("contacts_uz")
    if await ru_language(message):
        await message.answer(contacts)
    else:
        await message.answer(contacts_uz)


async def about_doctors(message: types.Message):
    db = message.bot.get("db")
    _ = message.bot.get("lang")
    menu = await admins_list(message)

    doctors = []
    doctors_uz = []
    for id, full_name, specialist, uz_specialist, photo_id, ru_text, uz_text in await db.select_all_doctors():
        if await ru_language(message):
            if full_name not in doctors:
                doctors.append(full_name)
                await message.bot.send_photo(message.chat.id, photo_id, ru_text, reply_markup=menu)
        else:
            if full_name not in doctors_uz:
                doctors_uz.append(full_name)
                await message.bot.send_photo(message.chat.id, photo_id, uz_text, reply_markup=menu)


def register_adout(dp: Dispatcher):
    dp.register_message_handler(about_us, text=["ℹ️ О Нас", "ℹ️ Biz haqimizda"])
    dp.register_message_handler(about_contacts, text=["☎️ Контакты", "☎️ Kontaktlar"])
    dp.register_message_handler(about_doctors, text=["👨‍⚕️ Врачи", "👨‍⚕️ Shifokorlar"])

