from thesis_backend import azure_openai
from json import dumps, loads
from flask import Flask, jsonify, request
from marshmallow import Schema, fields, ValidationError


app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Hello World!</h1>'''


class AzurePromptSchema(Schema):
    model = fields.Str(required=True)
    messages = fields.List(fields.Dict(), required=True)


class AzureFunctionPromptSchema(AzurePromptSchema):
    functions = fields.List(fields.Dict())
    tool_choice = fields.Dict()


@app.get('/prompt_azure_openai/function')
def prompt_azure_openai_function():
    try:
        request_data = AzureFunctionPromptSchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    completion = azure_openai.get_completion_azure_function(
        model=request_data.get("model"),
        messages=request_data.get("messages"),
        functions=request_data.get("functions"),
        tool_choice=request_data.get("tool_choice")
    )

    return {
        "script": completion["script"],
        "explanation": completion["explanation"]
    }


@app.get('/prompt_azure_openai/message')
def prompt_azure_openai_message():
    try:
        request_data = AzurePromptSchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    response = azure_openai.get_completion_azure_message(
        model=request_data.get("model"),
        messages=request_data.get("messages")
    )

    return {
        "response": response
    }


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
