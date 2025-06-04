# handlers/top_100.py

from aiogram import Router, types
from database.db import get_movies_connection
from database.queries import GET_TOP_100_MOVIES  # Убедись, что это строка с SQL-запросом

router = Router()

@router.message(lambda message: message.text == "🏆 Топ-100 фильмов")
async def send_top_100_movies(message: types.Message):
    with get_movies_connection() as conn:
        cur = conn.cursor()
        cur.execute(GET_TOP_100_MOVIES)
        movies = cur.fetchall()

    if not movies:
        await message.answer("Фильмы не найдены.")
        return

    text = "🏆 Топ-100 фильмов:\n\n"
    for i, movie in enumerate(movies, start=1):
        title, year, rating = movie
        text += f"{i}. {title}\n   Год: {year}, Рейтинг: ⭐{rating}\n\n"

    max_length = 4096
    messages_text = [text[i:i + max_length] for i in range(0, len(text), max_length)]

    for msg in messages_text:
        await message.answer(msg)