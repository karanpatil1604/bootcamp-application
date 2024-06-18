from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import NoResultFound
from db import db
from models import User, Book, Section

app = Flask(__name__)


app.config["SECRET_KEY"] = "some_secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
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


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("users/register.html")
    elif request.method == "POST":
        # 1. Validate and get request data
        username = request.form.get("username")  # None if no key named 'username'

        email = request.form.get("email")
        password = request.form.get("password")
        print(f"username: {username}, password: {password}")
        role = "student"
        # validate the request data for our usage

        # 2. Create an entry to the users table
        new_user = User(username=username, email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        # 3. Send appropriate response
        return redirect(url_for("login"))


def check_password(user_password, password):
    return user_password == password


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("users/login.html")
    elif request.method == "POST":
        # 1. Validate and get request data
        username = request.form.get("username")  # None if no key named 'username'
        password = request.form.get("password")
        print(f"username: {username}, password: {password}")
        # validate the request data for our usage

        # 2. fetch details for the username
        try:
            user = User.query.filter_by(username=username).one()
        except NoResultFound as e:
            flash("User with this username not found.", "warning")
            return redirect(url_for("login"))
        authenticated = check_password(user.password, password)
        if authenticated:
            return redirect(url_for("homepage"))
        else:
            flash("Password is wrong.", "warning")
            return redirect(url_for("login"))


# List - (We are getting an HTTP GET request to this endpoint)
@app.route("/users", methods=["GET", "POST"])
def list_users():
    if request.method == "GET":
        users = User.query.all()
        return render_template("user_list.html", users=users)
    elif request.method == "POST":
        # 1. Validate and get request data
        username = request.form.get("username")  # None if no key named 'username'
        email = request.form.get("email")
        password = request.form.get("password")
        print(f"username: {username}, password: {password}")
        role = "student"
        # validate the request data for our usage

        # 2. Create an entry to the users table
        new_user = User(username=username, email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        # 3. Send appropriate response
        return redirect(url_for("list_users"))


@app.route("/sections")
def list_sections():
    sections = Section.query.all()
    return render_template("sections/list.html", sections=sections)


@app.route("/sections/create", methods=["GET", "POST"])
def create_section():
    if request.method == "GET":
        return render_template("sections/create.html")
    elif request.method == "POST":
        section_name = request.form.get("section-name")
        if section_name:
            new_section = Section(section_name=section_name)
            db.session.add(new_section)
            db.session.commit()
            flash("Section created succesfully", "success")
        return redirect(url_for("list_sections"))


@app.route("/sections/update/<section_id>", methods=["GET", "POST"])
def update_section(section_id):
    section = Section.query.get(section_id)
    if request.method == "GET":
        if not section_id:
            flash("Can't find the section with given section id", "warning")
            return redirect(url_for("list_sections"))
        return render_template("sections/update.html", section=section)
    elif request.method == "POST":
        new_section_name = request.form.get("section-name")
        if new_section_name:
            section.section_name = new_section_name
            db.session.add(section)
            db.session.commit()
        flash("Section updated successfully", "success")
        return redirect(url_for("list_sections"))


@app.route("/sections/delete/<section_id>", methods=["GET", "POST"])
def delete_section(section_id):
    section = Section.query.get(section_id)
    if request.method == "GET":
        return render_template("sections/confirm_delete.html", section=section)
    elif request.method == "POST":
        db.session.delete(section)
        db.session.commit()
        flash("Section deleted successfully", "warning")
        return redirect(url_for("list_sections"))


@app.route("/create_tables")
def create_tables():
    with app.app_context():
        db.create_all()
    return "Tables created succesfully"


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
