# coding: utf-8

from flask import g, Module, request, flash, abort, redirect, url_for, session, render_template, current_app
from flaskext.babel import gettext as _
from flaskext.principal import identity_changed, Identity, AnonymousIdentity

from codewow.ext import oid, COMMON_PROVIDERS
from codewow.forms import SignupForm, UpdateProfileForm
from codewow.models import User

account = Module(__name__)

@account.route("/login", methods=('GET', 'POST'))
@oid.loginhandler
def login():
    if g.user is not None:
        return redirect(oid.get_next_url())

    if request.method == 'POST':
        openid = request.form.get('openid')
        if openid:
            return oid.try_login(COMMON_PROVIDERS.get(openid, "fackeone"),
                    ask_for=['email', 'fullname', 'nickname'])

    return render_template('account/login.html',
             next=oid.get_next_url(),
             error=oid.fetch_error())


@oid.after_login
def create_or_login(rsp):
    session['openid'] = rsp.identity_url

    user = User.query.filter_by(openid=rsp.identity_url).first()
    if user is not None:
        flash(_('Successfully signed in'), 'success')
        identity_changed.send(current_app._get_current_object(), identity=Identity(user.pk))
        print Identity(user.pk).name
        return redirect(oid.get_next_url())

    return redirect(url_for('create_profile',
        next=oid.get_next_url(),
        nickname=rsp.nickname or rsp.fullname,
        email=rsp.email))


@account.route('/create-profile', methods=['GET', 'POST'])
def create_profile():
    if g.user is not None or 'openid' not in session:
        return redirect(url_for('home.index'))

    form = SignupForm(
            next=oid.get_next_url,
            nickname=request.values.get('nickname', None),
            email=request.values.get('email', None),
            )

    if form.validate_on_submit():
        user = User(openid=session['openid'])
        form.populate_obj(user)

        user.save()

        flash(_('Profile successfully created'), 'success')

        return redirect(oid.get_next_url())

    return render_template('account/create_profile.html',
            form=form)


@account.route('/profile', methods=['GET', 'POST'])
def edit_profile():
    if g.user is None:
        abort(401)

    form = UpdateProfileForm(
            #email=g.user.email,
            blog=getattr(g.user, 'blog', None),
            github=getattr(g.user, 'github', None),
            brief=getattr(g.user, 'brief', None),
            )

    if form.validate_on_submit():
        if form.delete.data:
            # TODO delete relational data
            g.user.remove()
            session.pop('openid', None)
            flash(_('Profile deleted'), 'success')

            return redirect(url_for('home.index'))

        form.populate_obj(g.user)
        g.user.save()

        return redirect(url_for('edit_profile'))

    return render_template('account/edit_profile.html',
            form=form)


@account.route('/logout')
def logout():
    session.pop('openid', None)
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    flash(_('You have been signed out'), 'success')
    return redirect(oid.get_next_url())
