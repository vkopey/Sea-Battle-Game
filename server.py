# -*- coding: utf-8 -*-
"Якщо немає 'білої' IP-ареси:  ngrok http 8080"
from bottle import route, run, request, WSGIRefServer, ServerAdapter
from client import Ship

S={} # словник кораблів

# Корабель створюється http://localhost:8080/start?name=Bismark&x=7&y=1&armor=4&gun=4
@route('/start')
def start_get():
    name = request.GET['name']
    x = int(request.GET['x'])
    y = int(request.GET['y'])
    armor = int(request.GET['armor'])
    gun = int(request.GET['gun'])
    if 0<=x<10 and 0<=y<10 and 0<armor<5 and 0<gun<5:
        S[name]=Ship(name,x,y,armor,gun) # занести корабель у словник
        print "start: ", name
    return "start %s"%name

# Корабель стріляє http://localhost:8080/shoot?name=Bismark&x=2&y=2
@route('/shoot')
def shoot_get():
    name = request.GET['name']
    if S[name].armor<=0: return '' # якщо потоплений, то ""
    x = int(request.GET['x'])
    y = int(request.GET['y'])
    print name," shoot: ",x," ",y
    for s in S: # для кожного корабля
        if S[s].x==x and S[s].y==y and S[s].armor>0: # якщо влучили
            S[s].armor-=S[name].gun # пошкодити
            if S[s].armor<=0: print s," ship sunk!"
            else: print s," ship damage!"
    return name," shoot"

# Корабель рухається
@route('/move')
def move_get():
    name = request.GET['name']
    if S[name].armor<=0: return '' # якщо потоплений, то ""
    S[name].x = int(request.GET['x'])
    S[name].y = int(request.GET['y'])
    return name," move"

# Синхронізація http://localhost:8080/sync?name=Bismark
@route('/sync')
def sync_get():
    name = request.GET['name']
    s=S[name]
    return "%d"%s.armor    

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