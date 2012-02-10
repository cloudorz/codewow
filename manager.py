#!/usr/bin/env python
# coding: utf-8

from codewow import create_app

from flaskext.script import Server, Shell, Manager, Command, prompt_bool


manager = Manager(create_app('dev.cfg'))

manager.add_command("runserver", Server('0.0.0.0',port=8080))


if __name__ == "__main__":
    manager.run()
