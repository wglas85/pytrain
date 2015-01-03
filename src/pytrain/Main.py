import os
from werkzeug.wrappers import Request, Response, Headers
from werkzeug.wsgi import SharedDataMiddleware
import json

class Shortly(object):

    def __init__(self, config):
        self.config = config
        self.switchState = [ 0,0,0,0,0,0,0,0,0 ]
#        self.redis = redis.Redis(config['redis_host'], config['redis_port'])

    def dispatch_request(self, request):
        
        if request.path == '/':
            return Response("Found",status=302,headers=Headers({"Location": "/index.html"}))                   
        elif request.path == '/toggleSwitch':
            if request.values.has_key('id'):
                swid = request.values['id']
                if swid and swid.startswith('layer_switch_'):
                    i = int(swid[13:])-1
                    self.switchState[i] = 1-self.switchState[i]
                    print("switched number ",i," new state is ",self.switchState)
                
            je = json.encoder.JSONEncoder()
            body = je.encode(self.switchState)
            return Response(body,content_type="appplication/json")
                
        
        return Response('Not Found',status=404)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


def create_app(redis_host='localhost', redis_port=6379, with_static=True):
    
    app = Shortly({
        'use_gpio':       False
    })
    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/':  os.path.join(os.path.dirname(__file__), '../../htdocs')
        })
    return app

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app = create_app()
    run_simple('127.0.0.1', 8000, app, use_debugger=True, use_reloader=False, threaded=True)