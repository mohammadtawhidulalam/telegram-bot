from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, InlineQueryHandler, ContextTypes, MessageHandler, filters
import uuid
import os

TOKEN = os.getenv("BOT_TOKEN")

# INLINE CALCULATOR
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
                    )
                )
            )
        except:
            pass

    await update.inline_query.answer(results, cache_time=1)


# AUTO REPLY CALCULATOR
async def auto_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text

    try:
        result = str(eval(text))
        await update.message.reply_text(result)
    except:
        pass


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(InlineQueryHandler(inline_calc))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_calc))

app.run_polling()
