# coding: utf-8


from flask import g, Module, request, flash, abort, redirect, url_for, session, render_template, jsonify
from flaskext.babel import gettext as _

from codewow.permissions import normal
from codewow.models import Gist, Reply
from codewow.utils.mail import sendmail

reply = Module(__name__)

@reply.route("/<reply_id>", methods=("DELETE", "POST"))
@normal.require(401)
def reply_resouce(reply_id):
    if request.method == 'POST':
        reply = Reply()
        reply.from_dict(request.json_data)
        reply.author = g.user
        reply.maybe_save()

        rsp = make_response(jsonify(msg=_("Created Success")), 201)
        rsp.headers['Location'] = reply.uri
        
    else:
        reply = Reply.query.get_or_404(reply_id)
        reply.permissions.delete.test(403)
        reply.remove()

        if g.user.id != gist.author_id:
            body = render_template("emails/reply_deleted.html",
                                   reply=reply)

            sendmail(subject=_("Your reply has been deleted"),
                    body=body,
                    tos=[reply.author.email])

    return rsp

