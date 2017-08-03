import pygame

class Entity:
	def __init__(self, p):
		self.w = 200
		self.h = 200
		self.fp = 0.8 #Foot position (as a fraction of height)
		self.img = [pygame.image.load("img/person/idle.png"),
			pygame.image.load("img/person/walk.png"),
			pygame.image.load("img/person/jump.png")]
		self.anim = 1
		self.frame = 0
		self.length = [72,48,36] #TODO img and length will be arrays

		self.p = p			#Position
		self.v = (0,0,0)	#Velocity
		self.d = 2		#0-4 clockwise

		self.grounded = False

		self.dead = False	#True if object has been destroyed


	def tick(self):
		pass

	def hurt(self, hp):
		pass

	def drawShade(self, screen, cx, cy):
		#TODO Blur shadow based on z-pos

		shade = self.img[self.anim].subsurface(self.frame*self.w, self.h*2*self.d+self.h, self.w, self.h).copy()
		shade.fill((255, 0, 255, max(200-self.p[2], 1)), None, pygame.BLEND_RGBA_MULT)

		screen.blit(shade, (cx,cy))

	def draw(self, screen, cx, cy):
		screen.blit(self.img[self.anim].subsurface(self.frame*self.w, self.h*2*self.d, self.w, self.h), (cx - self.w/2,cy - self.h*self.fp))

		#This code should probably be elsewhere:
		if self.frame < self.length[self.anim]-1: self.frame += 1
		else: self.frame = 0

		#pygame.draw.rect(screen, (26,26,26), [cx, cy, 1, 1])

	def setAnim(self, n):
		#if self.frame >= self.length[n]: self.frame = self.length[n]-1
		self.frame = 0
		self.anim = n
