import os
from werkzeug.wrappers import Request, Response, Headers
from werkzeug.wsgi import SharedDataMiddleware
import json
from pytrain.backend import Backend
import sys
import logging
import logging.handlers
import signal
import select

class PyTrainRequestHandler(object):

    def __init__(self, config):
        self.config = config
        self.backend = Backend()

    def dispatch_request(self, request):
        
        if request.path == '/':
            return Response("Found",status=302,headers=Headers({"Location": "/index.html"}))                   
        elif request.path == '/toggleSwitch' or request.path == '/releaseSwitch' or request.path == '/pressSwitch':
            
            if request.values.has_key('id'):
                swid = request.values['id']
                if swid and swid.startswith('layer_switch_'):
                    i = int(swid[13:])-1
                    if  request.path == '/releaseSwitch':
                        self.backend.setSwitch(i,1)
                    elif request.path == '/pressSwitch':
                        self.backend.setSwitch(i,0)
                    else:
                        self.backend.toggleSwitch(i)
                
            je = json.encoder.JSONEncoder()
            body = je.encode(self.backend.switchState)
            return Response(body,content_type="appplication/json")
                
        
        return Response('Not Found',status=404)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


def create_app(redis_host='localhost', redis_port=6379, with_static=True):
    
    app = PyTrainRequestHandler({
        'use_gpio':       False
    })
    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/':  os.path.join(os.path.dirname(__file__), '../../htdocs')
        })
    return app

if __name__ == '__main__':

    if os.getuid() == 0:
# daemon-mode logging
        handler = logging.handlers.SysLogHandler(facility=logging.handlers.SysLogHandler.LOG_DAEMON,address='/dev/log')

        formatter = logging.Formatter('pytrain %(levelname)s %(message)s')
        handler.setFormatter(formatter)
    else:
# development-mode logging
        handler = logging.StreamHandler(open('/dev/stderr', 'w'))
        formatter = logging.Formatter( '%(asctime)s %(levelname)s %(message)s') 
        handler.setFormatter(formatter)
        
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG)

    root_logger.debug("sys.path=[{}]".format(sys.path))
    # from werkzeug.serving import run_simple
    from werkzeug.serving import make_server
    app = create_app()
    
    server = make_server('0.0.0.0',8011,app,threaded=True)
    
    def signal_handler(sig,frame):
        root_logger.info("Shutting down server upon signal %d."%sig)
        app.backend.reset()
        os.close(server.fileno())
        
    signal.signal(signal.SIGINT,signal_handler)
    signal.signal(signal.SIGHUP,signal_handler)
    signal.signal(signal.SIGTERM,signal_handler)
    signal.signal(signal.SIGABRT,signal_handler)
    signal.signal(signal.SIGQUIT,signal_handler)
    
    try:
        server.serve_forever()
    except select.error:
        exit()
