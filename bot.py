# bot.py
import os
import httpx
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_URL = "http://localhost:8000"
AGENT_URL = "http://localhost:8001"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я твой Task Manager бот.\n\n"
        "Просто напиши мне задачу и я её создам.\n"
        "Например: 'Иванов просит проверить holdtime, высокий приоритет'\n\n"
        "Команды:\n"
        "/tasks — список открытых задач\n"
        "/stats — статистика за текущий квартал"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text("⏳ Обрабатываю...")

    try:
        import sys

        sys.path.append("src")
        from agent import run_agent

        result = run_agent(user_message)
        await update.message.reply_text(f"✅ {result}")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")


async def get_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = httpx.get(f"{API_URL}/tasks/")
    tasks = response.json()
    open_tasks = [t for t in tasks if t["status"] == "В работе"]

    if not open_tasks:
        await update.message.reply_text("Нет открытых задач 🎉")
        return

    text = "📋 Открытые задачи:\n\n"
    for t in open_tasks:
        text += f"#{t['id']} {t['subject']}\n"
        text += f"   От: {t['sender']} | Приоритет: {t['priority']}\n\n"

    await update.message.reply_text(text)


async def get_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = httpx.get(f"{API_URL}/stats/", params={"quarter": "Q2 2026"})
    stats = response.json()
    text = (
        f"📊 Статистика Q2 2026:\n\n"
        f"Всего задач: {stats['total']}\n"
        f"Выполнено: {stats['completed']}\n"
        f"В работе: {stats['in_progress']}\n"
        f"Выполнение: {stats['completion_rate']}%"
    )
    await update.message.reply_text(text)


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tasks", get_tasks))
    app.add_handler(CommandHandler("stats", get_stats))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
