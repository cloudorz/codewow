# coding: utf-8

import pycurl, urllib, json

def sendmail(subject, body, tos):
    return # TODO wait for using
    value = {
            'subject': subject,
            'body': body,
            'to': tos,
            }
    data = {
            'queue': 'mails',
            'value': json.dumps(value),
            }
    c = pycurl.Curl()
    c.setopt(pycurl.URL, "http://localhost:8080")
    c.setopt(pyrcurl.POST, 1)
    c.setopt(pycurl.POSTFIELDS, urllib.urlencode(data))
    c.perfom()
