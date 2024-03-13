from flask import Flask

from thesis_backend.api import azure_openai

app = Flask(__name__)
app.config["DEBUG"] = True

# Register blueprints
app.register_blueprint(azure_openai.bp)


@app.route("/", methods=["GET"])
def home():
    return """<h1>Hello World!</h1>"""


@app.after_request
def add_header(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
