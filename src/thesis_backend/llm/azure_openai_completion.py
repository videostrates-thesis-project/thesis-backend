import json
import os
from typing import Iterable

from openai import AzureOpenAI
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionToolChoiceOptionParam,
    ChatCompletionToolParam,
)

if "AZURE_OPENAI_KEY" not in os.environ:
    raise ValueError(
        "Azure OpenAI key not found in environment. "
        "Please set it in the environment variable AZURE_OPENAI_KEY"
    )

azure_client = AzureOpenAI(
    azure_endpoint="https://mirrorverse.openai.azure.com/",
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-15-preview",
)


def generate_function_call(
    model: str,
    messages: Iterable[ChatCompletionMessageParam],
    functions: Iterable[ChatCompletionToolParam],
    tool_choice: ChatCompletionToolChoiceOptionParam,
) -> dict[str, str]:
    completion = azure_client.chat.completions.create(
        model=model,
        messages=messages,
        tools=functions,
        tool_choice=tool_choice,
        temperature=0.25,
    )

    tool_calls = completion.choices[0].message.tool_calls

    if tool_calls is None:
        raise ValueError("No tool calls found in completion")

    return json.loads(tool_calls[0].function.arguments)


def generate_message(
    model: str, messages: Iterable[ChatCompletionMessageParam]
) -> str:
    completion = azure_client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.25,
    )

    response = completion.choices[0].message.content

    return response if response else ""


def generate_image(prompt: str) -> str:
    image_response = azure_client.images.generate(
        model="Dalle3",
        prompt=prompt,
        size="1792x1024",
        quality="hd",
        response_format="url",
    )

    url = image_response.data[0].url

    return url if url else ""
