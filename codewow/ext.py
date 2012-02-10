# coding: utf-8

from flaskext.mongoalchemy import MongoAlchemy
from flaskext.openid import OpenID

__all__ = ['db', 'oid']

db = MongoAlchemy()
oid = OpenID()
