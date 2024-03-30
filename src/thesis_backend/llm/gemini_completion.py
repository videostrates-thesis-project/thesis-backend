import os

import vertexai
from vertexai.generative_models import GenerativeModel
from vertexai.generative_models import FunctionDeclaration, Tool

from google.auth import credentials as auth_credentials
from vertexai.generative_models import Content, Part


class MyCredentials(auth_credentials.Credentials):
    def __init__(self, token: str) -> None:
        super().__init__()
        self.token = token

    def refresh(self, request) -> None:
        pass


token = os.getenv("GEMINI_TOKEN")

if not token:
    raise ValueError("Please set the GEMINI_TOKEN environment variable")

gemini_project = os.getenv("GEMINI_PROJECT")

if not gemini_project:
    raise ValueError("Please set the GEMINI_PROJECT environment variable")

cred = MyCredentials(token)

vertexai.init(project=gemini_project, credentials=cred)


def transform_function_call_dict(function_call_dict: list[dict]) -> list[FunctionDeclaration]:
    functions = []
    for function in function_call_dict:
        functions.append(
            FunctionDeclaration(
                name=function["function"]["name"],
                description=function["function"]["description"],
                parameters=function["function"]["parameters"]
            )
        )

    return functions


def transform_messages_dict(messages_dict: list[dict]) -> list[Content]:
    messages = []
    previous_role = None
    current_msg = None
    for message in messages_dict:
        role = message["role"]

        if role == "system":
            content = f"---SYSTEM INSTRUCTIONS--- \n{message['content']}\n---END OF SYSTEM INSTRUCTIONS---"
        else:
            content = message["content"]

        if role == "system":
            role = "user"
        if role == "assistant":
            role = "model"

        if role == previous_role:
            current_msg += "\n\n" + content
        elif previous_role is None:
            current_msg = content
        else:
            messages.append(Content(role=previous_role, parts=[Part.from_text(current_msg)]))
            current_msg = content

        previous_role = role

    if current_msg:
        messages.append(Content(role=previous_role, parts=[Part.from_text(current_msg)]))

    return messages


def gemini_generate_message(model: str, messages: list[dict]) -> str:
    model = GenerativeModel(model_name=model)
    messages_transformed = transform_messages_dict(messages)
    response = model.generate_content(messages_transformed)
    return response.candidates[0].content.parts[0].text


def gemini_generate_function_call(
    model: str, messages: list[dict], functions: list[dict], tool_choice
) -> str:
    gemini_model = GenerativeModel(model_name=model)
    messages_transformed = transform_messages_dict(messages)
    tools = [
        Tool(function_declarations=transform_function_call_dict(functions))
    ]
    response = gemini_model.generate_content(messages_transformed, tools=tools)

    result_args = response.candidates[0].content.parts[0].function_call.args

    args_map = {
        key: result_args[key] for key in result_args
    }

    return args_map
