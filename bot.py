from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

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

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, check))

app.run_polling()