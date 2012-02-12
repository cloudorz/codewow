# coding: utf-8

import datetime

from werkzeug import cached_property
from flaskext.principal import RoleNeed, UserNeed, Permission
from flaskext.mongoalchemy import BaseQuery

from codewow.ext import db
from codewow.permissions import admin, sa


now = datetime.datetime.utcnow

class UserQuery(BaseQuery):

    def from_identity(self, identity):
        user = self.get(identity.name)
        if user:
            identity.provides.update(user.provides)

        identity.user = user

        return user


class User(db.Document):
    query_class = UserQuery

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

    @db.computed_field(db.DateTimeField())
    def updated(self):
        return now()

    class Permissions(object):
        def __init__(self, obj):
            self.obj = obj

        @cached_property
        def edit(self):
            return Permission(UserNeed(self.obj.mongo_id)) & sa

        @cached_property
        def delete(self):
            return Permission(UserNeed(self.obj.mongo_id)) & sa

    @cached_property
    def permissions(self):
        return Self.Permissions(self)

    @cached_property
    def provides(self):
        needs = [RoleNeed('auth'), UserNeed(self.mongo_id)]

        if self.is_sa:
            needs.append(RoleNeed('super'))

        if self.is_admin:
            needs.append(RoleNeed('admin'))

        return needs

    @property
    def is_sa(self):
        return self.role >= self.SA

    @property
    def is_admin(self):
        return self.role >= self.ADMIN


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

    @db.computed_field(db.DateTimeField())
    def updated(self):
        return now()

    class Permissions(object):
        def __init__(self, obj):
            self.obj = obj

        @cached_property
        def edit(self):
            return Permission(UserNeed(self.obj.author.mongo_id))

        @cached_property
        def delete(self):
            return Permission(UserNeed(self.obj.author.mongo_id)) & admin

    @cached_property
    def permissions(self):
        return self.Permissions(self)

    def can_save():
        return self.author and self.desc and self.code_type and content


class Reply(db.Document):

    author = db.DocumentField(User)
    gist = db.DocumentField(Gist)
    content = db.StringField(max_length=140)

    class Permissions(object):
        def __init__(self, obj):
            self.obj = obj

        @cached_property
        def edit(self):
            return Permission(UserNeed(self.obj.author.mongo_id))

        @cached_property
        def delete(self):
            return Permission(UserNeed(self.obj.author.mongo_id)) & admin

    @cached_property
    def permissions(self):
        return self.Permissions(self)


class Stat(db.Document):

    tag_set = db.DictField(value_type=db.IntField())
    new_gist = db.IntField()
    new_user = db.IntField()

