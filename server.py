# -*- coding: utf-8 -*-
"Якщо немає 'білої' IP-ареси:  ngrok http 8080"
from bottle import route, run, request, WSGIRefServer, ServerAdapter

S={} # словник кораблів

# Корабель створюється http://62a07d86bfa8.ngrok.io/start?name=Bismark&x=1&y=1
@route('/start')
def start_get():
    name = request.GET['name']
    x = int(request.GET['x'])
    y = int(request.GET['y'])
    S[name]=[x,y] # занести корабель у словник
    return "start %s"%name

# Корабель стріляє http://62a07d86bfa8.ngrok.io/shoot?name=Bismark&x=2&y=2
@route('/shoot')
def shoot_get():
    name = request.GET['name']
    if S[name]==[-1,-1]: return '' # якщо потоплений, то ""
    x = int(request.GET['x'])
    y = int(request.GET['y'])
    print name," shoot: ",x," ",y
    for s in S: # для кожного корабля
        if S[s]==[x,y]: # якщо влючили
            print s," ship sunk!"
            S[s]=[-1,-1] # потолений
    return name," shoot"


##
# WSGIRefServer без logging. Див. https://stackoverflow.com/a/13597980/2369808
class WSGIRefServer(ServerAdapter):
    def run(self, handler): # pragma: no cover
        from wsgiref.simple_server import make_server, WSGIRequestHandler

        class LogHandler(WSGIRequestHandler):
            def log_request(self, code='-', size='-'):
                """Log an accepted request.

                This is called by send_response().

                """
                if code not in  ["200", "304"]:
                    self.log_message('"%s" %s %s',
                                     self.requestline, str(code), str(size))

        self.options['handler_class'] = LogHandler
        srv = make_server(self.host, self.port, handler, **self.options)
        srv.serve_forever()

# стартувати http сервер 
run(server=WSGIRefServer, host='localhost', port=8080)  