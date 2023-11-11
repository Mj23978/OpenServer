from .server.app import app
from .server import *

@app.route("/")
def index():
    return "interference api"


@app.route("/hello/<name>")
def hello(name):
    return f"Hello {name}"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
