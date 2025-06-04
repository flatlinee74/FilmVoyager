from aiogram import Router, types
from keyboards.main_menu import get_main_keyboard

router = Router()

@router.message(lambda message: message.text == "⬅️ Назад")
async def go_back(message: types.Message):
    await message.answer("Вы вернулись в главное меню:", reply_markup=get_main_keyboard())