import json
import os
from typing import Iterable

from openai import AzureOpenAI
from openai.types.chat import ChatCompletionMessageParam

azure_client = AzureOpenAI(
    azure_endpoint="https://mirrorverse.openai.azure.com/",
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-15-preview",
)


def generate_function_call(
    model: str,
    messages: Iterable[ChatCompletionMessageParam],
    functions: list[dict],
    tool_choice: dict,
) -> dict[str, str]:
    completion = azure_client.chat.completions.create(
        model=model,
        messages=messages,
        tools=functions,
        tool_choice=tool_choice,
    )

    return json.loads(
        completion.choices[0].message.tool_calls[0].function.arguments
    )


def generate_message(
    model: str, messages: Iterable[ChatCompletionMessageParam]
) -> str:
    completion = azure_client.chat.completions.create(
        model=model,
        messages=messages,
    )

    return completion.choices[0].message.content


def generate_image(prompt: str) -> str:
    image_response = azure_client.images.generate(
        model="Dalle3",
        prompt=prompt,
    )

    return image_response.data[0].url
