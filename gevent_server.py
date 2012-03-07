# coding: utf-8
from gevent.wsgi import WSGIServer
from codewoow import create_app

app = create_app('production.cfg')

http_server = WSGIServer(('127.0.0.1', 8000), app)
http_server.serve_forever()
