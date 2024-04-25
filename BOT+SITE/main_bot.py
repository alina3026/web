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

from map import send_Img

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
    quiz['bot_mode'] = 0
    await points_change()
    await update.message.reply_text(
        "Привет! Это бот квизов. Чтобы начать новую игру введи ник.",
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


async def help(update, context):
    await update.message.reply_text(
        "Я бот с интересными вопросами. Отвечай на них - зарабатывай баллы! Чтобы начать нажми /start. "
        "Если хочешь испугаться, нажми /address!")


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
    if answer == true_answer:
        await update.message.reply_text(f'{update.message.text} - правильный ответ! Вам начислен 1 балл')
        await points_change(1)
    elif answer in answer_options:
        await update.message.reply_text('К сожалению это неверно(...')


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
    if quiz['bot_mode'] == 1:
        adr = update.message.text
        quiz['bot_mode'] = 0
        await check_address(update, context, adr)
    if quiz['game_mode'] == 0:
        quiz['nick'] = update.message.text
        print('Регистрируем пользователя', quiz['nick'])
        quiz['game_mode'] = 1
        register(quiz['nick'])
        print(quiz)
    if quiz['game_mode'] == 1:
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
        # print('вывожу вопрос')
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text(
            result[0][0],
            reply_markup=markup
        )
        quiz['counts_questions'] -= 1
        quiz['degree'] = 1
        quiz['game_mode'] = 2
    if quiz['game_mode'] == 2:
        answer = update.message.text
        # print('вывожу результат')
        await check_ans(update, answer, answer_options(), true_answer())
        true_answer(quiz['true_answer'])
        answer_options(quiz['ans1'], quiz['ans2'], quiz['ans3'], quiz['ans4'])
    if quiz['counts_questions']:
        quiz['game_mode'] = 1
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


async def address(update, context):
    quiz = context.bot_data
    quiz['bot_mode'] = 1
    await update.message.reply_text("Скучно живете? Хочется больше щекотливых эмоций и адреналина в жизни?"
                                    " Вам к нам! Пришлите адрес своего дома, и мы отправим вам место, где вы живете! "
                                    "(Можно любое другое!)"
                                    " Отправьте адрес в формате: 'Город, адрес, дом'")


async def check_address(update, context, adr):
    print(adr)
    try:
        chat_id = update.effective_chat.id
        img = send_Img(adr)
        await context.bot.send_photo(chat_id=chat_id, photo=img)
    except:
        await update.message.reply_text('Карту с указанным адресом невозможно прислать')


def main():
    global bot_mode
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("game", game))
    application.add_handler(CommandHandler("site", site))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("address", address))

    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, game)
    application.add_handler(text_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
