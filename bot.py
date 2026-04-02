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

# 📊 User tracking
user_usage = {}

# ⚙️ Group settings
group_settings = {}

# ================== INLINE ==================
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
                        f"{query} = {result}\n— Caltaw Bot"
                    )
                )
            )
        except:
            pass

    await update.inline_query.answer(results)


# ================== START ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Welcome to Caltaw Bot!\n\n"
        "➤ Type math like:\n"
        "2+2\n50*3\n100/5\n\n"
        "📊 /stats → usage count\n"
        "🆘 /help → full guide\n\n"
        "👑 Owner: @mohammadtawhidulalam1"
    )


# ================== HELP ==================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🆘 Caltaw Bot Help Guide\n\n"

        "🧮 Calculator:\n"
        "➤ Just type math like:\n"
        "2+2\n50*3\n100/5\n\n"

        "📊 Usage:\n"
        "➤ /stats → See usage count\n\n"

        "🔗 Link Control (Group only):\n"
        "➤ /link on → Enable link block\n"
        "➤ /link off → Disable link block\n\n"

        "🚫 Spam Control (Group only):\n"
        "➤ /spam on → Enable spam block\n"
        "➤ /spam off → Disable spam block\n\n"

        "💡 Inline Mode:\n"
        "@caltawbot 2+2\n\n"

        "👑 Owner: @mohammadtawhidulalam1\n\n"

        "⚙️ Notes:\n"
        "Bot must be admin for protection\n"
        "Works in group & private chat\n\n"

        "🔥 Enjoy using Caltaw Bot!"
    )


# ================== STATS ==================
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    count = user_usage.get(user_id, 0)
    await update.message.reply_text(f"📊 You used bot {count} times")


# ================== LINK CONTROL ==================
async def link_control(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if chat_id not in group_settings:
        group_settings[chat_id] = {"link": False, "spam": False}

    if context.args and context.args[0] == "on":
        group_settings[chat_id]["link"] = True
        await update.message.reply_text("✅ Link block ON")
    elif context.args and context.args[0] == "off":
        group_settings[chat_id]["link"] = False
        await update.message.reply_text("❌ Link block OFF")
    else:
        await update.message.reply_text("Use: /link on or /link off")


# ================== SPAM CONTROL ==================
async def spam_control(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if chat_id not in group_settings:
        group_settings[chat_id] = {"link": False, "spam": False}

    if context.args and context.args[0] == "on":
        group_settings[chat_id]["spam"] = True
        await update.message.reply_text("✅ Spam block ON")
    elif context.args and context.args[0] == "off":
        group_settings[chat_id]["spam"] = False
        await update.message.reply_text("❌ Spam block OFF")
    else:
        await update.message.reply_text("Use: /spam on or /spam off")


# ================== MAIN LOGIC ==================
async def auto_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.lower()
    chat_id = update.effective_chat.id
    user_id = update.message.from_user.id

    # default settings
    if chat_id not in group_settings:
        group_settings[chat_id] = {"link": False, "spam": False}

    # 🔗 Link block
    if group_settings[chat_id]["link"]:
        if "http" in text or "t.me" in text:
            try:
                await update.message.delete()
                return
            except:
                pass

    # 🚫 Spam block (basic)
    if group_settings[chat_id]["spam"]:
        if text.count(text) > 5:
            try:
                await update.message.delete()
                return
            except:
                pass

    # 🧮 Calculator
    try:
        result = f"{eval(text):.2f}"
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
app.add_handler(CommandHandler("link", link_control))
app.add_handler(CommandHandler("spam", spam_control))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_calc))

print("Bot running...")
app.run_polling()
