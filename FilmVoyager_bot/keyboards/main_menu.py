from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_back_button():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
        text="⬅️ Назад",
        callback_data="back_to_main_menu"
    )]])
    
def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🏆 Топ-100 фильмов"),
                KeyboardButton(text="🔍 Поиск по названию"),
                KeyboardButton(text="🎭 По жанрам")
            ],
            [
                KeyboardButton(text="📺 Топ-100 сериалов"),
                KeyboardButton(text="🆕 Новинки"),
                KeyboardButton(text="🎲 Случайный фильм"),
            ],
            [
                KeyboardButton(text="❤️ Избранное"),
                KeyboardButton(text="⬅️ Назад")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )