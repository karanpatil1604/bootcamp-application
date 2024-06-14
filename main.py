from flask import Flask, render_template
from db import db
from models import User

app = Flask(__name__)

books = [
    {"book_title": "book 1", "author": "author 1"},
    {"book_title": "book 2", "author": "author 1"},
    {"book_title": "book 3", "author": "author 2"},
]

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


# http://localhost:8000/
@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/books")
def book_list():
    return render_template("book_list.html", books=books)


@app.route("/users")
def list_users():
    users = User.query.all()
    return render_template("user_list.html", users=users)


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    app.run(host="localhost", port=8000, debug=True)
