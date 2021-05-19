from flask import Flask, request
from flask_restful import Api
from middleware.loggermiddleware import LoggerMiddleware
from time import strftime
from common.db import db
from common.ma import ma
from resources.routes import initialize_routes
import os


app = Flask(__name__)
api = Api(app)

app.logger.info('environment:%s', os.environ.get('FLASK_ENV').capitalize())
# app.wsgi_app = LoggerMiddleware(app.wsgi_app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config.from_object('config.'+os.environ.get('FLASK_ENV').capitalize())
db.init_app(app)
ma.init_app(app)
initialize_routes(api)
app.run(debug=True)


@app.after_request
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    app.logger.info('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response
