from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.main_menu import get_main_keyboard

router = Router()  # <-- Это главный объект, который мы экспортируем

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        """🎬 Добро пожаловать в FilmVoyager — твой гид в мире кино!

Теперь ты можешь выбрать, как хочешь искать идеальный фильм для вечера 🍿
Вот что я могу предложить:

    🔍 По жанрам — найдём фильмы под любое настроение
    🔤 По названию — получи подробную информацию о фильме или сериале
    🔥 Топ 100 — проверенные шедевры, которые смотрят все
    ⭐ Избранное — сохраняй любимые фильмы и возвращайся к ним снова
    🆕 Новинки — будь в курсе свежих релизов и трендов
    🎲 Случайный фильм — доверься судьбе и открой что-то новое

👉 Просто выбери, что тебя интересует, и наслаждайся просмотром!""",
        reply_markup=get_main_keyboard()
    )