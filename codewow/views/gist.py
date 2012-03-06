# coding: utf-8

from flask import g, Module, request, flash, abort, redirect, url_for, session, render_template, \
                    jsonify
from flaskext.babel import gettext as _

from codewow.permissions import normal
from codewow.models import Gist, Reply, User
from codewow.forms import GistForm, ReplyForm
from codewow.utils.mail import sendmail

gist = Module(__name__)

@gist.route("/<gist_id>/", methods=('GET', 'POST'))
@gist.route("/<gist_id>/<int:p>", methods=('GET', 'POST'))
def detail_gist(gist_id, p=1): 

    gist = Gist.query.get_or_404(gist_id)
    if p<1: p=1

    form = ReplyForm()
    if request.method == 'POST':
        with normal.require(401):
            if form.validate_on_submit():
                reply = Reply(author=g.user, gist=gist)
                form.populate_obj(reply)
                reply.maybe_save()

                flash(_("Post Comment success"), 'success')

                return redirect(url_for('gist.detail_gist', gist_id=gist.pk))

    page_obj = Reply.query.filter(Reply.gist.mongo_id==gist.mongo_id).\
            descending(Reply.mongo_id).\
            paginate(page=p, per_page=Reply.PERN, error_out=False)
    page_url = lambda pn: url_for("gist.detail_gist", gist_id=gist.pk, p=pn)

    return render_template("gist/detail.html",
            form=form,
            gist=gist,
            page_obj=page_obj,
            page_url=page_url)


@gist.route("/<uid>/gists/", methods=('GET',))
@gist.route("/<uid>/gists/<int:p>", methods=('GET',))
def user_gists(uid, p=1):
    user = User.query.get_or_404(uid)
    if p<1: p=1
    page_obj = Gist.query.filter(Gist.author.mongo_id==user.mongo_id).\
            descending(Gist.mongo_id).\
            paginate(page=p, per_page=Gist.PERN, error_out=False)
    page_url = lambda pn: url_for("gist.user_gists", uid=user.pk, p=pn)

    return render_template("gist/personal.html",
            page_obj=page_obj,
            page_url=page_url,
            user=user,
            )


@gist.route("/<uid>/follows/", methods=('GET',))
@gist.route("/<uid>/follows/<int:p>", methods=('GET',))
def followed_gists(uid, p=1):
    user = User.query.get_or_404(uid)
    if p<1: p=1
    page_obj = Gist.query.in_(Gist.mongo_id, *user.follows).\
            descending(Gist.mongo_id).\
            paginate(page=p, per_page=Gist.PERN, error_out=False)
    page_url = lambda pn: url_for("gist.followed_gists", uid=user.pk, p=pn)

    return render_template("gist/babies.html",
            page_obj=page_obj,
            page_url=page_url,
            user=user,
            )


@gist.route("/", methods=('GET', 'POST'))
@normal.require(401)
def create_gist():
    form = GistForm()

    if form.validate_on_submit():
        gist = Gist(author=g.user)
        gist.init_optional()
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


@gist.route("/<gist_id>/del", methods=('GET',))
@normal.require(401)
def del_gist(gist_id):

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
    next_url = request.args.get('next', url_for('home.index'))

    return redirect(next_url)


@gist.route("/<gist_id>/<op>", methods=('GET',))
@normal.require(401)
def vote_gist(gist_id, op):

    if op not in ('up', 'down'): abort(400)  

    gist = Gist.query.get_or_404(gist_id)
    if op == 'up':
        gist.flowers.add(g.user.mongo_id)
        try:
            gist.eggs.remove(g.user.mongo_id)
        except KeyError:
            pass
    else:
        gist.eggs.add(g.user.mongo_id)
        try:
            gist.flowers.remove(g.user.mongo_id)
        except KeyError:
            pass

    gist.save()

    return jsonify(success=True, up_num=len(gist.flowers), down_num=len(gist.eggs))


@gist.route("/<gist_id>/relate", methods=('GET',))
@normal.require(401)
def follow_gist(gist_id):

    gist = Gist.query.get_or_404(gist_id)
    if gist.mongo_id not in g.user.follows:
        g.user.follows.append(gist.mongo_id)
        gist.followers.add(g.user.mongo_id)
        op = 'follow'
        msg = _('unfollow')

    else:
        g.user.follows.remove(gist.mongo_id)
        gist.followers.remove(g.user.mongo_id)
        op = 'unfollow'
        msg = _('follow')

    gist.save()
    g.user.save()

    return jsonify(success=True, op=op, follow_num=len(g.user.follows), msg=msg)
