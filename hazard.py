import pygame
import random

from vmath import *

class Hazard:
    def __init__(self, caster, p, r, hp, tickTime, time):
        self.caster = caster #Entity casting the spell (can be None)

        self.p = p
        self.r = r

        self.hp = hp         #Damage per tick
        self.tickTime = tickTime       #Length of each tick in milliseconds
        self.time = time     #Ticks before damage is destroyed (-1 for never)

        self.done = False   #Object is waiting to be destroyed when True

    def tick(self):
        if self.time != -1:
            self.time = self.time - self.tickTime
            if self.time <= 0: self.done = True

    '''
    #TODO checkVolume
    def checkPoint(self, p):
        if mag(sub(p, self.p)) <= self.r: return True
        return False
    '''

    def checkCollision(self, e):
        collision = True

        for x in range(0,3): #Loop through dimensions
            if not(  self.p[x]+self.r > e.p[x] + (0 if x==2 else -e.w/2) and self.p[x]-self.r < e.p[x] + (e.h if x==2 else e.w/2)  ):
                collision = False
                break

        return collision

    def hurt(self, e):
        if e != self.caster: e.hurt(self.hp)

    def draw(self, screen, cx, cy):
        #TODO Shadow
        pygame.draw.ellipse(screen, (255,0,0), [cx-self.r, cy-self.r, self.r, self.r]) #TODO Should use 'VERTICAL_SCALE'
        #pygame.draw.rect(screen, (26,26,26), [cx, cy, 1, 1])

class Hit(Hazard):
    def tick(self):
        Hazard.tick(self)

class Beam(Hazard):
    def __init__(self, caster, p, v, r, hp, tickTime, time):
        Hazard.__init__(self, caster, p, r, hp, tickTime, time)
        self.v = add(caster.v, v)

    def tick(self):
        Hazard.tick(self)
        self.p = add(self.p, self.v)

class Spray(Beam):
    def __init__(self, caster, p, v, r, hp, tickTime, time):
        Beam.__init__(self, caster, p, v, r, hp, tickTime, time)
        self.spread = 1

    def tick(self):
        self.v = add(self.v, (random.uniform(-self.spread,self.spread), random.uniform(-self.spread,self.spread), random.uniform(-self.spread,self.spread)))
        self.r = self.r+0.5
        Beam.tick(self)

class Projectile(Beam):
    def hurt(self, e):
        Beam.hurt(self,e)
        if e != self.caster: self.done = True

class Area(Hazard):
    def tick(self):
        Hazard.tick(self)
