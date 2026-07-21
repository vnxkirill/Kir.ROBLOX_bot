"""Telegram-хендлеры раздела FNF: ссылки на GameJolt и пошаговые инструкции.

Каждая инструкция — альбом скриншотов (из записей экрана владельца)
с подписью-шагами. После первой отправки Telegram file_id кешируется
в памяти процесса, чтобы не загружать файлы заново.
"""

from dataclasses import dataclass
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


@dataclass(frozen=True)
class Guide:
    """Пошаговая инструкция: заголовок + (файл скриншота, текст шага)."""

    title: str
    steps: list[tuple[str, str]]
    footer: str = ""

    @property
    def caption(self) -> str:
        parts = [f"📖 <b>{self.title}</b>\n"]
        parts.extend(text for _, text in self.steps)
        if self.footer:
            parts.append(self.footer)
        return "\n\n".join(parts)


GUIDES: dict[str, Guide] = {
    "download": Guide(
        title="Как скачать FNF-мод",
        steps=[
            (
                "dl1_open_gamejolt.jpg",
                "1️⃣ Открой сайт <a href=\"https://gamejolt.com/c/fnf\">gamejolt.com/c/fnf</a> — "
                "это сообщество Friday Night Funkin'.",
            ),
            (
                "dl2_search.jpg",
                "2️⃣ В поиске сверху напиши название мода (например <i>fnf mod</i>) "
                "и выбери вкладку «Games».",
            ),
            (
                "dl3_mod_page.jpg",
                "3️⃣ Открой страницу понравившегося мода.",
            ),
            (
                "dl4_download_button.jpg",
                "4️⃣ Пролистай вниз до блока с версией и нажми кнопку <b>Download</b>.",
            ),
            (
                "dl5_downloading.jpg",
                "5️⃣ Начнётся загрузка — архив появится в папке «Загрузки».",
            ),
        ],
        footer="➡️ Дальше жми «📖 Как установить мод».",
    ),
    "install": Guide(
        title="Как установить FNF-мод",
        steps=[
            (
                "step1_extract.jpg",
                "1️⃣ Скачанный мод — это архив (.zip/.rar). "
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
        ],
        footer="⚠️ Скачивай моды только с проверенных сайтов (GameJolt, GameBanana).",
    ),
}

# Кеш Telegram file_id после первой загрузки: {имя файла: file_id}.
_file_id_cache: dict[str, str] = {}


class FnfCallback(CallbackData, prefix="fnf"):
    action: str


def _fnf_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📥 Как скачать мод", callback_data=FnfCallback(action="download"))
    builder.button(text="📖 Как установить мод", callback_data=FnfCallback(action="install"))
    builder.button(text="🌐 Открыть GameJolt FNF", url=_GAMEJOLT_FNF_URL)
    builder.button(text="🕹 Только игры и моды", url=_GAMEJOLT_FNF_GAMES_URL)
    builder.adjust(1)
    return builder.as_markup()


def _build_album(guide: Guide) -> list[InputMediaPhoto]:
    """Альбом из шагов; подпись — у первого фото (Telegram показывает её под альбомом)."""
    album: list[InputMediaPhoto] = []
    for index, (filename, _) in enumerate(guide.steps):
        media = _file_id_cache.get(filename) or FSInputFile(_ASSETS_DIR / filename)
        album.append(
            InputMediaPhoto(media=media, caption=guide.caption if index == 0 else None)
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


# Кнопки под инструкцией: со «скачать» ведём на «установить» и наоборот.
_NEXT_GUIDE: dict[str, tuple[str, str]] = {
    "download": ("📖 Как установить мод", "install"),
    "install": ("📥 Как скачать мод", "download"),
}


def _after_guide_keyboard(action: str) -> InlineKeyboardMarkup:
    text, next_action = _NEXT_GUIDE[action]
    builder = InlineKeyboardBuilder()
    builder.button(text=text, callback_data=FnfCallback(action=next_action))
    builder.button(text="🎵 Меню FNF", callback_data=FnfCallback(action="menu"))
    builder.adjust(1)
    return builder.as_markup()


@router.callback_query(FnfCallback.filter(F.action == "menu"))
async def back_to_fnf_menu(callback: CallbackQuery) -> None:
    await callback.message.answer(_FNF_TEXT, reply_markup=_fnf_keyboard())
    await callback.answer()


@router.callback_query(FnfCallback.filter(F.action.in_(set(GUIDES))))
async def show_guide(callback: CallbackQuery, callback_data: FnfCallback) -> None:
    guide = GUIDES[callback_data.action]
    sent = await callback.message.answer_media_group(media=_build_album(guide))
    # Запоминаем file_id, чтобы в следующий раз не загружать картинки заново.
    for msg, (filename, _) in zip(sent, guide.steps, strict=False):
        if msg.photo:
            _file_id_cache[filename] = msg.photo[-1].file_id
    # К альбому нельзя прикрепить кнопки — шлём их отдельным сообщением следом.
    await callback.message.answer(
        "Что дальше?", reply_markup=_after_guide_keyboard(callback_data.action)
    )
    await callback.answer()
