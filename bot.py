"""
Central Asia Power Solutions — Telegram Bot
"""

import logging
import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ── Config ──────────────────────────────────────────────────────────────────
BOT_TOKEN  = os.environ["BOT_TOKEN"]
WEBAPP_URL = "https://caps-partners.netlify.app/"   # host the webapp folder

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ── Translations ─────────────────────────────────────────────────────────────
TEXTS = {
    "uz": {
        "greeting": (
            "👋 Assalomu alaykum!\n\n"
            "Central Asia Power Solutions botiga xush kelibsiz.\n\n"
            "Iltimos, tilni tanlang:"
        ),
        "about_title": "🏢 Biz haqimizda",
        "about": (
            "Central Asia Power Solutions MChJ [CAPS] — issiqlik utilizatsiya bug' "
            "generatorlari (HRSG) va qozonlar uchun barcha OEM ishlab chiqaruvchilarning "
            "after-market xizmatlari va ehtiyot qismlari bo'yicha to'liq yechimlar "
            "yetkazib beruvchi sifatida tashkil etilgan.\n\n"
            "Biz eng yuqori sifatli original ehtiyot qismlar, xizmatlar va modernizatsiya "
            "yechimlarini taklif etib, HTPS Technical Service jamoasining tengsiz tajribasi "
            "va professional qo'llab-quvvatlashi bilan HRSG qurilmalarini eng tejamkor "
            "tarzda saqlash va boshqarishga yordam beramiz — tejamkorlik, samaradorlik "
            "va unumdorlikni maksimal darajada oshirib.\n\n"
            "🌐 ca-ps.uz"
        ),
        "partners_btn": "🤝 Hamkorlarimiz",
        "website_btn":  "🌐 Veb-sayt",
        "lang_set":     "✅ Til o'rnatildi: O'zbekcha",
    },
    "ru": {
        "greeting": (
            "👋 Добро пожаловать!\n\n"
            "Это официальный бот Central Asia Power Solutions.\n\n"
            "Пожалуйста, выберите язык:"
        ),
        "about_title": "🏢 О компании",
        "about": (
            "ООО Central Asia Power Solutions [CAPS] создана как поставщик комплексных "
            "решений в области послепродажного обслуживания и поставки запасных частей "
            "для котлов-утилизаторов (HRSG) и котлов всех OEM-производителей.\n\n"
            "Предлагая оригинальные запчасти, услуги и решения по модернизации высочайшего "
            "качества — при поддержке команды HTPS Technical Service — мы обеспечиваем "
            "максимально экономичную эксплуатацию ваших HRSG-установок, повышая "
            "производительность и эффективность.\n\n"
            "🌐 ca-ps.uz"
        ),
        "partners_btn": "🤝 Наши партнёры",
        "website_btn":  "🌐 Веб-сайт",
        "lang_set":     "✅ Язык установлен: Русский",
    },
    "en": {
        "greeting": (
            "👋 Welcome!\n\n"
            "This is the official bot of Central Asia Power Solutions.\n\n"
            "Please choose your language:"
        ),
        "about_title": "🏢 About Us",
        "about": (
            "Central Asia Power Solutions LLC [CAPS] is established as a total solution "
            "provider for all after-market services and parts related to Heat Recovery "
            "Steam Generators (HRSG) and boilers for any OEM manufacturer.\n\n"
            "By offering genuine parts, services, and upgrading solutions of the highest "
            "quality — backed by the unparalleled expertise of the HTPS Technical Service "
            "team — we deliver the most efficient solutions to maintain and operate your "
            "HRSG units in the most cost-effective way, maximising savings, performance, "
            "and efficiency.\n\n"
            "🌐 ca-ps.uz"
        ),
        "partners_btn": "🤝 Our Partners",
        "website_btn":  "🌐 Website",
        "lang_set":     "✅ Language set: English",
    },
}

# ── Keyboards ─────────────────────────────────────────────────────────────────
def lang_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇺🇿 O'zbek",  callback_data="lang_uz"),
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        ]
    ])


def main_keyboard(lang: str) -> InlineKeyboardMarkup:
    t = TEXTS[lang]
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                t["partners_btn"],
                web_app=WebAppInfo(url=WEBAPP_URL),
            )
        ],
        [
            InlineKeyboardButton(
                t["website_btn"],
                url="https://ca-ps.uz",
            )
        ],
    ])

# ── Handlers ──────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        TEXTS["en"]["greeting"],          # neutral until lang chosen
        reply_markup=lang_keyboard(),
    )


async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    lang = query.data.split("_")[1]       # lang_uz → uz
    context.user_data["lang"] = lang
    t = TEXTS[lang]

    # Acknowledge language selection
    await query.edit_message_text(
        t["lang_set"],
    )

    # Send About Us
    await query.message.reply_text(
        f"{t['about_title']}\n\n{t['about']}",
        reply_markup=main_keyboard(lang),
        disable_web_page_preview=True,
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Exception:", exc_info=context.error)

# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        CallbackQueryHandler(language_callback, pattern=r"^lang_")
    )
    app.add_error_handler(error_handler)

    logger.info("CAPS Bot running…")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
