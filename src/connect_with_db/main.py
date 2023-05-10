from flask import Flask, render_template, url_for, request, redirect, url_for, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:AlEx1902345@localhost/library'

db = SQLAlchemy(app)

data_person = []
data_book = []


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(40), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    patronymic = db.Column(db.String(40), nullable=False)
    date_of_issue_id = db.Column(db.DateTime, default=datetime.utcnow)
    cafedra = db.Column(db.String(40), nullable=False)
    passport_data = db.Column(db.String(40), nullable=False)
    date_of_birthday = db.Column(db.String(40), nullable=False)
    registration = db.Column(db.String(60), nullable=False)
    place_of_residence = db.Column(db.String(60), nullable=False)
    telephone = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"<Person {self.id}>"


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(40), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    date_of_issue = db.Column(db.DateTime, nullable=True)
    return_date = db.Column(db.DateTime, nullable=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=True)


    def __repr__(self):
        return f"<Person {self.id}>"


@app.route('/person')
def get_all_person():
    info = Person.query.order_by(Person.id).all()
    data_person.clear()
    for el in info:
        dict_json = {'id': el.id, 'surname': el.surname, 'name': el.name, 'patronymic': el.patronymic,
                     'date_of_issue_id': el.date_of_issue_id, 'cafedra': el.cafedra,
                     'passport_data': el.passport_data, 'date_of_birthday': el.date_of_birthday,
                     'registration': el.registration, 'place_of_residence': el.place_of_residence,
                     'telephone': el.telephone}
        data_person.append(dict_json)
    articles = jsonify(data_person)
    return articles


@app.route('/book')
def get_all_book():
    info = Book.query.order_by(Book.id).all()
    data_book.clear()
    for el in info:
        dict_json = {'id': el.id, 'author': el.author, 'name': el.name, 'date_of_issue': el.date_of_issue,
                     'return_date': el.return_date, 'person_id': el.person_id}
        data_book.append(dict_json)
    articles = jsonify(data_book)
    return articles


@app.route('/person/<int:id>')
def get_person(id):
    info_person = Person.query.get(id)
    dict_json = {'id': info_person.id, 'surname': info_person.surname, 'name': info_person.name,
                 'patronymic': info_person.patronymic,
                 'date_of_issue_id': info_person.date_of_issue_id, 'cafedra': info_person.cafedra,
                 'passport_data': info_person.passport_data, 'date_of_birthday': info_person.date_of_birthday,
                 'registration': info_person.registration, 'place_of_residence': info_person.place_of_residence,
                 'telephone': info_person.telephone}
    return jsonify(dict_json)


@app.route('/book/<int:id>')
def get_book(id):
    info_book = Book.query.get(id)
    dict_json = {'id': info_book.id, 'author': info_book.author, 'name': info_book.name,
                 'date_of_issue': info_book.date_of_issue,
                 'return_date': info_book.return_date, 'person_id': info_book.person_id}
    return jsonify(dict_json)


@app.route('/book/<int:id>/put',  methods=['PUT'])
def put_user(id):
    info_book = Book.query.get_or_404(id)
    info_book.author = request.json['author']
    info_book.name = request.json['name']
    info_book.person_id = request.json['person_id']

    db.session.commit()


@app.route('/add_user', methods=['POST'])
def add_user():
    with app.app_context():
        surname = request.json['surname']
        name = request.json['name']
        patronymic = request.json['patronymic']
        cafedra = request.json['cafedra']
        passport_data = request.json['passport_data']
        date_of_birthday = request.json['date_of_birthday']
        registration = request.json['registration']
        place_of_residence = request.json['place_of_residence']
        telephone = request.json['telephone']

        person = Person(surname=surname, name=name, patronymic=patronymic, cafedra=cafedra,
                        passport_data=passport_data, date_of_birthday=date_of_birthday,
                        registration=registration, place_of_residence=place_of_residence,
                        telephone=telephone)

        db.session.add(person)
        db.session.commit()


@app.route('/add_book', methods=['POST'])
def add_book():
    with app.app_context():
        author = request.json['author']
        name = request.json['name']

        book = Book(author=author, name=name)

        db.session.add(book)
        db.session.commit()


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(port=5001, debug=True)