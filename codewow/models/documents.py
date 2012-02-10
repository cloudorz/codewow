# coding: utf-8

import datetime

from codewow.ext import db
from flaskext.mongoalchemy import BaseQuery

now = datetime.datetime.utcnow

class User(db.Document):

    BLOCK, NORMAL, ADMIN, SA = 0, 100, 200, 300

    nickname = db.StringField(max_length=20)
    email = db.StringField(max_length=64) # 
    role = db.EnumField(db.IntField(), BLOCK, NORMAL, ADMIN, SA, default=NORMAL)
    openid = db.StringField()
    avatar = db.StringField(required=False) # FIXME maybe change
    brief = db.StringField(required=False, max_length=140)
    blog = db.StringField(required=False, max_length=50)
    github = db.StringField(required=False, max_length=50)
    mentions = db.ListField(required=False, item_type=db.DictField(db.AnythingField()), max_capacity=100) # FIXME maybe large 
    follows = db.ListField(required=False, item_type=db.ObjectIdField(), max_capacity=20480) # FIXME maybe large 
    created = db.DateTimeField(default=now)

    @db.computed_field(db.DateTimeField())
    def updated(self):
        return now()


class Gist(db.Document):

    author = db.DocumentField(User)
    desc = db.StringField(max_length=140)
    code_type = db.StringField(max_length=20)
    content = db.StringField()
    snapshot = db.StringField(required=False) # FIXME maybe change
    eggs = db.ListField(required=False, item_type=db.ObjectIdField(), max_capacity=20480) # FIXME maybe large 
    flowers = db.ListField(required=False, item_type=db.ObjectIdField(), max_capacity=20480) # FIXME maybe large 
    followers = db.ListField(required=False, item_type=db.ObjectIdField(), max_capacity=10240) # FIXME maybe large 
    tags = db.SetField(required=False, item_type=db.StringField(), max_capacity=16)
    created = db.DateTimeField(default=now)

    @db.computed_field(db.DateTimeField())
    def updated(self):
        return now()


class Reply(db.Document):

    author = db.DocumentField(User)
    gist = db.DocumentField(Gist)
    content = db.StringField(max_length=140)
    created = db.DateTimeField(default=now)


class Stat(db.Document):

    tag_set = db.DictField(value_type=db.IntField())
    new_gist = db.IntField()
    new_user = db.IntField()
    created = db.DateTimeField(default=now)
