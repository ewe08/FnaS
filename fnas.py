from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

main = Flask(__name__)
main.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///libary.db'
main.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
libary = SQLAlchemy(main)


class Article(libary.Model):
    id = libary.Column(libary.Integer, primary_key=True)
    title = libary.Column(libary.String(300), nullable=False)
    text = libary.Column(libary.Text, nullable=False)
    publication_date = libary.Column(libary.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Article %r' % self.id


flag = False


@main.route("/")
def home():
    articles = Article.query.order_by(Article.publication_date).all()
    return render_template("/index.html", articles=articles)


@main.route("/admin", methods=['post', 'get'])
def admin_page():
    return render_template("/admin.html")


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


@main.route("/add_in_libary_page", methods=['POST', 'GET'])
def create_article():
    global flag
    if flag:
        if request.method == 'POST':
            title = request.form.get('title')
            text = request.form.get('text')
            article = Article(title=title, text=text)
            libary.session.add(article)
            libary.session.commit()
            return redirect('/')
        else:
            return render_template("add_in_libary_page.html")
    else:
        return redirect("/")


if __name__ == "__main__":
    main.run(debug=True)
