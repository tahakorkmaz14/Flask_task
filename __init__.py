from .app.routes import site
from .api.routes import api
from flask import Flask
import logging


# log file
logging.basicConfig(filename='app.log',
                    level=logging.DEBUG)

# initialization of the general app


def create_app():
    app = Flask(__name__)

    app.register_blueprint(api)
    app.register_blueprint(site)

    return app
