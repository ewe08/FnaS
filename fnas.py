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


@main.route("/main_page")
def main_page():
    articles = Article.query.order_by(Article.publication_date).all()
    return render_template("/main_page.html", articles=articles)


@main.route("/admin")
def admin_page():
    return render_template("/admin.html")


flag = False


@main.route("/admin", methods=['post', 'get'])
def admin_data_for_login():
    global flag
    if request.method == 'POST':
        admin_name = request.form.get('admin_name')
        admin_password = request.form.get('admin_password')
        if admin_name == 's' and admin_password == 's':
            flag = True
            return redirect("/main_page")
        else:
            return "Отправляйся в изгнание странник"


@main.route("/add_in_libary_page", methods=['POST', 'GET'])
def create_article():
    global flag
    if flag == True:
        if request.method == 'POST':
            title = request.form.get('title')
            text = request.form.get('text')
            button_flag = request.form.get('exit_button')
            if button_flag:
                flag = False
                return redirect("/main_page")
            else:
                article = Article(title=title, text=text)
                libary.session.add(article)
                libary.session.commit()
                return redirect('/main_page')
        else:
            return render_template("add_in_libary_page.html")
    else:
        return redirect("/main_page")


if __name__ == "__main__":
    main.run(debug=True)
