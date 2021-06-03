from .user import User, Users, UserToken


def initialize_routes(api):
    api.add_resource(Users, '/users')
    api.add_resource(User, '/user/<name>')
    api.add_resource(UserToken, '/userToken')