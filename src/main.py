from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import json
import psycopg2
import pytz
from datetime import datetime, timedelta
from dateutil.parser import parse

app = Flask(__name__)


@app.route('/')
def main():
    return render_template("main.html")


@app.route('/statistics/all')
def statistics_all():
    articles = requests.get('http://127.0.0.1:5001/date_of_take')
    data = []
    data_keys = list(articles.json().keys())
    data_values = list(articles.json().values())
    for i in range(len(articles.json())):
        data.append([data_keys[i], data_values[i]])
    return render_template("statistics.html", data=data)


@app.route('/statistics/week')
def statistics_weak():
    articles = requests.get('http://127.0.0.1:5001/date_of_take')
    data = []
    data_keys = list(articles.json().keys())
    data_values = list(articles.json().values())
    for i in range(len(articles.json())):
        data.append([data_keys[i], data_values[i]])
    data = data[:-8:-1]
    data = data[::-1]
    return render_template("statistics.html", data=data)


@app.route('/statistics/last_month')
def statistics_last_month():
    articles = requests.get('http://127.0.0.1:5001/date_of_take')
    data = []
    data_keys = list(articles.json().keys())
    data_values = list(articles.json().values())
    for i in range(len(articles.json())):
        data.append([data_keys[i], data_values[i]])
    data = data[:-31:-1]
    data = data[::-1]
    return render_template("statistics.html", data=data)


@app.route('/statistics/month')
def statistics_month():
    articles = requests.get('http://127.0.0.1:5001/date_of_take/month')
    data = []
    data_keys = list(articles.json().keys())
    data_values = list(articles.json().values())
    for i in range(len(articles.json())):
        data.append([data_keys[i], data_values[i]])
    return render_template("statistics.html", data=data)


@app.route('/statistics/year')
def statistics_year():
    articles = requests.get('http://127.0.0.1:5001/date_of_take/year')
    data = []
    data_keys = list(articles.json().keys())
    data_values = list(articles.json().values())
    for i in range(len(articles.json())):
        data.append([data_keys[i], data_values[i]])
    return render_template("statistics.html", data=data)


@app.route('/all_users')
def all_users():
    info_person = requests.get('http://127.0.0.1:5001/person')
    return render_template("all_users.html", articles_person=info_person.json())


@app.route('/all_books', methods=['POST', 'GET'])
def all_books():
    info_book = requests.get('http://127.0.0.1:5001/book').json()
    if request.method == "POST":
        arrears = int(request.form['arrears'])
        return redirect(f"/all_books/arrears/{arrears}")
    return render_template("all_books.html", articles_books=info_book)


@app.route('/all_books/arrears/<int:arrears>', methods=['POST', 'GET'])
def all_books_arrears(arrears):
    info_book = requests.get('http://127.0.0.1:5001/book').json()
    data_arrears = []
    for i in info_book:
        if type(i["date_of_issue"]) == str:
            new_time = parse(i["date_of_issue"])
            time_now = datetime.now(pytz.timezone('Europe/Moscow')).strftime("%Y-%m-%d")
            if new_time.date() + timedelta(days=arrears) < parse(time_now).date():
                data_arrears.append(i)
    return render_template("all_books_arrears.html", articles_books=data_arrears, arrears=arrears)


@app.route('/add_person', methods=['POST', 'GET'])
def create_user():
    if request.method == "POST":
        surname = request.form['surname']
        name = request.form['name']
        patronymic = request.form['patronymic']
        cafedra = request.form['cafedra']
        passport_data = request.form['passport_data']
        date_of_birthday = request.form['date_of_birthday']
        registration = request.form['registration']
        place_of_residence = request.form['place_of_residence']
        telephone = request.form['telephone']

        requests.post('http://127.0.0.1:5001/add_user', json={"surname": surname, "name": name,
                                                              "patronymic": patronymic,
                                                              "cafedra": cafedra,
                                                              "passport_data": passport_data,
                                                              "date_of_birthday": date_of_birthday,
                                                              "registration": registration,
                                                              "place_of_residence": place_of_residence,
                                                              "telephone": telephone})
        return redirect('/all_users')
    else:
        return render_template("add_user.html")


@app.route('/add_book', methods=['POST', 'GET'])
def add_book():
    if request.method == "POST":
        author = request.form['author']
        name = request.form['name']

        requests.post('http://127.0.0.1:5001/add_book', json={"author": author, "name": name})
        return redirect('/all_books')
    else:
        return render_template("add_book.html")


@app.route('/book/<int:id>/put', methods=['POST', 'GET'])
def put_book(id):
    info_Book = requests.get(f'http://127.0.0.1:5001/book/{id}')
    if request.method == "POST":

        author = request.form['author']
        name = request.form['name']
        person_id = request.form['person_id']
        requests.put(f'http://127.0.0.1:5001/book/{id}/put',
                     json={"author": author, "name": name,
                           "person_id": person_id, "id": id})
        return redirect('/all_books')
    else:
        return render_template("book_update.html", info_Book=info_Book.json())


@app.route('/all_users/<int:id>/put', methods=['POST', 'GET'])
def put_user(id):
    info_Person = requests.get(f'http://127.0.0.1:5001/all_users/{id}')
    if request.method == "POST":
        surname = request.form['surname']
        name = request.form['name']
        patronymic = request.form['patronymic']
        cafedra = request.form['cafedra']
        passport_data = request.form['passport_data']
        date_of_birthday = request.form['date_of_birthday']
        registration = request.form['registration']
        place_of_residence = request.form['place_of_residence']
        telephone = request.form['telephone']

        requests.put(f'http://127.0.0.1:5001/all_users/{id}/put', json={"surname": surname, "name": name,
                                                              "patronymic": patronymic,
                                                              "cafedra": cafedra,
                                                              "passport_data": passport_data,
                                                              "date_of_birthday": date_of_birthday,
                                                              "registration": registration,
                                                              "place_of_residence": place_of_residence,
                                                              "telephone": telephone})
        return redirect('/all_users')
    else:
        return render_template("user_update.html", info_Person=info_Person.json())


if __name__ == "__main__":
    app.run(debug=True)