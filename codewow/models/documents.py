# coding: utf-8

import datetime, re, operator

from flask import g, request, abort, url_for, session
from werkzeug import cached_property
from flaskext.principal import RoleNeed, UserNeed, Permission
from flaskext.mongoalchemy import BaseQuery
from mongoalchemy.exceptions import ExtraValueException
from mongoalchemy.document import Index

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
    follows = db.ListField(required=False, item_type=db.ObjectIdField()) # FIXME maybe large 

    @db.computed_field(db.DateTimeField())
    def updated(self):
        return now()

    class Permissions(object):
        def __init__(self, obj):
            self.obj = obj

        @cached_property
        def edit(self):
            return Permission(UserNeed(self.obj.pk)) & sa

        @cached_property
        def delete(self):
            return Permission(UserNeed(self.obj.pk)) & sa

    @cached_property
    def pk(self):
        return str(self.mongo_id)

    @cached_property
    def permissions(self):
        return Self.Permissions(self)

    @cached_property
    def provides(self):
        needs = [RoleNeed('auth'), UserNeed(self.pk)]

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

    @cached_property
    def avatar_url(self):
        # TODO full url
        return self.avatar

    def __str__(self):
        return "<%s>" % str(self.mongo_id)

    def __repr__(self):
        return "<%s>" % str(self.mongo_id)

    def init_optional(self):
        self.avatar = ""
        self.brief = ""
        self.blog = ""
        self.github = ""
        self.mentions = []
        self.follows = []

    @cached_property
    def gist_num(self):
        return Gist.query.filter(Gist.author.mongo_id==self.mongo_id).count()

    @property
    def created_time(self):
        if self.has_id():
            return self.mongo_id.generation_time

    @cached_property
    def tag_cloud(self):
        last = Stat.query.descending(Stat.mongo_id).first()
        if last:
            tags = sorted(last.tag_set.items(), key=operator.itemgetter(1), reverse=True)[:20]
        else:
            tags = []

        return [{'name':k, 'count': v} for k,v in tags]

    @cached_property
    def recommend_tags(self):
        # FIXME very cost 
        gists = Gist.query.filter(Gist.author.mongo_id==self.mongo_id)
    
        tags = []
        if gists.count() > 0:
            tag_list = []
            tag_set = set()
            for e in gists:
                tag_list.extend(e.tags)
                tag_set.update(e.tags)

            tag_num_list = [(e, tag_list.count(e)) for e in tag_set]

            tags = sorted(tag_num_list, key=operator.itemgetter(1), reverse=True)[:10]

        return [{'name':k, 'count': v} for k,v in tags]


class Gist(db.Document):

    PERN = 20

    author = db.DocumentField(User)
    desc = db.StringField(max_length=140)
    code_type = db.StringField(max_length=20)
    content = db.StringField()
    snapshot = db.StringField(required=False) # FIXME maybe change
    eggs = db.SetField(required=False, item_type=db.ObjectIdField())
    flowers = db.SetField(required=False, item_type=db.ObjectIdField()) 
    followers = db.SetField(required=False, item_type=db.ObjectIdField())
    _tags = db.SetField(required=False, item_type=db.StringField(), max_capacity=8)

    @db.computed_field(db.DateTimeField())
    def updated(self):
        return now()

    t_index = Index().ascending('_tags')

    class Permissions(object):
        def __init__(self, obj):
            self.obj = obj

        @cached_property
        def edit(self):
            return Permission(UserNeed(self.obj.author.pk))

        @cached_property
        def delete(self):
            return Permission(UserNeed(self.obj.author.pk)) & admin

    @cached_property
    def permissions(self):
        return self.Permissions(self)

    @cached_property
    def pk(self):
        return str(self.mongo_id)

    def maybe_save(self, safe=None):
        try:
            self.save()
        except:
            abort(400)

    def from_dict(self, data):
        cls = self.__class__
        fields = self.get_fields()

        for name, field in fields.iteriterms():
            if self.partial and field.db_field not in self.retrieved_fields:
                continue

            if name in data:
                getattr(cls, name).set_value(self, data[name], from_db=loading_from_db)
                continue

        for k in data:
            if k not in fields:
                if self.config_extra_fields == 'ignore':
                    self.__extra_fields_orig[k] = data[k]
                else:
                    raise ExtraValueException(k)

    @cached_property
    def uri(self):
        return url_for("gist.detail_gist", gist_id=self.pk)

    def __str__(self):
        return "<%s>" % str(self.mongo_id)

    def __repr__(self):
        return "<%s>" % str(self.mongo_id)

    def _get_tags(self):
        return self._tags

    def _set_tags(self, tags):
        if isinstance(tags, set):
            self._tags = tags
        elif isinstance(tags, basestring):
            self._tags = set(e for e in re.split('\s+', tags) if e)
        else:
            self._tags = set()

    tags = property(_get_tags, _set_tags)

    def keywords(self):
        return ','.join(self.tags)

    def description(self):
        return self.desc[:20]

    def init_optional(self):
        self.snapshot = ""
        self.eggs = set()
        self.flowers = set()
        self.followers = set()
        self.tags = set()

    @property
    def created_time(self):
        if self.has_id():
            return self.mongo_id.generation_time


class Reply(db.Document):

    PERN = 20

    author = db.DocumentField(User)
    gist = db.DocumentField(Gist)
    content = db.StringField(max_length=140)

    class Permissions(object):
        def __init__(self, obj):
            self.obj = obj

        @cached_property
        def edit(self):
            return Permission(UserNeed(self.obj.author.pk))

        @cached_property
        def delete(self):
            return Permission(UserNeed(self.obj.author.pk)) & \
                    Permission(UserNeed(self.obj.gist.author.pk)) & admin

    @cached_property
    def permissions(self):
        return self.Permissions(self)

    @cached_property
    def pk(self):
        return str(self.mongo_id)

    def maybe_save(self, safe=None):
        try:
            self.save()
        except:
            abort(400)

    def from_dict(self, data):
        cls = self.__class__
        fields = self.get_fields()

        for name, field in fields.iteriterms():
            if self.partial and field.db_field not in self.retrieved_fields:
                continue

            if name in data:
                getattr(cls, name).set_value(self, data[name], from_db=loading_from_db)
                continue

        for k in data:
            if k not in fields:
                if self.config_extra_fields == 'ignore':
                    self.__extra_fields_orig[k] = data[k]
                else:
                    raise ExtraValueException(k)

    @cached_property
    def uri(self):
        return url_for("reply.reply_resource", gist_id=self.pk)

    def __str__(self):
        return "<%s>" % str(self.mongo_id)

    def __repr__(self):
        return "<%s>" % str(self.mongo_id)

    @property
    def created_time(self):
        if self.has_id():
            return self.mongo_id.generation_time


class Stat(db.Document):

    tag_set = db.DictField(value_type=db.IntField())
    new_gist = db.IntField()
    new_user = db.IntField()

    @cached_property
    def pk(self):
        return str(self.mongo_id)

    def __str__(self):
        return "<%s>" % str(self.mongo_id)

    def __repr__(self):
        return "<%s>" % str(self.mongo_id)

    @property
    def created_time(self):
        if self.has_id():
            return self.mongo_id.generation_time
