from flask import Flask


app = Flask(__name__)


# http://localhost:8000/
@app.route("/")
def hello():
    return "<h1>Hello world</h1>"


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
