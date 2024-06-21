from flask import Blueprint, request, render_template, redirect, flash, url_for
from sqlalchemy.exc import NoResultFound

from app.db import db
from app.models import User

bp = Blueprint("user", __name__, url_prefix="")


@bp.route("/register", methods=["GET", "POST"])
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


@bp.route("/login", methods=["GET", "POST"])
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
@bp.route("/users", methods=["GET", "POST"])
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
