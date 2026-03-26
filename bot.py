from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, InlineQueryHandler, ContextTypes
import uuid
import os

TOKEN = os.getenv("8763225409:AAHz3dPmAY_lJvJE-h9b8xAEUKc_QxwsbMc")

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

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(InlineQueryHandler(inline_calc))

app.run_polling()