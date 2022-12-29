import os
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from app.extensions import db,login_manager, csrf
from .conf import app_conf, blueprints, BASE_DIR


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_conf[config_name])
    if app.debug:
        configure_error_handler(app)
    db.init_app(app)
    init_auth(app)
    # file_storage.init_app(app)

    init_blueprints(app)
    if app.debug:
        DebugToolbarExtension(app)

    return app

def init_blueprints(app):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def init_auth(app):
    from app import auth
    login_manager.init_app(app)
    login_manager.user_loader(auth.load_user)
    login_manager.login_view = "account.login"


def configure_error_handler(app):
   
    from .error_pages import page_not_found, access_forbidden, server_error
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(403, access_forbidden)
    app.register_error_handler(500, server_error)