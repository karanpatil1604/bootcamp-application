from flask import Blueprint, request, render_template, redirect, flash, url_for
from sqlalchemy.exc import NoResultFound

from app.db import db
from app.models import Section
from app.bp.users import login_required


bp = Blueprint("section", __name__, url_prefix="")


@bp.route("/sections")
@login_required("admin")
def list_sections():
    # if sesssion role is admin
    # otherwise redirct with flash need to login as admin
    sections = Section.query.all()
    return render_template("sections/list.html", sections=sections)


@bp.route("/sections/<section_id>", methods=["GET", "POST"])
def retrieve_section(section_id):
    if request.method == "GET":
        section = Section.query.get(section_id)
        return render_template("sections/section_details.html", section=section)


@bp.route("/sections/create", methods=["GET", "POST"])
# @login_required("admin")
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
        return redirect(url_for("section.list_sections"))


@bp.route("/sections/update/<section_id>", methods=["GET", "POST"])
def update_section(section_id):
    section = Section.query.get(section_id)
    if request.method == "GET":
        if not section_id:
            flash("Can't find the section with given section id", "warning")
            return redirect(url_for("section.list_sections"))
        return render_template("sections/update.html", section=section)
    elif request.method == "POST":
        new_section_name = request.form.get("section-name")
        if new_section_name:
            section.section_name = new_section_name
            db.session.add(section)
            db.session.commit()
        flash("Section updated successfully", "success")
        return redirect(url_for("section.list_sections"))


@bp.route("/sections/delete/<section_id>", methods=["GET", "POST"])
def delete_section(section_id):
    section = Section.query.get(section_id)
    if request.method == "GET":
        return render_template("sections/confirm_delete.html", section=section)
    elif request.method == "POST":
        db.session.delete(section)
        db.session.commit()
        flash("Section deleted successfully", "warning")
        return redirect(url_for("section.list_sections"))
