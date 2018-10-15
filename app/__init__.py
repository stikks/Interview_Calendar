from flask import jsonify

# Import Migrate
from flask_migrate import Migrate

# Import CORS
from flask_cors import CORS

# Import connexion module to use swagger specification
import connexion
from connexion.api import *

import config
from services.common import InvalidUsage
from . import forms

"""
Initialize the flask application
Appropriately name the application
Read application config from config.py
Read the api.yaml file to configure the endpoints
"""
connexion_app = connexion.App('interview_api', template_folder="templates", static_folder='static',
                              specification_dir="./")

with connexion_app.app.app_context():
    connexion_app.app.config.from_object(config)
    connexion_app.add_api('api.yaml')

    # Define the WSGI application object
    app = connexion_app.app

    from . import models

    # initialize migrate to manage db migrations
    migrate = Migrate(app, models.db)

    # initialize cors
    CORS(app)

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response