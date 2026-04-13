import os
import logging
import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN not set!")

URL = os.environ.get("RENDER_EXTERNAL_URL", "http://localhost:8000")
PORT = int(os.getenv("PORT", 8000))

WAIT_START_BUTTON, WAIT_FIRST_SWEET = range(2)

START_BUTTON = KeyboardButton("🍬 Начать приключение!")
START_MARKUP = ReplyKeyboardMarkup([[START_BUTTON]], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🍬 Привет! Я бот профессора Сладкова!\n\n"
        "Нажми кнопку «Начать приключение!», чтобы начать квест! 👇",
        reply_markup=START_MARKUP
    )
    return WAIT_START_BUTTON

async def button_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Отлично! Первый вопрос:\n\n"
        "**Какая сладость в самой большой упаковке?**\n"
        "Подсказка: 16 букв, похожа на облачка",
        parse_mode="Markdown"
    )
    return WAIT_FIRST_SWEET

async def check_first_sweet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.message.text.lower().strip()
    if answer == "воздушные зефирки":
        await update.message.reply_text(
            "✅ Правильно! Ты прошёл первый этап!\n\n"
            "🎬 Смотри мультфильм: https://youtu.be/BDNfNYRaexg"
        )
        return ConversationHandler.END
    else:
        await update.message.reply_text("❌ Неправильно, попробуй ещё раз!")
        return WAIT_FIRST_SWEET

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Квест прерван. Напиши /start чтобы начать заново.")
    return ConversationHandler.END

async def main():
    app = Application.builder().token(TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WAIT_START_BUTTON: [MessageHandler(filters.Regex("^🍬 Начать приключение!$"), button_start)],
            WAIT_FIRST_SWEET: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_first_sweet)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv_handler)
    
    print("Бот запущен на порту", PORT)
    
    # Запускаем вебхук
    await app.initialize()
    await app.bot.set_webhook(url=f"{URL}/telegram", allowed_updates=Update.ALL_TYPES)
    print(f"Webhook установлен на {URL}/telegram")
    
    # Запускаем сервер
    from starlette.applications import Starlette
    from starlette.routing import Route
    from starlette.requests import Request
    from starlette.responses import Response, PlainTextResponse
    import uvicorn
    
    async def telegram_webhook(request: Request) -> Response:
        """Обработка входящих обновлений от Telegram"""
        data = await request.json()
        update = Update.de_json(data, app.bot)
        await app.process_update(update)
        return Response()
    
    async def health_check(request: Request) -> PlainTextResponse:
        return PlainTextResponse("OK")
    
    starlette_app = Starlette(routes=[
        Route("/telegram", telegram_webhook, methods=["POST"]),
        Route("/healthcheck", health_check, methods=["GET"]),
    ])
    
    config = uvicorn.Config(starlette_app, host="0.0.0.0", port=PORT, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
