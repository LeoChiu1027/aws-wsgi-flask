from flask import request
from flask_restful import Resource
from models.schema.user import UserSchema, UserTokenSchema
from models.user import UserModel
from marshmallow import ValidationError
from datetime import datetime, timedelta
import jwt

user_schema = UserSchema()
users_schema = UserSchema(many=True)
userToken_schmea = UserTokenSchema()

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 600

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
        user.email = result['email']
        user.password = result['password']
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


class UserToken(Resource):
    def post(self):
        try:
            result = userToken_schmea.load(request.json)
        except ValidationError as err:
            return err.messages, 422
            
        try:
            user = UserModel.get_user_by_email(result['email'])
            user.match_password(result['password'])
        except (UserModel.DoesNotExist, UserModel.PasswordDoesNotMatch):
            return {'message': 'Wrong credentials'}, 400            

        payload = {
            'user_id': user.email,
            'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
        }

        jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
        print(jwt_token)
        decodedPayload = jwt.decode(jwt_token, JWT_SECRET,
                        algorithms=[JWT_ALGORITHM])
        print(decodedPayload)
        return {'token': jwt_token}
        
