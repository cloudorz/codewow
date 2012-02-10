# coding: utf-8

from flask import Flask

from flaskext.principal import Principal, RoleNeed, UserNeed, identity_loaded
from flaskext.babel import Babel, gettext as _

from codewow import views
from codewow.ext import db, oid

# configure
DEFAULT_APP_NAME = 'codewow'

DEFAULT_MODULES = (
    ("", views.home),
)

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
    configure_extensions(app)
    configure_i18n(app)
    configure_identity(app)

    return app

def configure_extensions(app):
    # configure extensions          
    db.init_app(app)
    oid.init_app(app)

def configure_modules(app, modules):
    
    for url_prefix, module in modules:
        app.register_module(module, url_prefix=url_prefix)

def configure_i18n(app):

    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        accept_languages = app.config.get('ACCEPT_LANGUAGES',['en','zh'])
        return request.accept_languages.best_match(accept_languages)

def configure_identity(app):

    principal = Principal(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        g.user = None # TODO user here

def configure_before_handlers(app):

    @app.before_request
    def authenticate():
        g.user = None
        if 'openid' in session:
            g.user = None
