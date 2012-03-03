# coding: utf-8

from flask import g, Module, request, flash, abort, redirect, url_for, session, render_template, \
                    jsonify, make_response
from flaskext.babel import gettext as _

from codewow.permissions import normal
from codewow.models import Gist, Reply
from codewow.forms import GistForm
from codewow.utils.mail import sendmail

gist = Module(__name__)

@gist.route("/<gist_id>/detail", methods=('GET',))
def detail_gist(gist_id): 
    #gist = Gist.query.get_or_404(gist_id)
    # do other things TODO

    #return render_template("gist/detail.html", gist=gist)
    return render_template("gist/detail.html")

@gist.route("/", methods=('GET', 'POST'))
@normal.require(401)


@gist.route("/<gist_id>", methods=('POST', 'UPDATE', 'DELETE'))
@gist.route("/", methods=('GET',))
@normal.require(401)
def gist_resource(gist_id=None):
    if request.method == 'GET':
        return render_template("gist/create_gist.html")
    elif request.method == 'POST':
        gist = Gist()
        gist.from_dict(request.json_data)
        gist.author = g.user
        gist.maybe_save()

        rsp = make_response(jsonify(msg=_("Created Success")), 201)
        rsp.headers['Location'] = gist.uri
        
    elif request.method == 'UPDATE':
        gist = Gist.query.get_or_404(gist_id)
        gist.permissions.edit.test(403)
        gist.from_dict(request.json_data)
        gist.mayby_save()

        rsp = make_response(jsonify(msg=_("Updated Success")), 200)
        
    else:
        gist = Gist.query.get_or_404(gist_id)
        gist.permissions.delete.test(403)
        gist.remove()

        if g.user.id != gist.author_id:
            body = render_template("emails/gist_deleted.html",
                                   gist=gist)

            sendmail(subject=_("Your gist has been deleted"),
                    body=body,
                    tos=[gist.author.email])

        rsp = make_response(jsonify(msg=_("Deleted Success")), 200)
        
    return rsp

