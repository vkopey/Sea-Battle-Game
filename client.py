import urllib2
class Ship:
    def __init__(self, name, x, y):
        self.name=name
        self.x=x
        self.y=y
        url='http://62a07d86bfa8.ngrok.io/start?name=%s&x=%d&y=%d'%(self.name, self.x, self.y)
        urllib2.urlopen(url)            
    def shoot(self,x,y):
        url='http://62a07d86bfa8.ngrok.io/shoot?name=%s&x=%d&y=%d'%(self.name, x, y)
        urllib2.urlopen(url)

p1=Ship("Bismarck", 0, 1)
p2=Ship("Iowa", 2, 2)
#p1.shoot(1,1)
#p2.shoot(1,2)