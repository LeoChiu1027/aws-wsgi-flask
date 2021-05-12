from flask import Flask, request
from middleware.loggermiddleware import LoggerMiddleware
from time import strftime


app = Flask(__name__)
app.wsgi_app = LoggerMiddleware(app.wsgi_app)

@app.route("/", methods=['GET'])
def handler():
    return 'hello world'



@app.after_request
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    app.logger.info('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response

if __name__ == '__main__':
    app.run(debug=True)