import json
import os
from openai import AzureOpenAI


azure_client = AzureOpenAI(
  azure_endpoint="https://mirrorverse.openai.azure.com/",
  api_key=os.getenv("AZURE_OPENAI_KEY"),
  api_version="2024-02-15-preview"
)


def get_completion_azure_function(
    model: str,
    messages: json,
    functions: json,
    tool_choice: json
) -> dict[str, str]:
    completion = azure_client.chat.completions.create(
        model=model,
        messages=messages,
        tools=functions,
        tool_choice=tool_choice,
    )

    return json.loads(completion.choices[0].message.tool_calls[0].function.arguments)


def get_completion_azure_message(
    model: str,
    messages: json
) -> str:
    print("model: ", model)
    print("messages: ", messages)

    completion = azure_client.chat.completions.create(
        model=model,
        messages=messages,
    )

    return completion.choices[0].message.content

