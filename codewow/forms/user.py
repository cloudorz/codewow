# coding: utf-8

from flaskext.wtf import Form, TextAreaField, HiddenField, BooleanField, \
        SubmitField, TextField, ValidationError, length, \
        required, email, equal_to, regexp, optional
from flaskext.babel import gettext, lazy_gettext as _ 

from codewow.models import User
from .validators import is_username

class SignupForm(Form):
    nickname = TextField(_("Nickname"), validators=[
        required(message=_("Nickname required")),
        is_username])
    email = TextField(_("Email address"), validators=[
        required(message=_("Email address required")),
        email(message=_("A valid email address is required"))
        ])
    next = HiddenField()
    submit = SubmitField(_("Create profile"))

    def validate_nickname(self, field):
        user = User.query.filter_by(nickname=field.data and field.data.strip()).first()
        if user:
            raise ValidationError, gettext("This nickname is taken")

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data and field.data.strip()).first()
        if user:
            raise ValidationError, gettext("This email is taken")


class UpdateProfileForm(Form):
    
    blog = TextField(_("Blog url"), validators=[optional()])
    github = TextField(_("Github url"), validators=[optional()])
    brief = TextAreaField(_("Brief"), validators=[optional(), length(max=140,message=_("less than 140 characater"))])

    next = HiddenField()
    submit = SubmitField(_("Update profile"))
    delete = SubmitField(_("Delete"))
