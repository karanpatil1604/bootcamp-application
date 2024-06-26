from flask import Blueprint, request, render_template, redirect, flash, url_for, session
from sqlalchemy.exc import NoResultFound, IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps


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
        if password:
            password = generate_password_hash(password)
        print(f"username: {username}, password: {password}")
        role = "student"
        # validate the request data for our usage

        # 2. Create an entry to the users table
        try:
            new_user = User(
                username=username, email=email, password=password, role=role
            )
            db.session.add(new_user)
            db.session.commit()
            # if role == 'infuencer':
            # take influencer detailsf rom request
            # make entry to influencersDetails table with the foreign key new_user.id
        except IntegrityError as e:
            flash(f"{str(e)} has occured", "danger")
            return redirect(url_for("user.login"))
        except:
            pass
        # 3. Send appropriate response
        return redirect(url_for("user.login"))


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
            return redirect(url_for("user.login"))
        authenticated = check_password_hash(user.password, password)
        if authenticated:
            session["username"] = user.username
            session["role"] = user.role
            session["email"] = user.email
            # if role is influencer redirect to influencer dashboard
            # otherwise
            return redirect(url_for("homepage"))
        else:
            flash("Password is wrong.", "warning")
            return redirect(url_for("user.login"))


@bp.route("/logout")
def logout():
    session.pop("username")
    session.pop("role")
    session.pop("email")
    return redirect(url_for("homepage"))


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
        return redirect(url_for("user.list_users"))


def login_required(role):
    def decorator(original):
        def wrapper(*args, **kwargs):
            if (
                session.get("username")
                and session.get("email")
                and session.get("role") == role
            ):
                return original(*args, **kwargs)
            else:
                flash(f"You need to login as {role}", "warning")
                return redirect(url_for("user.login"))

        return wrapper

    return decorator
