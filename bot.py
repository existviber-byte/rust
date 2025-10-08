import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import subprocess

# ==== НАСТРОЙКИ ====
BOT_TOKEN = '7635605099:AAG32j38TXsPk2q4x9uNUuqZ_57wTavTK1U'
ADMIN_ID = 123456789  # Telegram ID администратора
RCON_COMMAND = './RustDedicated -rcon.port 20602 -rcon.password "YOUR_PASSWORD"'  # Пример запуска, не используется напрямую

# Логирование
logging.basicConfig(level=logging.INFO)

# === Хэндлер для ответов на сообщения с ID ===
from valve.rcon import RCON

async def handle_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        text = update.message.text
        original = update.message.reply_to_message.text

        if '🆔' in original:
            try:
                id_line = [line for line in original.splitlines() if "🆔" in line][0]
                question_id = id_line.split(":")[-1].strip().replace("<code>", "").replace("</code>", "")

                # Подключаемся к RCON
                with RCON(("37.230.137.6", 20602), "Derso250499") as rcon:
                    cmd = f"say Ответ администрации на вопрос {question_id}: {text}"
                    rcon.execute(cmd)
                    rcon.execute(f"ask.reply {question_id} {text}")

                await update.message.reply_text("✅ Ответ отправлен в Rust.")
            except Exception as e:
                print(f"Ошибка: {e}")
                await update.message.reply_text(f"❌ Ошибка обработки: {e}")
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



