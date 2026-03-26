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

# 📊 User usage tracking
user_usage = {}

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


# ================== START ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Welcome to Caltaw Bot!\n\n"
        "➤ Just type math like:\n"
        "2+2\n50*3\n100/5\n\n"
        "📊 Use /stats to see usage\n"
        "📌 Works in group & private\n"
        "💡 Inline: @caltawbot 2+2"
    )


# ================== HELP ==================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🆘 Help Menu\n\n"
        "➤ Calculator use:\n"
        "2+2\n10*5\n100/4\n\n"
        "📊 /stats → usage count\n"
        "🚫 Links are blocked in group\n"
        "💡 Inline: @caltawbot 2+2"
    )


# ================== STATS ==================
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    count = user_usage.get(user_id, 0)

    await update.message.reply_text(f"📊 You used bot {count} times")


# ================== AUTO REPLY + PROTECTION ==================
async def auto_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.lower()
    user_id = update.message.from_user.id

    # 🚫 Block links
    if "http" in text or "t.me" in text:
        try:
            await update.message.delete()
            await update.message.reply_text("🚫 Links not allowed!")
        except:
            pass
        return

    # 🧮 Calculator
    try:
        result = str(eval(text))

        user_usage[user_id] = user_usage.get(user_id, 0) + 1

        await update.message.reply_text(
            f"{result}\n\n📊 Uses: {user_usage[user_id]}"
        )
    except:
        pass


# ================== MAIN ==================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(InlineQueryHandler(inline_calc))
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_calc))

print("Bot is running...")
app.run_polling()
