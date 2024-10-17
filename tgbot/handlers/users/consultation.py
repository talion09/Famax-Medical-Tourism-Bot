from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.handlers.users.start import ru_language, bot_start, admins_list
from tgbot.states.users import Consul


async def enrol(message):
    enroll = ReplyKeyboardMarkup(resize_keyboard=True)
    if await ru_language(message):
        enroll.add(KeyboardButton(text="Записаться"))
        enroll.add(KeyboardButton(text="Назад"))
    else:
        enroll.add(KeyboardButton(text="Ro'yxatdan o'tish"))
        enroll.add(KeyboardButton(text="Ortga"))
    return enroll


async def choose_consul(message: types.Message):
    db = message.bot.get("db")
    _ = message.bot.get("lang")
    specialists = []
    uz_specialists = []
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for id, full_name, specialist, uz_specialist, photo_id, ru_text, uz_text in await db.select_all_doctors():
        if await ru_language(message):
            if specialist not in specialists:
                specialists.append(specialist)
                markup.insert(KeyboardButton(text=specialist))
        else:
            if uz_specialist not in uz_specialists:
                uz_specialists.append(uz_specialist)
                markup.insert(KeyboardButton(text=uz_specialist))
    text5 = _("Назад")
    markup.add(KeyboardButton(text=text5))
    text6 = _("На чью консультацию Вы хотите записаться?")
    await message.answer(text6, reply_markup=markup)
    await Consul.Specialist.set()


# Consul.Specialist
async def consul(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    _ = message.bot.get("lang")
    enroll = await enrol(message)
    if await ru_language(message):
        doctor = await db.select_doctor(specialist=message.text)
    else:
        doctor = await db.select_doctor(uz_specialist=message.text)
    if message.text in ["Назад", "Ortga"]:
        await bot_start(message, state)
    else:
        try:
            photo_id = doctor.get("photo_id")
            text01 = _("Записаться на консультацию")
            await message.bot.send_photo(message.chat.id, photo_id, f"{text01} <b>{message.text}</b> ?", reply_markup=enroll)
            await state.update_data(doc=message.text)
            await Consul.Confirm.set()
        except:
            await state.reset_state()
            await choose_consul(message)


# Consul.Confirm
async def confirm_consul(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    _ = message.bot.get("lang")
    menu = await admins_list(message)
    data = await state.get_data()
    doc = data.get("doc")
    if message.text in ["Назад", "Ortga"]:
        await bot_start(message, state)
    elif message.text in ["Записаться", "Ro'yxatdan o'tish"]:
        text = _(f"Вы успешно записались на консультацию")
        await message.answer(f"{text} ({doc})!", reply_markup=menu)
        user = await db.select_user(telegram_id=int(message.from_user.id))
        full_name = user.get("full_name")
        number = user.get("number")
        language = user.get("language")
        username = user.get("username")
        if username:
            name = f"@{username}"
        else:
            name = f"<a href='tg://user?id={message.from_user.id}'>{full_name}</a>"
        try:
            for id, group_id, group_name in await db.select_all_groups():
                group_text = f"{name}, записался на консультацию {doc}\n" \
                             f"Номер телефона: {number}\n" \
                             f"Язык: {language}"
                await message.bot.send_message(chat_id=int(group_id), text=group_text)
        except:
            pass

    await state.reset_state()


def register_consultation(dp: Dispatcher):
    dp.register_message_handler(choose_consul, text=["📝 Онлайн Консультация", "📝 Onlayn Konsultatsiya"])
    dp.register_message_handler(consul, state=Consul.Specialist)
    dp.register_message_handler(confirm_consul, text=["Назад", "Ortga",
                                                      "Записаться", "Ro'yxatdan o'tish"], state=Consul.Confirm)
