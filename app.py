from flask import Flask, request
from flask_restful import Api
from middleware.loggermiddleware import LoggerMiddleware
from time import strftime
from common.db import db
from common.ma import ma
from resources.user import Users, User


app = Flask(__name__)
api = Api(app)

api.add_resource(Users, '/users')
api.add_resource(User, '/user/<name>')

# app.wsgi_app = LoggerMiddleware(app.wsgi_app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db.init_app(app)
ma.init_app(app)
# initialize_routes(api)



@app.after_request
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    app.logger.info('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response

if __name__ == '__main__':
    app.run(debug=True)