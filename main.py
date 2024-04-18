import sqlite3
import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
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

reply_keyboard = [['/address', '/phone'],
                  ['/site', '/work_time']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


async def start(update, context):
    await update.message.reply_text(
        "Привет! Это бот квизов. Чтобы начать новую игру введи ник.",
        reply_markup=ReplyKeyboardRemove()
    )
    global user_in
    user_in = 1


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


async def echo(update, context):
    global user_in
    if user_in == 1:
        await update.message.reply_text(
            f'Пользователь {update.message.text} зарегистирован! Нажми "/game", чтобы начать игру')
        user_in = 0

        # connection = sqlite3.connect('tg_bot.sqlite')
        # cursor = connection.cursor()
        # result_id = cursor.execute("""SELECT id FROM users ORDER BY id DESC limit 1""").fetchall()
        # id = result_id[0][0]
        # cursor.execute(f"INSERT INTO users VALUES (?,?,?), (id + 1, {update.message.text}, '')")
        # connection.commit()
        # connection.close()

    else:
        await update.message.reply_text("Выбери ответ из предложенных!")


async def help(update, context):
    await update.message.reply_text(
        "Я бот справочник.")


async def game(update, context):
    global user_in
    points = 2
    # await update.message.reply_text(
    #     "Адрес: г. Москва, ул. Льва Толстого, 16")
    while points != 0:
        connection = sqlite3.connect('tg_bot.sqlite')
        cursor = connection.cursor()
        result = cursor.execute(
            """SELECT ques, ans1, ans2, ans3, ans4, true_ans FROM questions ORDER BY RANDOM() limit 1""").fetchall()

        connection.commit()
        connection.close()
        reply_keyboard = [[f'{result[0][1]}'], [f'{result[0][2]}'],
                          [f'{result[0][3]}'], [f'{result[0][4]}']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text(
            result[0][0],
            reply_markup=markup
        )
        break


async def site(update, context):
    await update.message.reply_text(
        "Сайт: http://www.yandex.ru/company")





def main():
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token(BOT_TOKEN).build()

    # Зарегистрируем их в приложении перед
    # регистрацией обработчика текстовых сообщений.
    # Первым параметром конструктора CommandHandler я
    # вляется название команды.
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("game", game))
    application.add_handler(CommandHandler("site", site))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("close", close_keyboard))

    # Создаём обработчик сообщений типа filters.TEXT
    # из описанной выше асинхронной функции echo()
    # После регистрации обработчика в приложении
    # эта асинхронная функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    if user_in == 1:
        text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
        # Регистрируем обработчик в приложении.
        application.add_handler(text_handler)

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
