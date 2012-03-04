# coding: utf-8


from flask import g, Module, request, flash, abort, redirect, url_for, session, render_template, jsonify
from flaskext.babel import gettext as _

from codewow.permissions import normal
from codewow.models import Reply
from codewow.utils.mail import sendmail

reply = Module(__name__)

@reply.route("/<reply_id>/del", methods=("GET",))
@normal.require(401)
def del_reply(reply_id):
    reply = Reply.query.get_or_404(reply_id)
    reply.permissions.delete.test(403)
    reply.remove()

    if g.user.pk != reply.author.pk:
        body = render_template("emails/reply_deleted.html",
                       reply=reply)

        sendmail(subject=_("Your reply has been deleted"),
                body=body,
                tos=[reply.author.email])

    flash(_("The reply has been deleted"), "success")

    return redirect(url_for("gist.detail_gist", gist_id=reply.gist.pk))
