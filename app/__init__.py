import os
import logging
from flask import Flask, redirect, url_for
from app.extensions.db import db
from app.extensions.assets import assets, configure_assets
from app.extensions.toolbar import configure_toolbar

DEFAULT_BLUEPRINTS = [

]

def create_app(config=None, blueprints=None):
    """
    Create and initialise the application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('%s/config/default.py' % app.root_path)

    if config:
        app.config.from_pyfile(config)
    elif os.getenv('FLASK_CONFIG'):
        app.config.from_envvar('FLASK_CONFIG')

    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    configure_logging(app)
    configure_extensions(app)
    configure_context_processors(app)
    configure_assets(app)

    configure_blueprints(app, blueprints)

    @app.route('/')
    def index():
        """
        Placeholder
        """
        return ''

    return app


def configure_extensions(app):
    """
    Set up Flask extensions.
    """
    db.init_app(app)
    assets.init_app(app)
    configure_toolbar(app)


def configure_blueprints(app, blueprints):
    """
    Register blueprints.
    """
    for blueprint in blueprints:
        # Import blueprint from view module
        module = __import__('app.blueprints.%s.views' % blueprint[0], globals(), locals(), '*')
        app.register_blueprint(module.blueprint, url_prefix=blueprint[1])


def configure_context_processors(app):

    @app.context_processor
    def debug(debug=app.debug):
        """
        Notify templates that they're in debug mode
        """
        return dict(debug=debug)


def configure_logging(app):

    if app.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        log_format = logging.Formatter('''
---
Message type:       %(levelname)s
Location:           %(pathname)s:%(lineno)d
Module:             %(module)s
Function:           %(funcName)s
Time:               %(asctime)s

%(message)s

''')

        # Send errors via email
        mail_handler = logging.handlers.SMTPHandler('127.0.0.1', app.config.get('DEFAULT_MAIL_SENDER'), app.config.get('ERROR_EMAIL'), 'Error')
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(log_format)

        # Also continue to log errors to stderr
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_format)

        app.logger.addHandler(stream_handler)
        app.logger.addHandler(mail_handler)
