import os
from flask import (
    Flask, request, render_template
)
import connexion

import config

"""
Initialize the flask application
Appropriately name the application
Read application config from config.py
Read the api.yaml file to configure the endpoints
"""
connexion_app = connexion.App('interview_api', template_folder="templates", specification_dir="./")
connexion_app.app.config.from_object(config)
connexion_app.add_api('api.yaml')


if __name__ == '__main__':
    connexion_app.run()
