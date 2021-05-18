from marshmallow import validate, Schema, fields


class UserSchema(Schema):
    name = fields.String(required=False)
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=[
                      validate.Length(min=6, max=36)],)