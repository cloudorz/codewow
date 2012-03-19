# coding: utf-8

import operator

from flask import Flask, g, session, request, redirect, url_for, jsonify, render_template, flash

from flaskext.principal import Principal, identity_loaded
from flaskext.babel import Babel, gettext as _ # P.S: use gettext, not lazy_gettext or cookies bug

from codewow import views, helpers
from codewow.ext import db, oid
from codewow.models import User, Stat
from codewow.utils.escape import json_encode, json_decode

# configure
DEFAULT_APP_NAME = 'codewow'

DEFAULT_MODULES = (
    ("", views.home),
    ("", views.account),
    ("/gist", views.gist),
    ("/reply", views.reply),
    ("/depoly", views.depoly),
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
    configure_template_filters(app)

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

    @app.before_request
    def convert_data():
        content_type = request.headers.get('Content-Type', '').split(';').pop(0).strip().lower()
        if content_type == 'application/json' and request.method in ('PUT', 'POST'):
            try:
                data = json_decode(request.data) 
            except (ValueError, TypeError), e:
                abort(415)
            else:
                request.json_data = data

    @app.before_request
    def tag_cloud():
        last = Stat.query.descending(Stat.mongo_id).first()
        if last:
            tags = sorted(last.tag_set.items(), key=operator.itemgetter(1), reverse=True)[:20]
        else:
            tags = []

        g.tags = [{'name':k, 'count': v} for k,v in tags]


def configure_errorhandlers(app):
    @app.errorhandler(401)
    def unauthorized(error):
        if request.is_xhr:
            return jsonify(code=401, error=_("Login required"))
        flash(_("Please login to see this page"), "error")
        return redirect(url_for("account.login", next=request.path))
  
    @app.errorhandler(403)
    def forbidden(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, page not allowed'))
        return render_template("errors/403.html", error=error)

    @app.errorhandler(404)
    def page_not_found(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, page not found'))
        return render_template("errors/404.html", error=error)

    @app.errorhandler(500)
    def server_error(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, an error has occurred'))
        return render_template("errors/500.html", error=error)

    @app.errorhandler(415)
    def json_decode_error(error):
        return jsonify(error=_('Json format error'))

    @app.errorhandler(400)
    def json_decode_error(error):
        return jsonify(error=_('args error'))


def configure_template_filters(app):
    
    @app.template_filter()
    def timesince(value):
        return helpers.timesince(value)

    @app.template_filter()
    def endtags(value):
        return helpers.endtags(value)

    @app.template_filter()
    def gravatar(email,size):
        return helpers.gravatar(email,size)

    @app.template_filter()
    def format_date(date,s='full'):
        return helpers.format_date(date,s)

    @app.template_filter()
    def format_datetime(time,s='full'):
        return helpers.format_datetime(time,s)

    @app.template_filter()
    def code_highlight(html):
        return helpers.code_highlight(html)

    @app.template_filter()
    def gistcode(html):
        return helpers.gistcode(html)

    @app.template_filter()
    def intrange(value):
        return helpers.intrange(value)

    @app.template_filter()
    def code2html(code, lang):
        return helpers.code2html(code, lang)

