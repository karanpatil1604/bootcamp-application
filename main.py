from flask import Flask, render_template


app = Flask(__name__)

books = [
    {"book_title": "book 1", "author": "author 1"},
    {"book_title": "book 2", "author": "author 1"},
    {"book_title": "book 3", "author": "author 2"},
]


# http://localhost:8000/
@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/books")
def book_list():
    book = {"book_title": "book 1", "author": "author 1"}
    return render_template("book_list.html", instance=book)


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
