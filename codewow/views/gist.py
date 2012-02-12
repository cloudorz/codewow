# coding: utf-8

from flask import g, Module, request, flash, abort, redirect, url_for, session, render_template, jsonify
from flaskext.babel import lazy_gettext as _

from codewow.permissions import normal
from codewow.models import Gist, Reply
from codewow.forms import GistForm

gist = Module(__name__)

@gist.route("/", methods=('GET', 'POST'))
@normal.require(401)
def create_gist():

    form = GistForm

    if form.validate_on_submit():

        gist = Gist(author=g.user)
        form.populate_obj(gist)
        gist.save()

        flash(_("Posting success"), "success")

        return redirect(url_for("detail_gist", gist_id=gist.mongo_id))

    return render_template("gist/post_gist.html",
            form=form)


@gist.route("/<gist_id>/edit/", methods=("GET","POST"))
@normal.require(401)
def edit_gist(gist_id):

    gist = Gist.query.get_or_404(gist_id)

    form = GistForm(desc = gist.desc, 
                    code_type = gist.code_type,
                    content = gist.content, 
                    tags = gist.tags)

    if form.validate_on_submit():
        
        form.populate_obj(gist)
        gist.save()
        
        flash(_("Gist has been changed"), "success")
        
        return redirect(url_for("detail_gist", gist_id=gist.mongo_id))

    return render_template("gist/create_gist.html", form=form)


@gist.route("/<gist_id>/detail", methods=('GET',))
def detail_gist(gist_id): 
    gist = Gist.query.get_or_404(gist_id)
    # do other things TODO

    return render_template("gist/detail.html", gist=gist)


@gist.route("/<gist_id>/delete/", methods=("GET","POST"))
@normal.require(401)
def delete_gist(gist_id):

    gist = Gist.query.get_or_404(gist_id)
    gist.permissions.delete.test(403)

    Reply.query.filter_by(gist=gist).remove() # FIXME maybe error here
    
    if g.user.id != gist.author_id:
        body = render_template("emails/post_deleted.html",
                               gist=gist)

        message = Message(subject="Your post has been deleted",
                          body=body,
                          recipients=[gist.author.email])

        #mail.send(message)

    flash(_("The gist has been deleted"), "success")

    return jsonify(success=True,
                   redirect_url=url_for('home.index'))


@gist.route("/<gist_id>", methods=('POST', 'UPDATE', 'DELETE'))
@normal.require(401)
def gist_resource(gist_id=None):
    if request.method == 'POST':
        pass
    elif request.method == 'UPDATE':
        pass
    else:
        pass

    return "Waiting"

