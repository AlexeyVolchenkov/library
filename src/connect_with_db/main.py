from flask import Flask, render_template, url_for, request, redirect, url_for, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import pytz
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
    date_of_issue_id = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Europe/Moscow')))
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


class Date_book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_of_take = db.Column(db.Date, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=True)


    def __repr__(self):
        return f"<Date_book {self.id}>"


@app.route('/date_of_take')
def get_date_of_take():
    info = Date_book.query.order_by(Date_book.date_of_take).all()
    arr_of_dicts = {}
    data = []
    for i in info:
        data.append(str(i.date_of_take))
    data_unique = set(data)
    for i in data_unique:
        arr_of_dicts[i] = data.count(i)
    return jsonify(arr_of_dicts)


@app.route('/date_of_take/month')
def get_date_of_take_month():
    info = Date_book.query.order_by(Date_book.date_of_take).all()
    arr_of_dicts = {}
    data = []
    for i in info:
        data.append(i.date_of_take)
    for i, el in enumerate(data):
        data[i] = data[i].strftime("%Y-%m")
    data_unique = set(data)
    for i in data_unique:
        arr_of_dicts[i] = data.count(i)
    return jsonify(arr_of_dicts)


@app.route('/date_of_take/year')
def get_date_of_take_year():
    info = Date_book.query.order_by(Date_book.date_of_take).all()
    arr_of_dicts = {}
    data = []
    for i in info:
        data.append(i.date_of_take)
    for i, el in enumerate(data):
        data[i] = data[i].strftime("%Y")
    data_unique = set(data)
    for i in data_unique:
        arr_of_dicts[i] = data.count(i)
    return jsonify(arr_of_dicts)


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


@app.route('/all_users/<int:id>')
def get_person(id):
    info_person = Person.query.get(id)
    dict_json = {'id': info_person.id, 'surname': info_person.surname, 'name': info_person.name,
                 'patronymic': info_person.patronymic,
                 'date_of_issue_id': info_person.date_of_issue_id, 'cafedra': info_person.cafedra,
                 'passport_data': info_person.passport_data, 'date_of_birthday': info_person.date_of_birthday,
                 'registration': info_person.registration, 'place_of_residence': info_person.place_of_residence,
                 'telephone': info_person.telephone}
    return jsonify(dict_json)


@app.route('/all_users/<int:id>/delete')
def delete_person(id):
    info_book = Person.query.get(id)
    db.session.delete(info_book)
    db.session.commit()
    return redirect('http://127.0.0.1:5000/all_users')


@app.route('/book/<int:id>')
def get_book(id):
    info_book = Book.query.get(id)
    print(info_book)
    print(type(info_book))
    dict_json = {'id': info_book.id, 'author': info_book.author, 'name': info_book.name,
                 'date_of_issue': info_book.date_of_issue,
                 'return_date': info_book.return_date, 'person_id': info_book.person_id}
    return jsonify(dict_json)


@app.route('/book/<int:id>/delete')
def delete_book(id):
    info_book = Book.query.get(id)
    db.session.delete(info_book)
    db.session.commit()
    return redirect('http://127.0.0.1:5000/all_books')


@app.route('/book/<int:id>/put',  methods=['PUT'])
def put_book(id):
    info_book = Book.query.get_or_404(id)
    info_book.author = request.json['author']
    info_book.name = request.json['name']
    info_book.person_id = request.json['person_id']
    if int(info_book.person_id) == 0:
        info_book.person_id = None
        info_book.date_of_issue = None
        info_book.return_date = datetime.now(pytz.timezone('Europe/Moscow'))
    else:
        date_book = Date_book(date_of_take=datetime.now(pytz.timezone('Europe/Moscow')).strftime("%Y-%m-%d"),
                              book_id=request.json['id'])
        db.session.add(date_book)
        info_book.date_of_issue = datetime.now(pytz.timezone('Europe/Moscow'))
        info_book.return_date = None

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


@app.route('/all_users/<int:id>/put',  methods=['PUT'])
def put_user(id):
    info_person = Person.query.get_or_404(id)
    info_person.surname = request.json['surname']
    info_person.name = request.json['name']
    info_person.patronymic = request.json['patronymic']
    info_person.cafedra = request.json['cafedra']
    info_person.passport_data = request.json['passport_data']
    info_person.date_of_birthday = request.json['date_of_birthday']
    info_person.registration = request.json['registration']
    info_person.place_of_residence = request.json['place_of_residence']
    info_person.telephone = request.json['telephone']

    db.session.commit()

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(port=5001, debug=True)