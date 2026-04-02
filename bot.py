from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (
    ApplicationBuilder,
    InlineQueryHandler,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters,
)
import uuid
import os

TOKEN = os.getenv("BOT_TOKEN")

# =========================
# FORMAT FUNCTION (IMPORTANT FIX)
# =========================
def format_result(value):
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        else:
            return f"{value:.2f}"
    return str(value)

# =========================
# INLINE CALCULATOR
# =========================
async def inline_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    results = []

    if query:
        try:
            value = eval(query)
            result = format_result(value)

            results.append(
                InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title=f"{query} = {result}",
                    input_message_content=InputTextMessageContent(
                        f"{query} = {result}\n— CalTaw Bot"
                    ),
                )
            )
        except:
            pass

    await update.inline_query.answer(results, cache_time=1)


# =========================
# START COMMAND
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Welcome to CalTaw Bot!\n\n"
        "👉 Just type math like:\n"
        "2+2 or 10*5 or 100/4\n\n"
        "⚡ Works in group & private\n"
        "💡 Inline: @caltawbot 2+2\n\n"
        "👑 Owner: @mohammadtawhidulalam1"
    )


# =========================
# HELP COMMAND
# =========================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📘 Help Menu\n\n"
        "🧮 Calculator:\n"
        "Type any math → 2+2, 10*5, 50/2\n\n"
        "⚡ Inline Mode:\n"
        "@caltawbot 2+2\n\n"
        "👥 Group:\n"
        "Bot auto reply দিব math দেখলে\n\n"
        "🛠 Features:\n"
        "✔ Inline Calculator\n"
        "✔ Auto Reply Calculator\n\n"
        "👑 Owner: @mohammadtawhidulalam1"
    )


# =========================
# AUTO REPLY CALCULATOR
# =========================
async def auto_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text

    try:
        value = eval(text)
        result = format_result(value)
        await update.message.reply_text(result)
    except:
        pass


# =========================
# MAIN APP
# =========================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(InlineQueryHandler(inline_calc))
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_calc))

app.run_polling()
