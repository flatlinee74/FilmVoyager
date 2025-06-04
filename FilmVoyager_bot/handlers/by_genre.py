# handlers/by_genre.py

from aiogram import Router, types
from aiogram.types import CallbackQuery
from database.db import get_movies_connection
from keyboards.genre_keyboard import build_genre_keyboard, fetch_all_genres, fetch_movies_by_genre_ids

router = Router()

# Хранение состояния пользователя
user_state = {}  # {user_id: {'genre_ids': [...], 'offset': ...}}


@router.message(lambda message: message.text == "🎭 По жанрам")
async def select_multiple_genres(message: types.Message):
    genres = fetch_all_genres()
    
    if not genres:
        await message.answer("Жанры не найдены в базе данных.")
        return

    user_state[message.from_user.id] = {"genre_ids": [], "offset": 0}

    markup = build_genre_keyboard(genres)
    await message.answer("Выберите один или несколько жанров:", reply_markup=markup)


@router.callback_query(lambda call: call.data.startswith("select_genre_"))
async def toggle_genre(call: CallbackQuery):
    genre_id = int(call.data.split("_")[2])
    user_id = call.from_user.id
    state = user_state.get(user_id, {"genre_ids": [], "offset": 0})
    genre_ids = state["genre_ids"]

    if genre_id in genre_ids:
        genre_ids.remove(genre_id)
    else:
        genre_ids.append(genre_id)

    state["genre_ids"] = genre_ids
    user_state[user_id] = state

    all_genres = fetch_all_genres()
    markup = build_genre_keyboard(all_genres, selected_ids=genre_ids)
    await call.message.edit_reply_markup(reply_markup=markup)

    genre_name = next((g['name'] for g in all_genres if g['id'] == genre_id), None)
    await call.answer(f"{'Добавлен' if genre_id in genre_ids else 'Убран'} жанр: {genre_name}")
    
@router.callback_query(lambda call: call.data == "show_movies_by_genres")
async def show_movies_by_selected_genres(call: CallbackQuery):
    user_id = call.from_user.id
    state = user_state.get(user_id)

    if not state or not state["genre_ids"]:
        await call.answer("Выберите хотя бы один жанр", show_alert=True)
        return

    state["offset"] = 0
    user_state[user_id] = state

    result = fetch_movies_by_genre_ids(state["genre_ids"], offset=state["offset"])
    movies = result["movies"]
    total = result["total"]

    if not movies:
        await call.message.answer("Нет фильмов для выбранных условий (numVotes >= 50000)")
        return

    genre_names = [g['name'] for g in fetch_all_genres() if g['id'] in state["genre_ids"]]
    text = f"<b>🎬 Лучшие фильмы по жанрам:</b> {', '.join(genre_names)}\n\n"

    for i, movie in enumerate(movies, start=1):
        title, year, rating = movie
        text += f"{i}. <b>{title}</b>\n   Год: {year}, Рейтинг: ⭐{rating}\n\n"

    kb = [[types.InlineKeyboardButton(text="➡️ Следующие 20", callback_data="next_multi_genre_page")]]
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)

    await call.message.edit_text(text, parse_mode="HTML", reply_markup=markup)
    await call.answer()


@router.callback_query(lambda call: call.data == "next_multi_genre_page")
async def next_multi_genre_page(call: CallbackQuery):
    user_id = call.from_user.id
    state = user_state.get(user_id)

    if not state or not state["genre_ids"]:
        await call.answer("Ошибка: данные о жанрах не найдены")
        return

    state["offset"] += 20
    user_state[user_id] = state

    result = fetch_movies_by_genre_ids(state["genre_ids"], offset=state["offset"])
    movies = result["movies"]
    total = result["total"]

    if not movies:
        await call.answer("Больше нет фильмов")
        return

    genre_names = [g['name'] for g in fetch_all_genres() if g['id'] in state["genre_ids"]]
    text = f"<b>🎬 Фильмы по жанрам:</b> {', '.join(genre_names)} (продолжение)\n\n"

    for i, movie in enumerate(movies, start=1):
        title, year, rating = movie
        text += f"{i + state['offset']}. <b>{title}</b>\n   Год: {year}, Рейтинг: ⭐{rating}\n\n"

    kb = [
        [types.InlineKeyboardButton(text="⬅️ Предыдущие 20", callback_data="prev_multi_genre_page"),
         types.InlineKeyboardButton(text="➡️ Следующие 20", callback_data="next_multi_genre_page")]
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)

    await call.message.edit_text(text, parse_mode="HTML", reply_markup=markup)
    await call.answer()


@router.callback_query(lambda call: call.data == "prev_multi_genre_page")
async def prev_multi_genre_page(call: CallbackQuery):
    user_id = call.from_user.id
    state = user_state.get(user_id)

    if not state or not state["genre_ids"]:
        await call.answer("Ошибка: данные о жанрах не найдены")
        return

    if state["offset"] >= 20:
        state["offset"] -= 20
    user_state[user_id] = state

    result = fetch_movies_by_genre_ids(state["genre_ids"], offset=state["offset"])
    movies = result["movies"]

    if not movies:
        await call.answer("Фильмы не найдены")
        return

    genre_names = [g['name'] for g in fetch_all_genres() if g['id'] in state["genre_ids"]]
    text = f"<b>🎬 Лучшие фильмы по жанрам:</b> {', '.join(genre_names)}\n\n"

    for i, movie in enumerate(movies, start=1):
        title, year, rating = movie
        text += f"{i + state['offset']}. <b>{title}</b>\n   Год: {year}, Рейтинг: ⭐{rating}\n\n"

    kb = [
        [types.InlineKeyboardButton(text="⬅️ Предыдущие 20", callback_data="prev_multi_genre_page"),
         types.InlineKeyboardButton(text="➡️ Следующие 20", callback_data="next_multi_genre_page")]
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)

    await call.message.edit_text(text, parse_mode="HTML", reply_markup=markup)
    await call.answer()