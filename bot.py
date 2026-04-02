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
# FORMAT RESULT (FIX FLOAT)
# =========================
def format_result(value):
    if isinstance(value, float):
        value = round(value, 2)
        if value.is_integer():
            return str(int(value))
        return str(value)
    return str(value)

# =========================
# INLINE CALCULATOR (2 OPTION + IMAGE)
# =========================
async def inline_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    results = []

    if query:
        try:
            value = eval(query)
            result = format_result(value)

            # OPTION 1 (clean result)
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title=f"{query}",
                    description=f"{result}",
                    thumbnail_url="https://cdn-icons-png.flaticon.com/512/2921/2921222.png",
                    input_message_content=InputTextMessageContent(
                        f"{result}"
                    ),
                )
            )

            # OPTION 2 (full text)
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title="Full text",
                    description=f"{query} = {result}",
                    thumbnail_url="https://cdn-icons-png.flaticon.com/512/2921/2921222.png",
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

        "💡 Inline usage:\n"
        "`@caltawbot 2+2`\n\n"

        "👆 Tap & hold to copy\n\n"

        "👑 Owner: @mohammadtawhidulalam1",
        parse_mode="Markdown"
    )
# =========================
# HELP COMMAND
# =========================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📘 Help Menu\n\n"
        "🧮 Calculator:\n"
        "Type any math → 2+2, 10*5\n\n"
        "⚡ Inline Mode:\n"
        "@caltawbot 2+2\n\n"
        "👥 Group:\n"
        "Auto reply works\n\n"
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
