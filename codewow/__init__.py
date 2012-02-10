# coding: utf-8

from flask import Flask
from flaskext.mongoalchemy import MongoAlchemy

from codewow.apps import home

# configure
DEFAULT_APP_NAME = 'codewow'

DEFAULT_MODULES = (
    ("", home),
)

db = MongoAlchemy()

# actions
def create_app(config=None, app_name=None, modules=None):

    if app_name is None:
        app_name = DEFAULT_APP_NAME

    if modules is None:
        modules = DEFAULT_MODULES   
    
    app = Flask(app_name)

    app.config.from_pyfile(config)

    # register module
    configure_modules(app, modules) 

    return app

def configure_extensions(app):
    # configure extensions          
    db.init_app(app)

def configure_modules(app, modules):
    
    for url_prefix, module in modules:
        app.register_module(module, url_prefix=url_prefix)
