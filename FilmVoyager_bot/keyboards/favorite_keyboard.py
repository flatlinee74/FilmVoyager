# keyboards/favorite_keyboard.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def build_favorite_list(movies_info):
    keyboard = []
    for movie_id, title, year, rating in movies_info:
        btn_text = f"{title} ({year}) ⭐{rating or '?'}"
        callback_data = f"remove_from_favorites_{movie_id}"
        keyboard.append([InlineKeyboardButton(text=btn_text, callback_data=callback_data)])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def build_add_button(movie_id):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
        text="➕ Добавить в избранное",
        callback_data=f"add_to_favorites_{movie_id}"
    )]])


def build_remove_button(movie_id):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
        text="➖ Убрать из избранного",
        callback_data=f"remove_from_favorites_{movie_id}"
    )]])