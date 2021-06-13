from flask import Flask
from flask_bootstrap import Bootstrap
from config import config_options
from flask_sqlalchemy import SQLAlchemy

#Initializong FLask extensions
bootstrap = Bootstrap()
db = SQLAlchemy()

def create_app(config_name):

  #Initializing the application
  app = Flask(__name__)

  # Setting up configuration
  app.config.from_object(config_options[config_name])
  # Initializing flask extensions
  bootstrap.init_app(app)
  db.init_app(app)

  #Registering the blue print
  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint)

  # setting config
  from .requests import configure_request
  configure_request(app)

  return app

