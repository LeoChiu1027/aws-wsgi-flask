from flask_restful import Resource, reqparse 
from models.schema.user_schema import UserSchema
from flask import request

users = [{
    'name': 'kirai',
}]

user_schema = UserSchema()

class User (Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True, help='Email is required')
    parser.add_argument('password', required=True, help='Password is required')

    def get(self, name):
        find = [item for item in users if item['name'] == name]
        if len(find) == 0:
            return {
                'message': 'username not exist!'
            }, 403
        user = find[0]
        if not user:
            return {
                'message': 'username not exist!'
            }, 403
        return {
            'message': '',
            'user': user
        }

    def post(self, name):
        json_data = request.json
        result = user_schema.load(json_data)

        if len(result.errors) > 0:
            return result.errors, 433

        user = {
            'name': name,
            'email': result.data['email'],
            'password': result.data['password']
        }
        global users
        users.append(user)
        return {
            'message': 'Insert user success',
            'user': user
        }

    def put(self, name):
        arg = self.parser.parse_args()
        find = [item for item in users if item['name'] == name]
        if len(find) == 0:
            return {
                'message': 'username not exist!'
            }, 403
        user = find[0]
        user['email'] = arg['email']
        user['password'] = arg['password']
        return {
            'message': 'Update user success',
            'user': user
        }

    def delete(self, name):
        global users
        users = [item for item in users if item['name'] != name]
        return {
            'message': 'Delete done!'
        }


class Users(Resource):
    def get(self):
        return {
            'message': '',
            'users': users
        }