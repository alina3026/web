import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler
from telegram.ext import ApplicationBuilder

# proxy_url = "socks5://user:pass@host:port"
#
# app = ApplicationBuilder().token("TOKEN").proxy_url(proxy_url).build()
BOT_TOKEN = '6533161431:AAH_iqGGFB5Ulk75XwXgdwa4zM16e5ccYJs'



# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def echo(update, context):
    await update.message.reply_text(f'Я получил сообщение {update.message.text}')


def main():
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token(BOT_TOKEN).build()

    async def start(update, context):
        """Отправляет сообщение когда получена команда /start"""
        user = update.effective_user
        await update.message.reply_html(
            rf"Привет {user.mention_html()}! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!",
        )

    async def help_command(update, context):
        """Отправляет сообщение когда получена команда /help"""
        await update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")

    # Зарегистрируем их в приложении перед
    # регистрацией обработчика текстовых сообщений.
    # Первым параметром конструктора CommandHandler я
    # вляется название команды.
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Создаём обработчик сообщений типа filters.TEXT
    # из описанной выше асинхронной функции echo()
    # После регистрации обработчика в приложении
    # эта асинхронная функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.

    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    # Регистрируем обработчик в приложении.
    application.add_handler(text_handler)


    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
