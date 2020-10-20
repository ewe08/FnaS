import os
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


main = Flask(__name__)
main.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
main.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database = SQLAlchemy(main)
UPLOAD_FOLDER_FOR_IMAGES ="D:\project for pyton\FnaS\covers"
UPLOAD_FOLDER_FOR_FILES = "D:\project for pyton\FnaS\libary"


class Articles(database.Model):
    __tablename__ = 'Articles'
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(300), nullable=False)
    text = database.Column(database.Text, nullable=False)
    cover = database.Column(database.Text, nullable=False)
    file = database.Column(database.Text, nullable=False)
    publication_date = database.Column(database.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Articles %r' % self.id


class Data_users(database.Model):
    __tablename__ = 'Data users'
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(300), nullable=False)
    password = database.Column(database.Text, nullable=False)
    publication_date = database.Column(database.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Data_users %r' % self.id


flag = False


@main.route("/", methods=["POST", "GET"])
def home():
    return render_template("/index.html")


@main.route("/main_page", methods=["POST", "GET"])
def books():
    articles = Articles.query.all()
    return render_template('main_page.html', articles=articles)


@main.route("/admin")
def admin_page():
    return render_template("/admin.html")


@main.route("/admin", methods=['post', 'get'])
def admin_data_for_login():
    global flag
    if request.method == 'POST':
        admin_name = request.form.get('admin_name')
        admin_password = request.form.get('admin_password')
        if admin_name == 's' and admin_password == 's':
            flag = True
            return redirect("/")
        else:
            return "Отправляйся в изгнание странник"


@main.route("/new_book", methods=['POST', 'GET'])
def create_article():
    global flag
    if flag:
        if request.method == 'POST':
            title = request.form.get('title')
            text = request.form.get('text')
            img = request.files['cover_book']
            file = request.files['file']
            file.filename = title + '.' + 'pdf'
            img.filename = title + '.' + 'png'
            article = Articles(title=title, text=text,
                              cover=os.path.join("http://127.0.0.1:8000/covers", img.filename),
                              file=os.path.join("http://127.0.0.1:8000/libary", file.filename))
            database.session.add(article)
            database.session.commit()
            if file:
                main.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_FOR_FILES
                file.save(os.path.join(main.config['UPLOAD_FOLDER'], file.filename))
                main.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_FOR_IMAGES
                img.save(os.path.join(main.config['UPLOAD_FOLDER'], img.filename))

                return redirect('/main_page')
            else:
                return redirect('/new_book')
        else:
            return render_template("/new_book.html")
    else:
        return redirect("/")


@main.route("/reg_page")
def reg_page():
    return render_template("/register.html")


@main.route("/reg_page", methods=['POST', 'GET'])
def create_new_user():
    if request.method == 'POST':
        if len(request.form['password']) > 4 and len(request.form['email']) > 4:
            email = request.form['email']
            psw = request.form['password']
            hash_password = generate_password_hash(psw)
            user = Data_users(email=email, password=hash_password)
            os.session.add(user)
            os.session.commit()
            return redirect("/")
        else:
            return redirect("/")
    else:
        redirect("/")


@main.route("/aut_page")
def aut_page():
    return render_template("/authorization.html")


@main.route("/authorization", methods=['POST'])
def authorization_user():
    email = request.form['email']
    password = request.form['password']
    if len(email) > 4 and len(password) > 4:
        for el_e in Data_users.email:
            if el_e == email:
                for el_p in Data_users.password:
                    if el_p == check_password_hash(password):
                        return redirect("/")

    else:
        return "Всо сломалось"


if __name__ == "__main__":
    main.run(debug=True)
