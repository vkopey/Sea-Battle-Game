# -*- coding: utf-8 -*-
import urllib2
serverURL="http://localhost:8080" #http://a944e1c870c1.ngrok.io

class Ship:
    u"Описує кораблі, які створюються на сервері"
    def __init__(self, name, x, y, a, g):
        self.name=name
        self.x=x
        self.y=y
        self.armor=a
        self.gun=g
        
class Battleship(Ship):
    u"""Описує кораблі, які створюються на клієнтах
    name - ім'я корабля
    x, y - координати (0..9)
    a - броня (1..4)
    g - гармати (1..4)
    """
    def __init__(self, name, x, y, a, g):
        Ship.__init__(self, name, x, y, a, g)
        url='%s/start?name=%s&x=%d&y=%d&armor=%d&gun=%d'%(serverURL, self.name, self.x, self.y, self.armor, self.gun)
        urllib2.urlopen(url)
        
    def shoot(self,x,y):
        url='%s/shoot?name=%s&x=%d&y=%d'%(serverURL, self.name, x, y)
        urllib2.urlopen(url)
    
    def move(self,mv='ru'):
        u"Рухає корабель на 1 клітинку (r-вправо, l-вліво, u-вверх, d-вниз)"
        if self.armor<=0: return
        if 'r' in mv and self.x<9: self.x+=1
        elif 'l' in mv and self.x>0: self.x-=1
        if 'u' in mv and self.y<9: self.y+=1
        elif 'd' in mv and self.y>0: self.y-=1
        url='%s/move?name=%s&x=%d&y=%d'%(serverURL, self.name, self.x, self.y)
        urllib2.urlopen(url)
    
    def sync(self):
        u"Синхронізація значення атрибута armor"
        url='%s/sync?name=%s'%(serverURL, self.name)
        f=urllib2.urlopen(url)
        self.armor=int(f.read())
        f.close()
        return self.armor
    
if __name__=='__main__':
    p1=Battleship("Bismarck", 0, 1, 4, 4)
    p2=Battleship("Iowa", 2, 2, 3, 3)
    p1.shoot(1,1)
    p2.shoot(0,1)
    p1.sync()
    p1.move('ru')