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
                    input_message_content=InputTextMessageContent(f"{query} = {result}")
                )
            )
        except:
            pass

    await update.inline_query.answer(results)


# ================== START ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot ready!\nUse /help")


# ================== HELP ==================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🆘 Commands:\n\n"
        "/link on/off → link block\n"
        "/spam on/off → spam block\n"
        "/stats → usage\n"
    )


# ================== SETTINGS COMMAND ==================
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


# ================== STATS ==================
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    count = user_usage.get(user_id, 0)
    await update.message.reply_text(f"📊 Uses: {count}")


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

    # 🔗 link block
    if group_settings[chat_id]["link"]:
        if "http" in text or "t.me" in text:
            try:
                await update.message.delete()
                return
            except:
                pass

    # 🚫 spam block (same message repeat)
    if group_settings[chat_id]["spam"]:
        if text.count(text) > 5:
            try:
                await update.message.delete()
                return
            except:
                pass

    # 🧮 calculator
    try:
        result = str(eval(text))
        user_usage[user_id] = user_usage.get(user_id, 0) + 1
        await update.message.reply_text(result)
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
