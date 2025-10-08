from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from valve.rcon import RCON

# === НАСТРОЙКИ ===
BOT_TOKEN = '7635605099:AAG32j38TXsPk2q4x9uNUuqZ_57wTavTK1U'            # токен от @BotFather
ADMIN_ID = 411379361                         # твой Telegram user ID
RCON_HOST = '37.230.137.6'            # IP или домен сервера
RCON_PORT = 20602                            # порт RCON (по умолчанию 28016)
RCON_PASSWORD = 'Derso250499'         # RCON-пароль сервера
# ================

async def handle_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ответа в Telegram (reply на сообщение от игрока)"""
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("❌ У тебя нет доступа.")
        return

    if update.message.reply_to_message:
        text = update.message.text
        original = update.message.reply_to_message.text

        # Ищем ID вопроса (в сообщении от плагина формат должен содержать: 🆔: <code>...</code>)
        if '🆔' in original:
            try:
                id_line = [line for line in original.splitlines() if "🆔" in line][0]
                question_id = id_line.split(":")[-1].strip().replace("<code>", "").replace("</code>", "")

                # Отправляем ответ через RCON -> ask.reply <id> <ответ>
                with RCON((RCON_HOST, RCON_PORT), RCON_PASSWORD) as rcon:
                    cmd = f'ask.reply {question_id} {text}'
                    result = rcon.execute(cmd)

                await update.message.reply_text("✅ Ответ отправлен игроку.")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка обработки: {e}")
                print(f"[ERROR] {e}")
        else:
            await update.message.reply_text("⚠️ Не найден ID вопроса в оригинальном сообщении.")
    else:
        await update.message.reply_text("⚠️ Ответь на сообщение от игрока, чтобы ответить ему.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & filters.REPLY, handle_reply))
    print("✅ Telegram-бот запущен.")
    app.run_polling()

if __name__ == "__main__":
    main()
