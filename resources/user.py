from flask import Response, request
from flask_restful import Resource
from models.schema.user import UserSchema
from models.user import UserModel
from marshmallow import ValidationError


user_schema = UserSchema()
users_schema = UserSchema(many=True)

class User (Resource):

    def get(self, name):
        user = UserModel.get_user(name)
        if not user:
            return {
                'message': 'username not exist!'
            }, 403
        return {
            'message': '',
            'user': user_schema.dump(user)
        }
        # return Response(user_schema.dump(user), mimetype="application/json", status=200)

    def put(self, name):
        try:
            result = user_schema.load(request.json)
        except ValidationError as err:
            return err.messages, 422

        user = UserModel.get_user(name)
        if not user:
            return {
                'message': 'username not exist!'
            }, 403
        user.email = result.data['email']
        user.password = result.data['password']
        return {
            'message': 'Update user success',
            'user': user_schema.dump(user)
        }

    def delete(self, name):
        UserModel.delete_user(name)
        return {
            'message': 'Delete done!'
        }


class Users(Resource):
    def get(self):
        return {
            'message': '',
            'users': users_schema.dump(UserModel.get_all_user())
        }

    def post(self):
        try:
            result = user_schema.load(request.json)
        except ValidationError as err:
            return err.messages, 422
            
        user = UserModel(result['name'], result['email'], result['password'])
        user.add_user()
        return {
            'message': 'Insert user success',
            'user': user_schema.dump(user)
        }    