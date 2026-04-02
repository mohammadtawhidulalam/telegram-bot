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

# 📊 GLOBAL USAGE COUNTER
usage_count = 0


# 🔢 RESULT FORMAT (decimal fix)
def format_result(value):
    if isinstance(value, float):
        value = round(value, 2)
        if value.is_integer():
            return str(int(value))
    return str(value)


# ⚡ INLINE CALCULATOR
async def inline_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global usage_count
    query = update.inline_query.query
    results = []

    if query:
        try:
            value = eval(query)
            result = format_result(value)
            usage_count += 1

            # OPTION 1 (clean)
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title=f"{query}",
                    description=f"{result}",
                    thumbnail_url="https://cdn-icons-png.flaticon.com/512/2921/2921222.png",
                    input_message_content=InputTextMessageContent(f"{result}"),
                )
            )

            # OPTION 2 (full)
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


# 🤖 START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 CalTaw Calculator Bot 🤖\n\n"
        "👉 Just type math like:\n"
        "2+2\n"
        "50*3\n"
        "100/5\n\n"
        "💡 Inline mode:\n"
        "@caltawbot 2+2\n\n"
        "📊 /stats → usage count\n"
        "🆘 /help → full guide\n\n"
        "👑 Owner: @mohammadtawhidulalam1"
    )


# 🆘 HELP COMMAND
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🆘 Caltaw Bot Help Guide\n\n"
        "🧮 Calculator:\n"
        "➤ Just type math like:\n"
        "2+2\n50*3\n100/5\n\n"
        "📊 /stats → See usage count\n\n"
        "💡 Inline Mode:\n"
        "@caltawbot 2+2\n\n"
        "⚙️ Works in group & private chat\n\n"
        "👑 Owner: @mohammadtawhidulalam1"
    )


# 📊 STATS COMMAND
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global usage_count
    await update.message.reply_text(
        f"📊 Total calculations used:\n{usage_count}"
    )


# 🤖 AUTO REPLY CALCULATOR
async def auto_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global usage_count

    if not update.message or not update.message.text:
        return

    text = update.message.text

    try:
        value = eval(text)
        result = format_result(value)
        usage_count += 1
        await update.message.reply_text(result)
    except:
        pass


# 🚀 APP START
app = ApplicationBuilder().token(TOKEN).build()

# handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(InlineQueryHandler(inline_calc))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_calc))

print("Bot running...")
app.run_polling()
