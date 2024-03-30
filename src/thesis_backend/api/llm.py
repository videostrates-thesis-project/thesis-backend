from flask import Blueprint, request
from marshmallow import ValidationError
import json

from src.thesis_backend.llm.azure_openai_completion import (
    generate_function_call,
    generate_image,
    generate_message,
)
from src.thesis_backend.llm.gemini_completion import (
    gemini_generate_message, gemini_generate_function_call
)
from ..schema import (
    AzureFunctionPromptSchema,
    AzureImagePromptSchema,
    AzureMessagePromptSchema,
)

bp = Blueprint("azure_openai", __name__)


@bp.post("/prompt_azure_openai/function")
def prompt_azure_openai_function() -> tuple[dict[str, str], int]:
    try:
        request_data = AzureFunctionPromptSchema().load(request.get_json())
    except ValidationError as err:
        return {"error": err.normalized_messages()}, 400

    model = request_data.get("model")

    if "gemini" in model:
        completion_fn = gemini_generate_function_call
        print("using gemini")
    else:
        print("using azure openai")
        completion_fn = generate_function_call

    # save messages to latest-prompt.txt
    with open("latest-prompt.txt", "w", encoding="utf-8") as f:
        f.write(request_data.get("messages")[-1]["content"])

    completion = completion_fn(
        model=model,
        messages=request_data.get("messages"),
        functions=request_data.get("functions"),
        tool_choice=request_data.get("tool_choice"),
    )

    return completion, 200


@bp.post("/prompt_azure_openai/message")
def prompt_azure_openai_message() -> tuple[dict[str, str], int]:
    try:
        request_data = AzureMessagePromptSchema().load(request.get_json())
    except ValidationError as err:
        return {"error": err.normalized_messages()}, 400

    model = request_data.get("model")
    if "gemini" in model:
        completion_fn = gemini_generate_message
        print("using gemini")
    else:
        completion_fn = generate_message
        print("using azure openai")

    response = completion_fn(
        model=request_data.get("model"), messages=request_data.get("messages")
    )

    return {"response": response}, 200


@bp.post("/prompt_azure_openai/image")
def prompt_azure_openai_image() -> tuple[dict[str, str], int]:
    try:
        request_data = AzureImagePromptSchema().load(request.get_json())
    except ValidationError as err:
        return {"error": err.normalized_messages()}, 400

    url = generate_image(prompt=request_data.get("prompt"))

    return {"url": url}, 200
