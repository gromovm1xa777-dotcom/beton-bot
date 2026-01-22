import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder


BOT_TOKEN = os.getenv("BOT_TOKEN")

# ВАЖНО: ссылки в кавычках и без пробелов
MINEPLAY_URL = "https://click.mytraffgun.com/click?pid=1910&offer_id=455"
ICEFISH_URL  = "https://click.mytraffgun.com/click?pid=1910&offer_id=455"


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def main_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="⛏️ MINEPLAY", callback_data="section_1")
    kb.button(text="🎣 ICEFISH", callback_data="section_2")
    kb.adjust(2)
    return kb.as_markup()


def play_menu(url: str):
    url = (url or "").strip()  # убираем пробелы/переносы
    kb = InlineKeyboardBuilder()
    kb.button(text="▶️ ГРАТИ", url=url)          # <-- НАДЁЖНО: это url-кнопка
    kb.button(text="⬅️ Назад", callback_data="back")
    kb.adjust(1)
    return kb.as_markup()


@dp.message(F.text.startswith("/start"))
async def start(message: Message):
    await message.answer(
        "Привіт 👋\n\n"
        "Ти потрапив до приватного простору з інтерактивними можливостями.\n"
        "Тут доступні різні розділи — обери той, який цікавить саме тебе 👇",
        reply_markup=main_menu()
    )


@dp.callback_query(F.data == "section_1")
async def section_1(call: CallbackQuery):
    await call.message.edit_text(
        "⛏️ MINEPLAY\n\n"
        "Натисни кнопку нижче, щоб продовжити 👇",
        reply_markup=play_menu(MINEPLAY_URL)
    )
    await call.answer()


@dp.callback_query(F.data == "section_2")
async def section_2(call: CallbackQuery):
    await call.message.edit_text(
        "🎣 ICEFISH\n\n"
        "Натисни кнопку нижче, щоб продовжити 👇",
        reply_markup=play_menu(ICEFISH_URL)
    )
    await call.answer()


@dp.callback_query(F.data == "back")
async def back(call: CallbackQuery):
    await call.message.edit_text(
        "⬇️ Обери розділ нижче",
        reply_markup=main_menu()
    )
    await call.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
