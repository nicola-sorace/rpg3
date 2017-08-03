import pygame
from vmath import *

from entity import Entity
from hazard import *

class Person(Entity):
	def __init__(self, p):
		Entity.__init__(self, p)

		self.hp = 1000		#Health
		self.maxHp = self.hp

		self.acc = 1.2		#Aceleration
		self.jump = 30

	def tick(self):
		Entity.tick(self)
		if(self.hp < 0): self.dead = True

	def draw(self, screen, cx, cy):
		Entity.draw(self, screen, cx, cy)

		#Health bar
		if self.hp < self.maxHp and self.hp > 0:
			pygame.draw.rect(screen, (150,0,0), [cx - self.w/6, cy + self.h*(1-self.fp) - 20, self.w/3, 7])
			pygame.draw.rect(screen, (0,200,0), [cx - self.w/6, cy + self.h*(1-self.fp) - 20, (self.w/3)*(self.hp/self.maxHp), 7])
			pygame.draw.rect(screen, (60,60,60), [cx - self.w/6, cy + self.h*(1-self.fp) - 20, self.w/3, 7], 1)

	def attack(self, entities, direction):
		entities.append(  Spray(self, (self.p[0],self.p[1],self.p[2]+80), polToVec(20,direction), 25, 0.1, 1, 50)  )

	def hurt(self, hp):
		Entity.hurt(self, hp)
		self.hp = self.hp - hp
