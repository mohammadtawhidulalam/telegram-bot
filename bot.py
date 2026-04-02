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
# FORMAT RESULT (FIX FLOAT ISSUE)
# =========================
def format_result(value):
    if isinstance(value, float):
        value = round(value, 2)
        if value.is_integer():
            return str(int(value))
        return str(value)
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
                        f"{query} = {result}"
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
        "🤖 CalTaw Bot Ready!\n\n"
        "👉 Type math like:\n"
        "2+2, 10*5, 100/4\n\n"
        "⚡ Inline: @caltawbot 2+2"
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
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_calc))

app.run_polling()
