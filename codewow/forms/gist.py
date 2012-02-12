# coding: utf-8

from flaskext.wtf import Form, TextAreaField, HiddenField, BooleanField, \
        SubmitField, TextField, ValidationError, length, \
        required, email, equal_to, regexp, optional
from flaskext.babel import gettext, lazy_gettext as _ 

class GistForm(Form):

    desc = TextAreaField(_("Description"), validators=[
                      required(message=_("Description required"))])
    code_type = TextField(_("Code type"), validators=[required(message=_("Code type required"))])
    content = TextAreaField(_("Content"))
    tags = TextField(_("Tags"), validators=[
                      required(message=_("Tags required"))])
    submit = SubmitField(_("Save"))
