# handlers/top_series.py

from aiogram import Router, types
from database.db import get_movies_connection
from database.queries import GET_TOP_100_SERIES
router = Router()

@router.message(lambda message: message.text == "📺 Топ-100 сериалов")
async def show_top_50_series(message: types.Message):
    print("Получен запрос на вывод топ-100 сериалов")

    with get_movies_connection() as conn:
        cur = conn.cursor()
        cur.execute(GET_TOP_100_SERIES)
        series_list = cur.fetchall()

    if not series_list:
        await message.answer("Сериалы не найдены в базе данных.")
        return

    text = "<b>📺 Топ-100 сериалов по рейтингу:</b>\n\n"
    for i, serie in enumerate(series_list, start=1):
        title, year, rating = serie
        text += f"{i}. <b>{title}</b>\n   Год: {year}, Рейтинг: ⭐{rating}\n\n"

    # Telegram позволяет до 4096 символов за раз
    max_length = 4096
    messages_text = [text[i:i + max_length] for i in range(0, len(text), max_length)]

    for msg in messages_text:
        await message.answer(msg, parse_mode="HTML")