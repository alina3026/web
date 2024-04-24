from flask import Flask, render_template
import sqlalchemy
from sqlalchemy import orm

# from .db_session import SqlAlchemyBase

app = Flask(__name__)


# class UsersTabl(SqlAlchemyBase):
#     __tablename__ = 'users'


@app.route('/')
@app.route('/Главная.html')
@app.route('/templates/Главная.html')
def gl():
    return render_template('index.html')


@app.route('/templates/Телеграм-бот.html')
@app.route('/Телеграм-бот.html')
def bot():
    return render_template('Телеграм-бот.html')


@app.route('/templates/Таблица-рейтинга.html')
@app.route('/Таблица-рейтинга.html')
def bot456():
    return render_template('Таблица-рейтинга.html')


if __name__ == '__main__':
    app.run()
