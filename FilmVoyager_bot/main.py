# main.py

from aiogram import Bot, Dispatcher
from aiogram.types import Message
import asyncio

# Импортируем роутеры из каждого handler'а
from handlers.start import router as start_router
from handlers.random_film import router as random_router
from handlers.favorites import router as favorites_router
from handlers.top_100 import router as top_100_router
from handlers.by_genre import router as by_genre_router
from handlers.newest import router as newest_router
from handlers.search_title import router as search_title_router
from handlers.top_series import router as top_series_router
from handlers.back_handler import router as back_router

# Токен бота
BOT_TOKEN = '7760505246:AAEjy5RUyjhnNhPWDAnW6VEDyvcsoxQ2uvQ'

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # === Регистрация роутеров ===
    dp.include_router(start_router)
    dp.include_router(by_genre_router)
    dp.include_router(newest_router)
    dp.include_router(random_router)
    dp.include_router(top_100_router)
    dp.include_router(top_series_router)
    dp.include_router(back_router)
    dp.include_router(favorites_router)
    dp.include_router(search_title_router) 

    print("Бот запущен...")
    await dp.start_polling(bot) 

if __name__ == "__main__":
    asyncio.run(main())