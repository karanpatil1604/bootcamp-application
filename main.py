from flask import Flask, render_template


app = Flask(__name__)


# http://localhost:8000/
@app.route("/")
def hello():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
