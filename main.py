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
    await update.message.reply_text(
        "Привет! Это бот квизов. Чтобы начать новую игру введи ник.",
        reply_markup=ReplyKeyboardRemove()
    )
    # os.system(r'nul>level.txt')
    # game_mode_update(1)


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


def register(name=''):
    connection = sqlite3.connect('tg_bot.sqlite')
    cursor = connection.cursor()
    result_id = cursor.execute("""SELECT id FROM users ORDER BY id DESC limit 1""").fetchall()
    id = result_id[0][0]
    cursor.execute("""INSERT INTO users VALUES (?,?,?)""", (id + 1, name, 0))
    connection.commit()
    connection.close()
    # game_mode_update(1)


# else:
#     await update.message.reply_text("Выбери ответ из предложенных!")


async def help(update, context):
    await update.message.reply_text(
        "Я бот справочник.")


async def new_question():
    connection = sqlite3.connect('tg_bot.sqlite')
    cursor = connection.cursor()
    id_id = random.randint(1, 16)
    result = cursor.execute("""SELECT ques, ans1, ans2, ans3, ans4, true_ans FROM questions WHERE id = ?""",
                            (id_id,)).fetchall()
    connection.commit()
    connection.close()
    if result:
        return result
    print('Из БД пустота')


def check_points():
    with open("points.txt") as f:
        return int(f.read())


async def points_change(delta=0):
    points = check_points()
    with open("points.txt", "w") as f:
        f.write(str(points + delta))


async def check_ans(update, answer='', true_answer=''):
    if answer == true_answer:
        await update.message.reply_text(f'{update.message.text} - правильный ответ! Вам начислен 1 балл')
        await points_change(1)
    else:
        # elif answer in [result[0][1], result[0][2], result[0][3], result[0][4]]:
        await update.message.reply_text('К сожалению это неверно(...')
        await points_change(-1)

    # with open("points.txt", "a+") as my_file:
    #     my_file.write('@')
    #     my_file.write(str(points))


def game_mode():
    with open("level.txt") as my_file:
        return int(my_file.read())


def game_mode_update(n):
    with open("level.txt", "w") as my_file:
        my_file.write(str(n))


# async def start_game(update, context):
# game_mode_update(1)
# await new_question(update)

def true_answer(ans=''):
    if ans:
        with open('true_answer.txt', 'w') as f:
            f.write(ans)
    else:
        with open('true_answer.txt') as f:
            return f.read()


async def game(update, context):
    quiz = context.bot_data

    if quiz['game_mode'] == 0:
        quiz['nick'] = update.message.text
        print('Регистрируем пользователя', quiz['nick'])
        quiz['game_mode'] = 1
        register(quiz['nick'])
        # await update.message.reply_text(
        #     f'Пользователь {quiz["nick"]} зарегистирован! Нажми "/game", чтобы начать игру'
        # )
        print(quiz)
    elif quiz['game_mode'] == 1:
        print('Пошла игра для ' + quiz['nick'])
        quiz['game_mode'] = 2
        # result = new_question()
        connection = sqlite3.connect('tg_bot.sqlite')
        cursor = connection.cursor()
        id_id = random.randint(1, 16)
        result = cursor.execute("""SELECT ques, ans1, ans2, ans3, ans4, true_ans FROM questions WHERE id = ?""",
                                (id_id,)).fetchall()
        connection.commit()
        connection.close()
        reply_keyboard = [[f'{result[0][1]}'], [f'{result[0][2]}'],
                          [f'{result[0][3]}'], [f'{result[0][4]}']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text(
            result[0][0]
            # reply_markup=markup
        )
    elif quiz['game_mode'] == 2:
        print('Режим проверки ответа')
        # input()
        quiz['game_mode'] = 1
        if not (true_answer()):
            await new_question()
        else:
            answer = update.message.text
            await check_ans(update, answer, true_answer())
            if check_points():
                await new_question()


async def stop(update, context):
    await update.message.reply_text('GAME OVER')
    # запись в бд

    # with open("points.txt") as out_file:
    #     x = out_file.read().split('@')[-1]
    #     points = int(x[0])
    # if points > 0:
    #     connection = sqlite3.connect('tg_bot.sqlite')
    #     cursor = connection.cursor()
    #     id_id = random.randint(1, 3)
    #     result = cursor.execute("""SELECT ques, ans1, ans2, ans3, ans4, true_ans FROM questions WHERE id = ?""",
    #                             (id_id,)).fetchall()
    #     connection.commit()
    #     connection.close()
    #     reply_keyboard = [[f'{result[0][1]}'], [f'{result[0][2]}'],
    #                       [f'{result[0][3]}'], [f'{result[0][4]}']]
    #     markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    #     await update.message.reply_text(
    #         result[0][0],
    #         reply_markup=markup
    #     )
    #     ans = update.message.text
    #     true_ans = result[0][5]
    #
    #     await check_ans(update, ans, true_ans)
    # else:
    #     await update.message.reply_text('Приятно было пообщаться')

    # if update.message.text == result[0][5]:
    #     await update.message.reply_text(f'{update.message.text} - правильный ответ! Вам начислен 1 балл')
    #     points += 1
    # elif update.message.text == result[0][1] or update.message.text == result[0][
    #     3] or update.message.text == result[0][4]:
    #     await update.message.reply_text('К сожалению это неверно(...')
    #     points -= 1


async def site(update, context):
    await update.message.reply_text(
        "Сайт: http://www.yandex.ru/company")


def main():
    # game_mode_update(0)
    # true_answer('')
    application = Application.builder().token(BOT_TOKEN).build()
    # Зарегистрируем их в приложении перед
    # регистрацией обработчика текстовых сообщений.
    # Первым параметром конструктора CommandHandler я
    # вляется название команды.
    application.add_handler(CommandHandler("start", start))
    # application.add_handler(CommandHandler("start_game", stagame))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("game", game))
    application.add_handler(CommandHandler("site", site))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("close", close_keyboard))
    # Создаём обработчик сообщений типа filters.TEXT
    # из описанной выше асинхронной функции echo()
    # После регистрации обработчика в приложении
    # эта асинхронная функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, game)
    application.add_handler(text_handler)

    # if game_mode() == 0:
    #     text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, register)
    #     application.add_handler(text_handler)
    #
    # if game_mode() == 1:
    #     if check_points():
    #         text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, game)
    #         application.add_handler(text_handler)

    # if game_mode() == 2:
    #     text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, game)
    #     application.add_handler(text_handler)

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
