import os
import sqlite3
import logging
import random
import tracemalloc
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder

tracemalloc.start()
# proxy_url = "socks5://user:pass@host:port"
#
# app = ApplicationBuilder().token("TOKEN").proxy_url(proxy_url).build()
BOT_TOKEN = '6533161431:AAH_iqGGFB5Ulk75XwXgdwa4zM16e5ccYJs'
# Запускаем логгирование
logging.basicConfig(
    filename="bot.log", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update, context):
    quiz = context.bot_data
    quiz['game_mode'] = 0
    quiz['points'] = 2
    quiz['counts_questions'] = 5
    await points_change()
    await update.message.reply_text(
        "Привет! Это бот квизов. Чтобы начать новую игру введи ник.",
        reply_markup=ReplyKeyboardRemove()
    )


# async def close_keyboard(update, context):
#     await update.message.reply_text(
#         "Ok",
#         reply_markup=ReplyKeyboardRemove()
#     )


def register(name=''):
    connection = sqlite3.connect('tg_bot.sqlite')
    cursor = connection.cursor()
    result_id = cursor.execute("""SELECT id FROM users ORDER BY id DESC limit 1""").fetchall()
    id = result_id[0][0]
    cursor.execute("""INSERT INTO users VALUES (?,?,?)""", (id + 1, name, 0))
    connection.commit()
    connection.close()


async def help(update, context):
    await update.message.reply_text(
        "Я бот справочник.")


# async def new_question(update):
#     connection = sqlite3.connect('tg_bot.sqlite')
#     cursor = connection.cursor()
#     id_id = random.randint(1, 15)
#     result = cursor.execute("""SELECT ques, ans1, ans2, ans3, ans4, true_ans FROM questions WHERE id = ?""",
#                             (id_id,)).fetchall()
#     connection.commit()
#     connection.close()
#     if result:
#         return result
#     print('Из БД пустота')
#     await update.message.reply_text(f'{result[0][0]}')
#     reply_keyboard = [[f'{result[0][1]}'], [f'{result[0][2]}'],
#                       [f'{result[0][3]}'], [f'{result[0][4]}']]
#     markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
#     await update.message.reply_text(
#         result[0][0],
#         reply_markup=markup
#     )
# true_answer(result[0][5])


def check_points():
    with open("points.txt") as f:
        return int(f.read())


async def points_change(delta=0):
    points = check_points()
    with open("points.txt", "w") as f:
        if delta:
            f.write(str(points + delta))
        else:
            f.write(str(0))


async def check_ans(update, answer='', answer_options='', true_answer=''):
    # print('Ответ проверили:', answer, true_answer)
    print('ответ Юзера:', answer, "Правильный ответ:", true_answer, "Варианты:", answer_options)
    if answer == true_answer:
        print('Ответ дан правильный')
        await update.message.reply_text(f'{update.message.text} - правильный ответ! Вам начислен 1 балл')
        await points_change(1)
    elif answer in answer_options:
        print('Ответ дан неправильный')
        await update.message.reply_text('К сожалению это неверно(...')
        # await points_change(-1)
    else:
        print('странно')


def game_mode():
    with open("level.txt") as my_file:
        return int(my_file.read())


def game_mode_update(n):
    with open("level.txt", "w") as my_file:
        my_file.write(str(n))


def true_answer(ans=''):
    if ans:
        with open('true_answer.txt', 'w') as f:
            f.write(ans)
    else:
        with open('true_answer.txt') as f:
            return f.read()


def answer_options(ans1='', ans2='', ans3='', ans4=''):
    if ans1:
        with open('answer_options.txt', 'w') as f:
            f.write(ans1 + ans2 + ans3 + ans4)
    else:
        with open('answer_options.txt') as f:
            return f.read()


async def game(update, context):
    quiz = context.bot_data
    if quiz['game_mode'] == 0:
        quiz['nick'] = update.message.text
        print('Регистрируем пользователя', quiz['nick'])
        quiz['game_mode'] = 1
        register(quiz['nick'])
        print(quiz)
    if quiz['game_mode'] == 1:
        # print('Пошла игра для ' + quiz['nick'])
        quiz['game_mode'] = 2
        # result = new_question()
        connection = sqlite3.connect('tg_bot.sqlite')
        cursor = connection.cursor()
        id_id = random.randint(1, 15)
        result = cursor.execute("""SELECT ques, ans1, ans2, ans3, ans4, true_ans FROM questions WHERE id = ?""",
                                (id_id,)).fetchall()
        connection.commit()
        connection.close()
        quiz['true_answer'] = (result[0][5])
        quiz['ans1'] = result[0][1]
        quiz['ans2'] = result[0][2]
        quiz['ans3'] = result[0][3]
        quiz['ans4'] = result[0][4]
        reply_keyboard = [[f'{result[0][1]}'], [f'{result[0][2]}'],
                          [f'{result[0][3]}'], [f'{result[0][4]}']]
        quiz['counts_questions'] -= 1
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text(
            result[0][0],
            reply_markup=markup
        )
    if quiz['game_mode'] == 2:
        # print('Режим проверки ответа')
        # quiz['game_mode'] = 1
        # if not (true_answer()):
        #     await new_question()
        # else:
        answer = update.message.text
        # print(f'Ответ пользователя: {answer}')
        await check_ans(update, answer, answer_options(), true_answer())
        # if not (true_answer()):
        #     await new_question(update)
        #     print('тру ансвер пустой')
        # else:
        # answer = update.message.text
        # print(f'Ответ пользователя: {answer}')
        # await check_ans(update, answer, quiz['ans1'], quiz['ans2'], quiz['ans3'], quiz['ans4'], true_answer())
        true_answer(quiz['true_answer'])
        answer_options(quiz['ans1'], quiz['ans2'], quiz['ans3'], quiz['ans4'])
    # if check_points():
    if quiz['counts_questions']:
        # await new_question()
        # await new_question(update)
        # print("Проверили, баллов достаточно")
        quiz['game_mode'] = 1
        # quiz['game_mode'] = 1
    else:
        await stop(update, context)


async def stop(update, context):
    n = check_points()
    connection = sqlite3.connect('tg_bot.sqlite')
    cursor = connection.cursor()
    result_id = cursor.execute("""SELECT id FROM users ORDER BY id DESC limit 1""").fetchall()
    id = result_id[0][0]
    cursor.execute(f'UPDATE users SET balls={n} WHERE id={id}')
    connection.commit()
    connection.close()

    await update.message.reply_text(
        f'ИГРА ЗАКОНЧЕНА. Заработанных баллов: {n}. Статистику пользователей можно посмотреть по ссылке: http://www.yandex.ru/company',
        reply_markup=ReplyKeyboardRemove()
    )


async def site(update, context):
    await update.message.reply_text(
        "Сайт: http://www.yandex.ru/company")


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("game", game))
    application.add_handler(CommandHandler("site", site))
    application.add_handler(CommandHandler("help", help))

    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, game)
    application.add_handler(text_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
