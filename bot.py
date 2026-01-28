import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from core import get_bot_reply

# =========================
# KONFIGURASI
# =========================
TOKEN = "7980947582:AAH8HchtixODasiRJO_Dd9Epj-CvBkoH9OU"
WHATSAPP_URL = "https://wa.me/6287850670438"

# =========================
# LOGGING
# =========================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =========================
# TOMBOL WHATSAPP
# =========================
def whatsapp_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📱 Order via WhatsApp", url=WHATSAPP_URL)]
    ])

# =========================
# COMMAND /start
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🍞 *Family Bakery Assistant*\n\n"
        "Halo 👋 Selamat datang di Family Bakery.\n\n"
        "Silakan tanyakan:\n"
        "• Menu & produk\n"
        "• Jam operasional\n"
        "• Alamat toko\n"
        "• Cara pemesanan"
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=whatsapp_button()
    )

# =========================
# HANDLE PESAN USER
# =========================
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    reply = get_bot_reply(user_text)

    await update.message.reply_text(
        reply,
        reply_markup=whatsapp_button()
    )

# =========================
# MAIN
# =========================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    logger.info("🤖 Bot Family Bakery berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
