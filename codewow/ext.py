# coding: utf-8

from flaskext.mongoalchemy import MongoAlchemy
from flaskext.openid import OpenID, COMMON_PROVIDERS

__all__ = ['db', 'oid', 'COMMON_PROVIDERS']

db = MongoAlchemy()
oid = OpenID()
