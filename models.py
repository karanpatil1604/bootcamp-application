from db import db


class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    role = db.Column(db.String)


class Book(db.Model):
    __tablename__ = "books"
    book_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    content = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    section = db.Column(db.String, nullable=True)
    # pages
    # thumbnail
    section_id = db.Column(
        db.Integer, db.ForeignKey("sections.section_id"), nullable=True
    )


class Section(db.Model):
    __tablename__ = "sections"
    section_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    section_name = db.Column(db.String)
    books = db.relationship("Book", backref="books", lazy=True)
