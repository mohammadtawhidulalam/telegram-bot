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

# ==============================
# 📊 USAGE STORAGE
# ==============================
usage_count = 0

# ==============================
# 🔧 CLEAN INPUT (÷ × FIX)
# ==============================
def clean_input(text):
    return (
        text.replace("÷", "/")
            .replace("×", "*")
            .replace("x", "*")
            .replace("X", "*")
            .replace("^", "**")
    )

# ==============================
# 🎯 FORMAT RESULT (DECIMAL FIX)
# ==============================
def format_result(value):
    if isinstance(value, float):
        value = round(value, 2)
        if value.is_integer():
            return str(int(value))
    return str(value)

# ==============================
# ⚡ INLINE CALCULATOR
# ==============================
async def inline_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    results = []

    if query:
        try:
            query_clean = clean_input(query)
            value = eval(query_clean)
            result = format_result(value)

            # OPTION 1 (result only)
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

# ==============================
# 🤖 START COMMAND
# ==============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 CalTaw Calculator Bot 🤖\n\n"
        "👉 Just type math like:\n"
        "2+2\n50*3\n100/5\n\n"
        "💡 Inline mode:\n"
        "@caltawbot 2+2\n\n"
        "📊 /stats → usage count\n"
        "🆘 /help → full guide\n\n"
        "👑 Owner: @mohammadtawhidulalam1"
    )

# ==============================
# 🆘 HELP COMMAND
# ==============================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🆘 Caltaw Bot Help Guide\n\n"
        "🧮 Calculator:\n"
        "➤ Just type math like:\n"
        "2+2\n50*3\n100/5\n\n"
        "📊 Usage:\n"
        "➤ /stats → See usage count\n\n"
        "💡 Inline Mode:\n"
        "@caltawbot 2+2\n\n"
        "👑 Owner: @mohammadtawhidulalam1\n\n"
        "⚙️ Works in group & private chat"
    )

# ==============================
# 📊 STATS COMMAND
# ==============================
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global usage_count
    await update.message.reply_text(f"📊 Total usage: {usage_count}")

# ==============================
# 💬 AUTO CALCULATOR
# ==============================
async def auto_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global usage_count

    if not update.message or not update.message.text:
        return

    text = update.message.text
    text = clean_input(text)

    try:
        value = eval(text)
        result = format_result(value)

        usage_count += 1

        await update.message.reply_text(result)

    except:
        pass

# ==============================
# 🚀 MAIN APP
# ==============================
app = ApplicationBuilder().token(TOKEN).build()

# handlers
app.add_handler(InlineQueryHandler(inline_calc))
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_calc))

print("Bot running...")
app.run_polling()
