import os
from flask import Flask
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_security import Security, SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore
from application.models import User, Role, user_datastore

#import logging
#logging.basicConfig(filename='debug.log', level=logging.DEBUG,
 #          format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development") == "production":
      raise Exception("Currently no production config is setup.")
    else:
      print("Staring Local Development")
      app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    app.secret_key = 'xyz'
    security = Security(app, user_datastore)
    return app

app = create_app()

# Import all the controllers so they are loaded
from application.controllers import *

@app.errorhandler(404)
def page_not_found(e):
    #note that we set the 404 status explicitly
    return render_template('404.html'), 404

if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0',port=8080)
