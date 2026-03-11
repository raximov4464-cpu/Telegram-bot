from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

from flask import Flask
import threading
import os

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = "@raximovganisher"

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Agar kanal nomidan yozilgan bo'lsa tekshirmaydi
    if update.message.sender_chat:
        return

    user_id = update.effective_user.id
    first_name = update.effective_user.first_name

    member = await context.bot.get_chat_member(CHANNEL, user_id)

    if member.status not in ["member", "administrator", "creator"]:

        mention = f'<a href="tg://user?id={user_id}">{first_name}</a>'

        await update.message.reply_text(
            f"❌ {mention} kommentariya yozish uchun kanalga a'zo bo'ling!",
            parse_mode="HTML"
        )

        await update.message.delete()


# -------- TELEGRAM BOT --------
app_bot = ApplicationBuilder().token(TOKEN).build()
app_bot.add_handler(MessageHandler(filters.TEXT, check))


# -------- WEB SERVER (Render uchun) --------
web = Flask(__name__)

@web.route("/")
def home():
    return "Bot ishlayapti"


def run_bot():
    app_bot.run_polling()


if __name__ == "__main__":

    # Botni alohida thread da ishga tushiramiz
    t = threading.Thread(target=run_bot)
    t.start()

    # Render uchun port ochamiz
    port = int(os.environ.get("PORT", 10000))
    web.run(host="0.0.0.0", port=port)
