# coding: utf-8

import random, datetime, hashlib
import calendar
import email.utils

class QDict(dict):
    """A dict that allows for object-like property access syntax."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

# singleton decorator

def singleton(aClass):
    instance = []

    def onCall(*args, **kwargs):
        if not instance:
            instance[0] = aClass(*args, **kwargs)
        return instance[0]

    return onCall

def generate_password():
    return ''.join(random.sample("abcdefghijkmnpqrstuvwxyz23456789", 6))

format = "%Y-%m-%d %H:%M:%S"
def str2time(date_string, format=format):
    return datetime.datetime.strptime(date_string, format)

def time2str(date_obj, format=format):
    return datetime.datetime.strftime(date_obj, format)

def make_md5(*args):
    ''' compute the sveral strings to md5.
    the strings is ordered.
    '''
    md5 = hashlib.md5()
    if args:
        any(md5.update(e) for e in sorted(args))
        return md5.hexdigest()

    return None

def timestamp(timeobject):
    ''' the time senconds from base of 1970.
    '''
    return calendar.timegm(timeobject.utctimetuple())

def pretty_time_str(timeobject):
    '''  'Fri, 09 Dec 2011 13:33:20 GMT'
    '''
    t = timestamp(timeobject)
    return email.utils.formatdate(t, localtime=False, usegmt=True)

if __name__ == "__main__":
    # test 
    pass

