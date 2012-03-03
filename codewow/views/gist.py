# coding: utf-8

from flask import g, Module, request, flash, abort, redirect, url_for, session, render_template, \
                    jsonify
from flaskext.babel import gettext as _

from codewow.permissions import normal
from codewow.models import Gist, Reply
from codewow.forms import GistForm
from codewow.utils.mail import sendmail

gist = Module(__name__)

@gist.route("/<gist_id>/", methods=('GET',))
def detail_gist(gist_id): 
    gist = Gist.query.get_or_404(gist_id)
    replies = Reply.query.filter_by(gist=gist).descending(Reply.mongo_id)

    return render_template("gist/detail.html",
            gist=gist,
            replies=replies,
            )


@gist.route("/", methods=('GET', 'POST'))
@normal.require(401)
def create_gist():
    form = GistForm()

    if form.validate_on_submit():

        gist = Gist(author=g.user)
        form.populate_obj(gist)
        gist.maybe_save()

        flash(_("Post gist success"), "success")

        return redirect(url_for("detail_gist", gist_id=gist.pk))

    return render_template("gist/create_gist.html",
            form=form)


@gist.route("/<gist_id>/edit", methods=('GET', 'POST'))
@normal.require(401)
def edit_gist(gist_id):
    gist = Gist.query.get_or_404(gist_id)
    gist.permissions.edit.test(403)
    
    form = GistForm(
            desc=gist.desc,
            code_type=gist.code_type,
            content=gist.content,
            tags=' '.join(gist.tags),
            )

    if form.validate_on_submit():
        
        form.populate_obj(gist)
        gist.maybe_save()
        
        flash(_("Gist has been changed"), "success")
        
        return redirect(url_for("detail_gist", gist_id=gist.pk))

    return render_template("gist/create_gist.html", form=form)


@gist.route("/<gist_id>/edit", methods=('GET',))
@normal.require(401)
def del_gist(gist_id):
    # TODO wait for test

    gist = Gist.query.get_or_404(gist_id)
    gist.permissions.delete.test(403)
    gist.remove()

    # maybe send mail
    if g.user.pk != gist.author.pk:
        body = render_template("emails/gist_deleted.html",
                       gist=gist)

        sendmail(subject=_("Your gist has been deleted"),
                body=body,
                tos=[gist.author.email])

    flash(_("The post has been deleted"), "success")

    # FIXME the redirect url maybe some change
    return jsonify(success=True, redirect_url=url_for('home.index'))
