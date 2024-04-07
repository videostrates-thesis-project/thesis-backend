from flask import Blueprint

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
from ..utils.with_request_data import with_request_data

bp = Blueprint("azure_openai", __name__)


@bp.post("/prompt_azure_openai/function")
@with_request_data(AzureFunctionPromptSchema())
def prompt_azure_openai_function(request_data) -> tuple[dict[str, str], int]:
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
@with_request_data(AzureMessagePromptSchema())
def prompt_azure_openai_message(request_data) -> tuple[dict[str, str], int]:
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
@with_request_data(AzureImagePromptSchema())
def prompt_azure_openai_image(request_data) -> tuple[dict[str, str], int]:
    url = generate_image(prompt=request_data.get("prompt"))

    return {"url": url}, 200
