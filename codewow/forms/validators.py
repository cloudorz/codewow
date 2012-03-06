# coding: utf-8

from flaskext.wtf import regexp
from flaskext.babel import lazy_gettext as _

is_username = regexp(r'^\w+$', message=_("You can only use a-z,A-Z,0-9,_"))
