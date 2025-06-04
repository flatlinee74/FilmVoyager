from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import get_movies_connection
from database.queries import GET_NEWEST_MOVIES

def build_newest_keyboard(offset=0, limit=20):
    buttons = []
    
    if offset > 0:
        buttons.append(InlineKeyboardButton(
            text="⬅️ Предыдущие",
            callback_data=f"newest_{offset - limit}"
        ))
    
    buttons.append(InlineKeyboardButton(
        text="➡️ Следующие",
        callback_data=f"newest_{offset + limit}"
    ))
    
    return InlineKeyboardMarkup(inline_keyboard=[buttons])

def fetch_newest_movies(limit=20, offset=0):
    try:
        with get_movies_connection() as conn:
            cur = conn.cursor()
            cur.execute(GET_NEWEST_MOVIES, (limit, offset))
            movies = cur.fetchall()
            print(f"SQL запрос выполнен, найдено фильмов: {len(movies)}")
            return movies
    except Exception as e:
        print(f"Ошибка при получении фильмов: {e}")
        return None