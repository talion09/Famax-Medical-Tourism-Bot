from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👨‍⚕️ Врачи"),
            KeyboardButton(text="📝 Онлайн Консультация")
        ],
        [
            KeyboardButton(text="ℹ️ О Нас"),
            KeyboardButton(text="☎️ Контакты"),
        ],
        [
            KeyboardButton(text="⚙️ Настройки"),
        ],
        [
            KeyboardButton(text="Администрация"),
        ]
    ], resize_keyboard=True)


admin_menu_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👨‍⚕️ Shifokorlar"),
            KeyboardButton(text="📝 Onlayn Konsultatsiya")
        ],
        [
            KeyboardButton(text="ℹ️ Biz haqimizda"),
            KeyboardButton(text="☎️ Kontaktlar"),
        ],
        [
            KeyboardButton(text="⚙️ Sozlamalar")
        ],
        [
            KeyboardButton(text="Администрация"),
        ]
    ], resize_keyboard=True)


m_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👨‍⚕️ Врачи"),
            KeyboardButton(text="📝 Онлайн Консультация")
        ],
        [
            KeyboardButton(text="ℹ️ О Нас"),
            KeyboardButton(text="☎️ Контакты"),
        ],
        [
            KeyboardButton(text="⚙️ Настройки"),
        ]
    ], resize_keyboard=True)


m_menu_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👨‍⚕️ Shifokorlar"),
            KeyboardButton(text="📝 Onlayn Konsultatsiya")
        ],
        [
            KeyboardButton(text="ℹ️ Biz haqimizda"),
            KeyboardButton(text="☎️ Kontaktlar"),
        ],
        [
            KeyboardButton(text="⚙️ Sozlamalar"),
        ]
    ], resize_keyboard=True)