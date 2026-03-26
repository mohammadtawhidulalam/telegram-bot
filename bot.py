from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (
    ApplicationBuilder,
    InlineQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CommandHandler,
)
import uuid
import os

TOKEN = os.getenv("BOT_TOKEN")

# ================== INLINE CALCULATOR ==================
async def inline_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    results = []

    if query:
        try:
            result = str(eval(query))

            results.append(
                InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title=f"{query} = {result}",
                    input_message_content=InputTextMessageContent(
                        f"{query} = {result}"
                    ),
                )
            )
        except:
            pass

    await update.inline_query.answer(results, cache_time=1)


# ================== START COMMAND ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Welcome to Caltaw Bot!\n\n"
        "➤ Just type math like:\n"
        "2+2\n50*3\n100/5\n\n"
        "📌 Works in group & private chat\n"
        "💡 Inline: @caltawbot 2+2"
    )


# ================== HELP COMMAND ==================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🆘 Help Menu\n\n"
        "➤ Use this bot as calculator\n\n"
        "📌 Examples:\n"
        "2+2\n10*5\n100/4\n\n"
        "📌 Group e directly likhle auto reply dibe\n"
        "📌 Inline use:\n"
        "@caltawbot 2+2"
    )


# ================== AUTO REPLY CALCULATOR ==================
async def auto_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text

    try:
        result = str(eval(text))
        await update.message.reply_text(result)
    except:
        pass


# ================== MAIN APP ==================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(InlineQueryHandler(inline_calc))
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_calc))

print("Bot is running...")
app.run_polling()
