# coding: utf-8


from flask import g, Module, request, flash, abort, redirect, url_for, session, render_template, jsonify
from flaskext.babel import lazy_gettext as _

from codewow.permissions import normal
from codewow.models import Gist, Reply

reply = Module(__name__)

@reply.route("/", methods=("DELETE", "POST"))
@normal.require(401)
def reply_resouce():
    if request.method == 'POST':
        pass
    else:
        pass
    # TODO json ajax
    return "Waiting"
