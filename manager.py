#!/usr/bin/env python
# coding: utf-8

from codewow import create_app
from codewow.models import Gist, User, Stat

from flaskext.script import Server, Shell, Manager, Command, prompt_bool


manager = Manager(create_app('dev.cfg'))

manager.add_command("runserver", Server('0.0.0.0',port=8080))

@manager.command
def stat():
    ''' update the stat data command
    '''
    last = Stat.query.descending(Stat.mongo_id).first()
    if last:
        gists = Gist.query.filter(Gist.mongo_id.ge_(last.mongo_id))
        users = User.query.filter(User.mongo_id.ge_(last.mongo_id))
    else:
        gists = Gist.query
        users = User.query

    tag_list = []
    tag_set = set()
    for e in gists:
        tag_list.extend(e.tags)
        tag_set.update(e.tags)

    stat = Stat()
    stat.new_gist = gists.count()
    stat.new_user = users.count()
    stat.tag_set = last and last.tag_set.copy() or {}
    for t in tag_set:
        if t in stat.tag_set:
            stat.tag_set[t] += tag_list.count(t)
        else:
            stat.tag_set[t] = tag_list.count(t)

    stat.save()


if __name__ == "__main__":
    manager.run()
