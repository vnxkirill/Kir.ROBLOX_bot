"""Telegram-хендлеры раздела FNF: ссылки на GameJolt и инструкция по установке модов.

Инструкция — альбом скриншотов (из записи экрана владельца) с подписями шагов.
После первой отправки Telegram file_id кешируется в памяти процесса,
чтобы не загружать файлы заново.
"""

from pathlib import Path

from aiogram import F, Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.keyboards import MainMenuButton
from app.keyboards.main_menu import MainMenuAction, MainMenuCallback

router = Router(name="fnf")

_FNF_TEXT = (
    "🎵 <b>FNF Mods</b>\n\n"
    "Моды Friday Night Funkin' живут на GameJolt — жми кнопку:"
)

_GAMEJOLT_FNF_URL = "https://gamejolt.com/c/fnf"
_GAMEJOLT_FNF_GAMES_URL = "https://gamejolt.com/c/fnf/games"

_ASSETS_DIR = Path(__file__).parent / "assets"

# Шаги инструкции: (файл, подпись). Подпись показывается под альбомом.
_GUIDE_STEPS: list[tuple[str, str]] = [
    (
        "step1_extract.jpg",
        "1️⃣ Скачай мод с GameJolt — получится архив (.zip/.rar). "
        "Кликни по нему правой кнопкой → «Извлечь всё…»",
    ),
    (
        "step2_wait.jpg",
        "2️⃣ Дождись, пока файлы распакуются (зелёная полоса дойдёт до конца).",
    ),
    (
        "step3_run_exe.jpg",
        "3️⃣ Открой распакованную папку и запусти файл с типом «Приложение» (.exe).",
    ),
    (
        "step4_play.jpg",
        "4️⃣ Готово! Мод запустится — жми Enter и играй. 🎤",
    ),
]

_GUIDE_CAPTION = (
    "📖 <b>Как установить FNF-мод</b>\n\n"
    + "\n\n".join(caption for _, caption in _GUIDE_STEPS)
    + "\n\n⚠️ Скачивай моды только с проверенных сайтов (GameJolt, GameBanana)."
)

# Кеш Telegram file_id после первой загрузки: {имя файла: file_id}.
_file_id_cache: dict[str, str] = {}


class FnfCallback(CallbackData, prefix="fnf"):
    action: str


def _fnf_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📖 Инструкция", callback_data=FnfCallback(action="guide"))
    builder.button(text="🌐 Открыть GameJolt FNF", url=_GAMEJOLT_FNF_URL)
    builder.button(text="🕹 Только игры и моды", url=_GAMEJOLT_FNF_GAMES_URL)
    builder.adjust(1)
    return builder.as_markup()


def _build_album() -> list[InputMediaPhoto]:
    """Альбом из шагов; подпись — у первого фото (Telegram показывает её под альбомом)."""
    album: list[InputMediaPhoto] = []
    for index, (filename, _) in enumerate(_GUIDE_STEPS):
        media = _file_id_cache.get(filename) or FSInputFile(_ASSETS_DIR / filename)
        album.append(
            InputMediaPhoto(media=media, caption=_GUIDE_CAPTION if index == 0 else None)
        )
    return album


@router.message(F.text == MainMenuButton.FNF)
async def fnf_menu_message(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(_FNF_TEXT, reply_markup=_fnf_keyboard())


@router.callback_query(MainMenuCallback.filter(F.action == MainMenuAction.FNF))
async def fnf_menu_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(_FNF_TEXT, reply_markup=_fnf_keyboard())
    await callback.answer()


@router.callback_query(FnfCallback.filter(F.action == "guide"))
async def show_guide(callback: CallbackQuery) -> None:
    sent = await callback.message.answer_media_group(media=_build_album())
    # Запоминаем file_id, чтобы в следующий раз не загружать картинки заново.
    for msg, (filename, _) in zip(sent, _GUIDE_STEPS, strict=False):
        if msg.photo:
            _file_id_cache[filename] = msg.photo[-1].file_id
    await callback.answer()
