# coding: utf-8

import subprocess

from flask import g, Module

deploy = Module(__name__)

@deploy.route("/git_update")
def git_update():
    subprocess.call("cd /data/web/codewow/ && git pull &&\
            cp -a codewow/static /data/web/")

    return "OK"
