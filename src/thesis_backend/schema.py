from marshmallow import Schema, fields, validate


class AzureImagePromptSchema(Schema):
    prompt = fields.Str(required=True)


class AzureMessagePromptSchema(Schema):
    model = fields.Str(required=True)
    messages = fields.List(fields.Dict(), required=True)


class AzureFunctionPromptSchema(AzureMessagePromptSchema):
    functions = fields.List(fields.Dict())
    tool_choice = fields.Dict()


class AzureVideoIndexerIndexSchema(Schema):
    url = fields.Str(required=True)
    name = fields.Str(required=True)


class AzureVideoIndexerStatusSchema(Schema):
    urls = fields.List(fields.Str(required=True), required=True)


class SearchedVideoSchema(Schema):
    url = fields.Str(required=True)
    start = fields.Float(required=True)
    end = fields.Float(required=True)


class AzureVideoIndexerSearchSchema(Schema):
    query = fields.Str(required=True)
    videos = fields.List(fields.Nested(SearchedVideoSchema()), required=True, validate=validate.Length(min=1))
