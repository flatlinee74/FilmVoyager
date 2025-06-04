from aiogram import Router, types
from aiogram.types import CallbackQuery
from keyboards.newest_keyboard import build_newest_keyboard, fetch_newest_movies
from keyboards.main_menu import get_back_button
router = Router()

user_state = {}

@router.message(lambda message: message.text == "🆕 Новинки")
async def show_newest_movies_handler(message: types.Message):
    print("Получен запрос на новинки")  # Отладочный вывод
    user_id = message.from_user.id
    user_state[user_id] = {"offset": 0}

    movies = fetch_newest_movies(limit=20, offset=0)
    print(f"Получено фильмов: {len(movies) if movies else 0}")  # Отладочный вывод

    if not movies:
        await message.answer("Новинок пока нет")
        return

    text = "<b>🆕 Свежие новинки кинопроката</b>\n\n"
    for i, movie in enumerate(movies, start=1):
        title, year, rating = movie
        rating_str = f"⭐{rating:.1f}" if rating else "⭐нет"
        text += f"{i}. <b>{title}</b>\n   Год: {year}, Рейтинг: {rating_str}\n\n"

    markup = build_newest_keyboard(offset=0)
    await message.answer(text, reply_markup=markup, parse_mode="HTML")

@router.callback_query(lambda call: call.data.startswith("newest_"))
async def next_newest_page(call: CallbackQuery):
    user_id = call.from_user.id
    offset = int(call.data.split("_")[1])
    user_state[user_id] = {"offset": offset}

    movies = fetch_newest_movies(limit=20, offset=offset)

    if not movies:
        await call.answer("Больше нет фильмов")
        return

    text = f"<b>🎬 Свежие новинки (с {offset + 1} по {offset + len(movies)})</b>\n\n"
    for i, movie in enumerate(movies, start=1):
        title, year, rating = movie
        rating_str = f"⭐{rating:.1f}" if rating else "⭐нет"
        text += f"{i + offset}. <b>{title}</b>\n   Год: {year}, Рейтинг: {rating_str}\n\n"

    markup = build_newest_keyboard(offset=offset)
    await call.message.edit_text(text, reply_markup=markup, parse_mode="HTML",)
    await call.answer()