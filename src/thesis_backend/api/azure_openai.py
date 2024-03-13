from flask import Blueprint, request
from marshmallow import ValidationError

from ..azure_openai_completion import (
    generate_function_call,
    generate_image,
    generate_message,
)
from ..schema import (
    AzureFunctionPromptSchema,
    AzureImagePromptSchema,
    AzureMessagePromptSchema,
)

bp = Blueprint("azure_openai", __name__)


@bp.post("/prompt_azure_openai/function")
def prompt_azure_openai_function():
    try:
        request_data = AzureFunctionPromptSchema().load(request.json)
    except ValidationError as err:
        return {"error": err.normalized_messages()}, 400

    completion = generate_function_call(
        model=request_data.get("model"),
        messages=request_data.get("messages"),
        functions=request_data.get("functions"),
        tool_choice=request_data.get("tool_choice"),
    )

    return completion


@bp.post("/prompt_azure_openai/message")
def prompt_azure_openai_message():
    try:
        request_data = AzureMessagePromptSchema().load(request.json)
    except ValidationError as err:
        return {"error": err.normalized_messages()}, 400

    response = generate_message(
        model=request_data.get("model"), messages=request_data.get("messages")
    )

    return {"response": response}


@bp.post("/prompt_azure_openai/image")
def prompt_azure_openai_image():
    try:
        request_data = AzureImagePromptSchema().load(request.json)
    except ValidationError as err:
        return {"error": err.normalized_messages()}, 400

    url = generate_image(prompt=request_data.get("prompt"))

    return {"url": url}
