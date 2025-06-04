# handlers/search_title.py
import sqlite3
from aiogram import Router, types
from aiogram.types import CallbackQuery
from database.db import get_movies_connection
from database.favorites_db import get_favorites_connection
from database.queries import (
    SEARCH_MOVIE_BY_TITLE,
    GET_GENRES_FOR_MOVIE,
    GET_DIRECTORS_FOR_MOVIE,
    GET_WRITERS_FOR_MOVIE
)
from keyboards.movie_search_keyboard import build_movie_search_results
from keyboards.favorite_keyboard import build_add_button, build_remove_button

router = Router()

user_state = {}  # {user_id: {'results': [...]}}


@router.message(lambda message: message.text == "🔍 Поиск по названию")
async def ask_for_title(message: types.Message):
    await message.answer("Введите название фильма или сериала:")


@router.message()
async def search_by_title(message: types.Message):
    query = message.text.strip()
    user_id = message.from_user.id

    with get_movies_connection() as conn:
        cur = conn.cursor()
        print(f"🔍 Выполняется поиск по '{query}'")

        try:
            cur.execute(SEARCH_MOVIE_BY_TITLE(query))
            results = cur.fetchall()
        except sqlite3.OperationalError as e:
            print(f"❌ Ошибка SQL: {e}")
            await message.answer("Ошибка в структуре базы данных")
            return

    if not results:
        await message.answer("Фильмы не найдены")
        return

    user_state[user_id] = {"results": results}
    markup = build_movie_search_results(results)
    await message.answer("Выберите фильм:", reply_markup=markup)


@router.callback_query(lambda call: call.data.startswith("movie_details_"))
async def show_full_movie_details(call: CallbackQuery):
    movie_id = call.data.split("_")[2]
    user_id = call.from_user.id

    result = next((r for r in user_state.get(user_id, {}).get("results", []) if r[0] == movie_id), None)

    if not result:
        await call.answer("Ошибка: фильм не найден", show_alert=True)
        return

    tconst, title, title_type, year_start, year_end, rating, votes, runtime = result
    year = f"{year_start}" + (f"–{year_end}" if year_end else "")

    with get_movies_connection() as conn:
        cur = conn.cursor()

        # Жанры
        cur.execute(GET_GENRES_FOR_MOVIE, (tconst,))
        genres = [g[0] for g in cur.fetchall()]

        # Режиссёры
        cur.execute(GET_DIRECTORS_FOR_MOVIE, (tconst,))
        directors = [d[0] for d in cur.fetchall()]

        # Сценаристы
        cur.execute(GET_WRITERS_FOR_MOVIE, (tconst,))
        writers = [w[0] for w in cur.fetchall()]

    # Проверяем, есть ли фильм в избранном
    is_favorite = False
    with get_favorites_connection() as fav_conn:
        fav_cur = fav_conn.cursor()
        fav_cur.execute("SELECT 1 FROM favorites WHERE user_id = ? AND movie_id = ?", (user_id, tconst))
        is_favorite = bool(fav_cur.fetchone())

    # Формируем текст
    type_mapping = {
        'movie': '🎬',
        'tvShow': '📺',
        'tvSeries': '📺',
        'tvMiniSeries': '🎞'
    }

    icon = type_mapping.get(title_type, '🎬')

    text = f"<b>{icon} Подробности</b>\n\n"
    text += f"🎥 Название: <b>{title}</b>\n"
    text += f"📅 Год: {year}\n"
    text += f"⭐ Рейтинг: {rating or 'нет'} ({votes or 'нет'})\n"

    if runtime:
        text += f"⏱ Продолжительность: {runtime} мин.\n"

    if genres:
        text += f"🎭 Жанры: {', '.join(genres)}\n"

    if directors:
        text += f"🎥 Режиссёры: {', '.join(directors[:5])}\n"

    if writers:
        text += f"✍️ Сценаристы: {', '.join(writers[:5])}\n"

    # Кнопка "Избранное"
    if is_favorite:
        markup = build_remove_button(tconst)
    else:
        markup = build_add_button(tconst)

    await call.message.edit_text(text, parse_mode="HTML", reply_markup=markup)
    await call.answer("Подробности загружены")