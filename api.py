from flask import Flask, request
from flask_restful import Api, Resource
from middleware.loggermiddleware import LoggerMiddleware
from time import strftime
from resources.user import User, Users

class PrintHelloWorld(Resource):
    def get(self):
        return {
            'message': 'Hello Wrold!'
        }, 200


app = Flask(__name__)
api = Api(app)
# app.wsgi_app = LoggerMiddleware(app.wsgi_app)

api.add_resource(PrintHelloWorld, "/print_hello_world/")
api.add_resource(User, "/user/<string:name>")
api.add_resource(Users, "/users/")

@app.route("/", methods=['GET'])
def handler():
    return 'hello world'



@app.after_request
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    app.logger.info('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response

if __name__ == '__main__':
    from common.ma import ma
    ma.init_app(app)
    app.run(debug=True)