# coding: utf-8

from codewow import create_app

app = create_app('dev.cfg')

if __name__ == '__main__':
    app.run()
