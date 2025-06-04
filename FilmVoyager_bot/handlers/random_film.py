# handlers/random_movie.py

from aiogram import Router, types
from database.db import get_movies_connection
from database.queries import get_random_movie

router = Router()

@router.message(lambda message: message.text == "🎲 Случайный фильм")
async def send_random_movie(message: types.Message):
    with get_movies_connection() as conn:
        cur = conn.cursor()
        cur.execute(get_random_movie())
        movie = cur.fetchone()

    if not movie:
        await message.answer("Фильм не найден.")
        return

    await message.answer(f" {movie[2]} Год: {movie[5]}, Рейтинг: ⭐{movie[9]}", parse_mode="HTML")