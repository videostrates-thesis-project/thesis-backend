import os

import flask
from flask import Flask
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))

from thesis_backend.api import llm

app = Flask(__name__)
app.config["DEBUG"] = True

# Register blueprints
app.register_blueprint(llm.bp)


@app.route("/", methods=["GET"])
def home() -> str:
    return """<h1>Hello World!</h1>"""


@app.after_request
def add_header(response: flask.Response) -> flask.Response:
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
