import os
import sqlite3
import logging
import random

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


async def start(update, context):
    await update.message.reply_text(
        "Привет! Это бот квизов. Чтобы начать новую игру введи ник.",
        reply_markup=ReplyKeyboardRemove()
    )
    user_in = 1
    # os.system(r'nul>level.txt')

    with open("level.txt", "a+") as my_file:
        my_file.write('@')
        my_file.write(str(user_in))


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


async def echo(update, context):
    with open("level.txt", "r+") as my_file:
        x = my_file.read().split('@')[-1]
        user_in = x[0]

    if user_in == '1':
        await update.message.reply_text(
            f'Пользователь {update.message.text} зарегистирован! Нажми "/game", чтобы начать игру')
        user_in = 0
        with open("level.txt", "a+") as my_file:
            my_file.write('@')
            my_file.write(str(user_in))

        # connection = sqlite3.connect('tg_bot.sqlite')
        # cursor = connection.cursor()
        # result_id = cursor.execute("""SELECT id FROM users ORDER BY id DESC limit 1""").fetchall()
        # id = result_id[0][0]
        # cursor.execute(f"INSERT INTO users VALUES (?,?,?), (id + 1, {update.message.text}, '')")
        # connection.commit()
        # connection.close()

    # else:
    #     await update.message.reply_text("Выбери ответ из предложенных!")


# async def check_answer(update, context):
#     global result
#     global points
#     with open("level.txt", "r+") as my_file:
#         x = my_file.read().split('@')[-1]
#         user_in = x[0]
#         if x[0] == 'Q':
#             if update.message.text == result[0][5]:
#                 await update.message.reply_text(f'{update.message.text} - правильный ответ! Вам начислен 1 балл')
#                 points += 1
#             else:
#                 await update.message.reply_text('К сожалению это неверно(...')
#                 points -= 1
#             with open("level.txt", "a+") as my_file:
#                 my_file.write('@')
#                 my_file.write('A')


async def help(update, context):
    await update.message.reply_text(
        "Я бот справочник.")


async def game(update, context):
    global points
    global result
    points = 2
    # не засовывать внутрь цикла!!!!!!!!!!!!
    with open("level.txt", "a+") as my_file:
        my_file.write('@')
        my_file.write('A')
    while points != 0:
        connection = sqlite3.connect('tg_bot.sqlite')
        cursor = connection.cursor()
        id_id = random.randint(1, 3)
        result = cursor.execute(
            """SELECT ques, ans1, ans2, ans3, ans4, true_ans FROM questions WHERE id = ?""", (id_id,)).fetchall()
        # result = cursor.execute(
        #     """SELECT ques, ans1, ans2, ans3, ans4, true_ans FROM questions ORDER BY RANDOM() limit 1""").fetchall()
        connection.commit()
        connection.close()

        with open("level.txt", "r+") as my_file:
            x = my_file.read().split('@')[-1]
            user_in = x[0]
            if user_in == 'A':
                reply_keyboard = [[f'{result[0][1]}'], [f'{result[0][2]}'],
                                  [f'{result[0][3]}'], [f'{result[0][4]}']]
                markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
                await update.message.reply_text(
                    result[0][0],
                    reply_markup=markup
                )
                with open("level.txt", "a+") as my_file:
                    my_file.write('@')
                    my_file.write('Q')
        with open("level.txt", "r+") as my_file:
            x = my_file.read().split('@')[-1]
            user_in = x[0]
            if user_in == 'Q':
                if update.message.text == result[0][5]:
                    await update.message.reply_text(f'{update.message.text} - правильный ответ! Вам начислен 1 балл')
                    points += 1
                else:
                    await update.message.reply_text('К сожалению это неверно(...')
                    points -= 1
                with open("level.txt", "a+") as my_file:
                    my_file.write('@')
                    my_file.write('A')


async def site(update, context):
    await update.message.reply_text(
        "Сайт: http://www.yandex.ru/company")


def main():
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
    with open("level.txt", "r+") as my_file:
        x = my_file.read().split('@')[-1]
        user_in = x[0]
        if user_in == '1':
            text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
            application.add_handler(text_handler)
        elif user_in == 'A':
            text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, game)
            application.add_handler(text_handler)
        # elif user_in == 'Q':
        #     text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer)
        #     application.add_handler(text_handler)
        # elif user_in == 'A':
        #     text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, game)
        #     application.add_handler(text_handler)
    # Запускаем приложение.
    application.run_polling()


if __name__ == '__main__':
    main()
