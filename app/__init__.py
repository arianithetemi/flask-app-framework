from flask import Flask
import os
import ConfigParser
from logging.handlers import RotatingFileHandler
from flask.ext.cors import CORS
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy
db = SQLAlchemy();

def create_app():
    # Here we  create flask instance
    app = Flask(__name__)

    # Allow cross-domain access to API.
    #cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Load application configurations
    load_config(app)

    # Configure logging.
    configure_logging(app)

    # Initialize SQLAlchemy
    db.init_app(app)

    # Init modules
    init_modules(app)

    return app


def load_config(app):
    ''' Reads the config file and loads configuration properties into the Flask app.
    :param app: The Flask app object.
    '''
    # Get the path to the application directory, that's where the config file resides.
    par_dir = os.path.join(__file__, os.pardir)
    par_dir_abs_path = os.path.abspath(par_dir)
    app_dir = os.path.dirname(par_dir_abs_path)

    # Read config file
    config = ConfigParser.RawConfigParser()
    config_filepath = app_dir + '/config.cfg'

    # Testing app config
    testapp_config_filepath = app_dir + '/test_app_config.cfg'

    # Checking if config.cfg file exists
    if os.path.isfile(config_filepath):
        config.read(config_filepath)
        app.config['SERVER_PORT'] = config.get('Application', 'SERVER_PORT')
        app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLAlchemy', 'SQLALCHEMY_DATABASE_URI')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        log_path = config.get('Logging', 'PATH')
    else:
        config.read(testapp_config_filepath)
        app.config['SERVER_PORT'] = config.get('Application', 'SERVER_PORT')
        app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLAlchemy', 'SQLALCHEMY_DATABASE_URI')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        log_path = config.get('Logging', 'PATH')

    # Logging path might be relative or starts from the root.
    # If it's relative then be sure to prepend the path with the application's root directory path.
    if log_path.startswith('/'):
        app.config['LOG_PATH'] = log_path
    else:
        app.config['LOG_PATH'] = app_dir + '/' + log_path

    app.config['LOG_LEVEL'] = config.get('Logging', 'LEVEL').upper()


def configure_logging(app):
    ''' Configure the app's logging.
     param app: The Flask app object
    '''

    log_path = app.config['LOG_PATH']
    log_level = app.config['LOG_LEVEL']

    # If path directory doesn't exist, create it.
    log_dir = os.path.dirname(log_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create and register the log file handler.
    log_handler = RotatingFileHandler(log_path, maxBytes=250000, backupCount=5)
    log_handler.setLevel(log_level)
    app.logger.addHandler(log_handler)

    # First log informs where we are logging to.
    # Bit silly but serves  as a confirmation that logging works.
    app.logger.info('Logging to: %s', log_path)


def init_modules(app):

    # Import blueprint modules
    from app.mod_main.views import mod_main
    from app.mod_api.views import mod_api

    app.register_blueprint(mod_main)
    app.register_blueprint(mod_api)
