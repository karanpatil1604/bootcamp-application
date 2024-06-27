from flask import Blueprint, url_for, redirect, render_template, request, session, flash


from app.db import db
from app.models import BookIssue
from app.bp.users import login_required


bp = Blueprint("book_issue", __name__, url_prefix="")


@bp.route("/issue/<book_id>", methods=["GET", "POST"])
# @login_required("student")
def issue_request(book_id):
    if request.method == "GET":
        print("get request is coming.")
    if request.method == "POST":
        user_id = session.get("user_id")
        role = session.get("role")
        print("Handling post request")
        if user_id and role == "student":
            new_issue = BookIssue(user_id=user_id, book_id=book_id)
            db.session.add(new_issue)
            db.session.commit()
            flash("Request to issue book is submitted", "success")
            return redirect(url_for("homepage"))
        else:
            flash("You need to login as student to request the book", "warning")
            return redirect(url_for("user.login"))


@bp.route("/issues", methods=["GET", "POST"])
@login_required("admin")
def issues():
    all_issues = BookIssue.query.all()
    return render_template("issues/issues.html", issues=all_issues)


@bp.route("/my-issues", methods=["GET", "POST"])
@login_required("student")
def my_issues():
    user_id = session.get("user_id")
    my_issues = BookIssue.query.filter_by(user_id=user_id)
    return render_template("issues/issues.html", issues=my_issues)
