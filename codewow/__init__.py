# coding: utf-8

from flask import Flask
from flask import g, session, request

from flaskext.principal import Principal, identity_loaded
from flaskext.babel import Babel, gettext as _

from codewow import views
from codewow.ext import db, oid
from codewow.models import User

# configure
DEFAULT_APP_NAME = 'codewow'

DEFAULT_MODULES = (
    ("", views.home),
    ("", views.account),
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
    configure_ba_handlers(app)
    configure_errorhandlers(app)

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
        g.user = User.query.from_identity(identity)

def configure_ba_handlers(app):

    @app.before_request
    def lookup_current_user():
        g.user = None
        if 'openid' in session:
            g.user = User.query.filter_by(openid=session['openid']).first()

def configure_errorhandlers(app):
   pass 
