# keyboards/movie_search_keyboard.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

type_icons = {
    'movie': '🎬',
    'tvShow': '📺',
    'tvSeries': '📺',
    'tvMiniSeries': '🎞',
    'short': '📽',
    'videoGame': '🎮'
}

def build_movie_search_results(results):
    keyboard = []
    for r in results:
        # Правильно распаковываем 8 значений
        tconst, en_title, title_type, year_start, year_end, rating, votes, runtime = r
        
        icon = type_icons.get(title_type, '🎬')
        year = f"{year_start}" + (f"–{year_end}" if year_end else "")
        btn_text = f"{en_title} ({year}) ⭐{rating or '?'} ({votes})"
        
        keyboard.append([InlineKeyboardButton(
            text=f"{icon} {btn_text}",
            callback_data=f"movie_details_{tconst}"
        )])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)