from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import NoResultFound

from app.config import LocalConfig
from app.db import db
from app.models import User, Book, Section

from app.bp.users import bp as user_bp
from app.bp.sections import bp as section_bp

app = Flask(__name__)

app.config.from_object(LocalConfig)

db.init_app(app)


# http://localhost:8000/
@app.route("/")
def homepage():
    if request.method == "GET":
        search = request.args.get("search")
        if search:
            books = Book.query.filter_by(title=search)
        else:
            books = Book.query.all()
    return render_template("homepage.html", books=books)


@app.route("/create_tables")
def create_tables():
    with app.app_context():
        db.create_all()
    return "Tables created succesfully"


app.register_blueprint(user_bp)
app.register_blueprint(section_bp)

if __name__ == "__main__":
    app.run(host="localhost", port=8000)
