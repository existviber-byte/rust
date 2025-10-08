import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import subprocess

# ==== НАСТРОЙКИ ====
BOT_TOKEN = '7635605099:AAG32j38TXsPk2q4x9uNUuqZ_57wTavTK1U'
ADMIN_ID = 123456789  # Telegram ID администратора
RCON_COMMAND = './RustDedicated -rcon.port 28016 -rcon.password "YOUR_PASSWORD"'  # Пример запуска, не используется напрямую

# Логирование
logging.basicConfig(level=logging.INFO)

# === Хэндлер для ответов на сообщения с ID ===
async def handle_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        text = update.message.text
        original = update.message.reply_to_message.text

        if '🆔' in original:
            try:
                id_line = [line for line in original.splitlines() if "🆔" in line][0]
                question_id = id_line.split(":")[-1].strip().replace("<code>", "").replace("</code>", "")

                # Отправим через RCON или локально
                rcon_cmd = f"say Executing reply... && ask.reply {question_id} {text}"
                subprocess.call(["rcon", "-P", "28016", "-p", "YOUR_PASSWORD", "-c", rcon_cmd])

                await update.message.reply_text("✅ Ответ отправлен в Rust.")
            except Exception as e:
                logging.error(f"Ошибка: {e}")
                await update.message.reply_text("❌ Ошибка обработки.")
        else:
            await update.message.reply_text("⚠️ В оригинальном сообщении нет ID вопроса.")
    else:
        await update.message.reply_text("⚠️ Ответь на сообщение с вопросом.")

# === Запуск ===
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & filters.REPLY, handle_reply))
    print("✅ Бот запущен.")
    app.run_polling()

if __name__ == "__main__":
    main()

