from marshmallow import Schema, fields


class AzureImagePromptSchema(Schema):
    prompt = fields.Str(required=True)


class AzureMessagePromptSchema(Schema):
    model = fields.Str(required=True)
    messages = fields.List(fields.Dict(), required=True)


class AzureFunctionPromptSchema(AzureMessagePromptSchema):
    functions = fields.List(fields.Dict())
    tool_choice = fields.Dict()
