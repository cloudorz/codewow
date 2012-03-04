# coding: utf-8

from flaskext.wtf import Form, TextAreaField, HiddenField, BooleanField, \
        SubmitField, TextField, ValidationError, length, SelectField, \
        required, email, equal_to, regexp, optional
from flaskext.babel import gettext, lazy_gettext as _ 

class ReplyForm(Form):
    content = TextAreaField(_("Reply"), validators=[required(message=_("Content required"))
        , length(max=140, message=_("Pls. less than 140 characater"))])
    submit = SubmitField(_("Commit"))
