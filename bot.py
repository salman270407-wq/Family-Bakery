import logging
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)

from core import get_bot_reply

# =============================
# LOGGING
# =============================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

# =============================
# ENVIRONMENT VARIABLES
# =============================
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    print("❌ TELEGRAM_BOT_TOKEN belum diset")
    exit()

# =============================
# MEMORY SINGKAT PER CHAT
# =============================
conversation_history = {}  # {chat_id: [{"user": msg, "bot": msg}, ...]}

# =============================
# COMMAND /START
# =============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    conversation_history[chat_id] = []  # reset history
    await update.message.reply_text(
        "Halo 👋 Selamat datang di *Family Bakery* 🥐🍞\n"
        "Silakan ketik pertanyaan atau langsung pesan produk kami 😊"
    )

# =============================
# HANDLE PESAN USER
# =============================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_text = update.message.text

    if chat_id not in conversation_history:
        conversation_history[chat_id] = []

    # Jawaban dari core.py
    reply = get_bot_reply(user_text)

    # Simpan history
    conversation_history[chat_id].append({
        "user": user_text,
        "bot": reply
    })

    await update.message.reply_text(reply)

# =============================
# MAIN PROGRAM
# =============================
if __name__ == '__main__':
    print("🤖 Bot Family Bakery sedang dijalankan...")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    app.run_polling()
