# import connexion app & flask app
from app import connexion_app, app

# run application
if __name__ == '__main__':
    connexion_app.run(port=5055, host='0.0.0.0')
