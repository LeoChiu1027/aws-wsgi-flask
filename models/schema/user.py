from marshmallow import validate, Schema, fields
from common.ma import ma
from models.user import UserModel

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
    name = fields.String(required=False)
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=[
                      validate.Length(min=6, max=36)],)


class UserTokenSchema(ma.SQLAlchemyAutoSchema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=[
                      validate.Length(min=6, max=36)],)