from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import json
import psycopg2

app = Flask(__name__)


@app.route('/')
def main():
    return render_template("main.html")


@app.route('/all_users')
def all_users():
    info_person = requests.get('http://127.0.0.1:5001/person')
    return render_template("all_users.html", articles_person=info_person.json())


@app.route('/all_books')
def all_books():
    info_book = requests.get('http://127.0.0.1:5001/book')
    return render_template("all_books.html", articles_books=info_book.json())


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
def put_user(id):
    info_Book = requests.get(f'http://127.0.0.1:5001/book/{id}')
    if request.method == "POST":
        author = request.form['author']
        name = request.form['name']
        date_of_issue = request.form['date_of_issue']
        return_date = request.form['return_date']
        person_id = request.form['person_id']
        requests.put(f'http://127.0.0.1:5001/book/{id}/put',
                     json={"author": author, "name": name,
                           "date_of_issue": date_of_issue,
                           "return_date": return_date,
                           "person_id": person_id})
        return redirect('/all_books')
    else:
        return render_template("book_update.html", info_Book=info_Book.json())

if __name__ == "__main__":
    app.run(debug=True)