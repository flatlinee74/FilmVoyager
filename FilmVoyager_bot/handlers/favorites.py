# handlers/favorites.py

from aiogram import Router, types
from aiogram.types import CallbackQuery
from database.favorites_db import get_favorites_connection
from database.db import get_movies_connection
from database.queries import GET_FAVORITES, GET_MOVIE_BY_ID
from keyboards.favorite_keyboard import build_favorite_list, build_add_button, build_remove_button

router = Router()

@router.message(lambda message: message.text == "❤️ Избранное")
async def show_favorites(message: types.Message):
    user_id = message.from_user.id

    with get_favorites_connection() as conn:
        cur = conn.cursor()
        cur.execute(GET_FAVORITES, (user_id,))
        favorite_rows = cur.fetchall()

    if not favorite_rows:
        await message.answer("Избранное пусто")
        return

    # Получаем данные по каждому фильму из основной базы
    movies_info = []
    with get_movies_connection() as movie_conn:
        movie_cur = movie_conn.cursor()
        for row in favorite_rows:
            movie_id = row[0]
            movie_cur.execute(GET_MOVIE_BY_ID, (movie_id,))
            data = movie_cur.fetchone()
            if data:
                full_title, full_year, full_rating = data
                movies_info.append((movie_id, full_title, full_year, full_rating))

    if not movies_info:
        await message.answer("Не удалось загрузить информацию о фильмах")
        return

    markup = build_favorite_list([
        (movie_id, title, year, rating) for movie_id, title, year, rating in movies_info
    ])

    await message.answer("❤️ Ваши избранные фильмы:", reply_markup=markup)


@router.callback_query(lambda call: call.data.startswith("add_to_favorites_"))
async def add_to_favorites(call: CallbackQuery):
    movie_id = call.data.split("_")[3]
    user_id = call.from_user.id

    with get_favorites_connection() as conn:
        cur = conn.cursor()
        cur.execute("INSERT OR IGNORE INTO favorites(user_id, movie_id) VALUES (?, ?)", (user_id, movie_id))
        conn.commit()

    await call.answer("Фильм добавлен в избранное")
    await call.message.edit_reply_markup(reply_markup=build_remove_button(movie_id))


@router.callback_query(lambda call: call.data.startswith("remove_from_favorites_"))
async def remove_from_favorites(call: CallbackQuery):
    movie_id = call.data.split("_")[3]
    user_id = call.from_user.id

    with get_favorites_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM favorites WHERE user_id = ? AND movie_id = ?", (user_id, movie_id))
        conn.commit()

    # Обновляем список после удаления
    await call.answer("Фильм удален из избранного")
    await show_favorites(call.message)