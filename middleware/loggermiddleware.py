

class LoggerMiddleware(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        print(self)
        print(environ)
        return self.app(environ, start_response)