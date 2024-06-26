from flask import Blueprint, request, render_template, url_for, redirect

from app.db import db
from app.models import Book, Section

bp = Blueprint("book", __name__, url_prefix="")

# @bp.route("/books")
# def list_books


@bp.route("/books/create", methods=["GET", "POST"])
# @login_required("admin")
def create_section():
    if request.method == "GET":
        sections = Section.query.all()
        return render_template("books/create.html", sections=sections)
    elif request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        author = request.form.get("author")
        content = request.form.get("content")
        section_id = request.form.get("section_id")
        new_book = Book(
            title=title,
            description=description,
            author=author,
            content=content,
            section_id=section_id,
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("homepage"))
