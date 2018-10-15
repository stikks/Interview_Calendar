# import subprocess
from subprocess import Popen, PIPE

# import connexion app & flask app
from app import connexion_app, app

# create database and run migrations
Popen("flask db init && flask db migrate && flask db upgrade", shell=True, stdout=PIPE).stdout.read()

# run application
if __name__ == '__main__':
    connexion_app.run(port=5055, host='0.0.0.0')
