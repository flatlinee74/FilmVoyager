# keyboards/genre_keyboard.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import get_movies_connection
from database.queries import GET_GENRES, GET_MOVIES_BY_GENRE_IDS, COUNT_GENRE_MOVIES


def build_genre_keyboard(genres, selected_ids=None):
    """Создаёт инлайн-клавиатуру с жанрами и галочками"""
    selected_ids = selected_ids or []
    keyboard = []
    row = []

    for genre in genres:
        if len(row) == 3:
            keyboard.append(row)
            row = []

        emoji = "✅" if genre["id"] in selected_ids else "🎭"
        row.append(InlineKeyboardButton(
            text=f"{emoji} {genre['name']}",
            callback_data=f"select_genre_{genre['id']}"
        ))

    if row:
        keyboard.append(row)

    # Кнопка "Показать фильмы"
    keyboard.append([InlineKeyboardButton(text="🎬 Показать фильмы", callback_data="show_movies_by_genres")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def fetch_all_genres():
    """Получает список всех жанров из БД"""
    with get_movies_connection() as conn:
        cur = conn.cursor()
        cur.execute(GET_GENRES)
        return [{"id": r[0], "name": r[1]} for r in cur.fetchall()]


def fetch_movies_by_genre_ids(genre_ids, limit=20, offset=0):
    """Возвращает фильмы по списку жанров"""
    sql = GET_MOVIES_BY_GENRE_IDS(genre_ids, limit, offset)
    count_sql = COUNT_GENRE_MOVIES(genre_ids)

    with get_movies_connection() as conn:
        cur = conn.cursor()
        cur.execute(count_sql)
        total = cur.fetchone()[0]

        if total == 0:
            return {"movies": [], "total": 0}

        cur.execute(sql)
        movies = cur.fetchall()

    return {
        "movies": movies,
        "total": total
    }