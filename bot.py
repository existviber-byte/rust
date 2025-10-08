from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from valve.rcon import RCON  # <-- Python RCON клиент

# ========== НАСТРОЙКИ ==========
BOT_TOKEN = '7635605099:AAG32j38TXsPk2q4x9uNUuqZ_57wTavTK1U'
ADMIN_ID = 123456789  # ← твой Telegram ID (число)
RCON_HOST = '37.230.137.6'
RCON_PORT = 20602
RCON_PASSWORD = 'Derso250499'
# ===============================

async def handle_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        text = update.message.text
        original = update.message.reply_to_message.text

        if '🆔' in original:
            try:
                # Получаем ID вопроса из сообщения
                id_line = [line for line in original.splitlines() if "🆔" in line][0]
                question_id = id_line.split(":")[-1].strip().replace("<code>", "").replace("</code>", "")

                # Подключаемся к RCON и отправляем команду
                with RCON((RCON_HOST, RCON_PORT), RCON_PASSWORD) as rcon:
                    cmd = f'ask.reply {question_id} {text}'
                    response = rcon.execute(cmd)

                await update.message.reply_text("✅ Ответ отправлен игроку.")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка обработки: {e}")
                print(f"[ERROR] {e}")
        else:
            await update.message.reply_text("⚠️ В оригинальном сообщении нет ID вопроса.")
    else:
        await update.message.reply_text("⚠️ Ответь на сообщение с вопросом.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & filters.REPLY, handle_reply))
    print("✅ Бот запущен.")
    app.run_polling()

if __name__ == "__main__":
    main()
