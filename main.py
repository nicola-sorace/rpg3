#!/usr/bin/python
import pygame

from vmath import * #3D vector math functions

from entity import Entity
from person import Person
from hazard import *
from tile import Tile

VERTICAL_SCALE = 0.5
DRAG_SCALE = 0.4
GRID_X = 20
GRID_Y = 10

WIDTH = 1920
HEIGHT = 1080

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
done = False

clock = pygame.time.Clock()

	#Keybindings
k = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d,	#Move
	pygame.K_SPACE]										#Jump

c = (0,0,0) #Camera coordinates

tc = c #Camera target (for smooth transition)

tiles = [[Tile(0,i,j) for j in range(GRID_Y)] for i in range(GRID_X)]

entities = []
player = Person((10,10,0))
entities.append(player)
entities.append(Person((0,0,0)))
entities.append(Person((20,400,10)))

hazards = []

g = (0,0,-1.5)

renderQueue = []

while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	screen.fill((26,200,26))

	renderQueue = []

	for l in tiles:
		for t in l:
			t.draw(screen, t.x*t.w+WIDTH/2-c[0], t.y*t.h+HEIGHT/2-c[1]/2)

	#entities.sort(key=lambda x: x.p[1], reverse=False)

	shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
	#shade.fill((255,255,255))
	#shade.set_colorkey((255,255,255))

	for h in hazards:
		h.tick()
		if(h.done):
			hazards.remove(h)
		else:
			for e in entities:
				if h.checkCollision(e): h.hurt(e)

			h.v = sub(h.v, fac(sqrt(mag(h.v))*DRAG_SCALE, uni(h.v)))

			#h.draw(screen, h.p[0]-c[0] + WIDTH/2, (h.p[1]-c[1])*VERTICAL_SCALE - h.p[2] + HEIGHT/2)
			s = pygame.Surface((h.r, h.r*VERTICAL_SCALE))
			s.fill((255,255,255))
			s.set_colorkey((255,255,255))
			#pygame.draw.ellipse(s, (0,0,0), [h.p[0]-c[0] + WIDTH/2 - h.r - h.p[2]/6, (h.p[1]-c[1])*VERTICAL_SCALE - h.p[2]/3 + HEIGHT/2 - h.r/2, h.r, h.r*VERTICAL_SCALE])
			pygame.draw.ellipse(s, (0,0,0), [0, 0, h.r, h.r*VERTICAL_SCALE])
			s.set_alpha(10)
			screen.blit(s, (h.p[0]-c[0] + WIDTH/2 - h.r - h.p[2]/6, (h.p[1]-c[1])*VERTICAL_SCALE - h.p[2]/3 + HEIGHT/2 - h.r/2))

			renderQueue.append(h)

	for e in entities:
		e.tick()
		if(e.dead):
			entities.remove(e)
			break

		#TODO Clean up coordinate expressions for readability (and move offsets into the draw function)
		#pygame.draw.rect(screen, (26,26,26), pygame.Rect(e.p[0]+WIDTH/2-c[0], e.p[1]*VERTICAL_SCALE-e.p[2]+HEIGHT/2-c[1]/2, 1, 1))
		e.drawShade(shade, e.p[0]+WIDTH/2-c[0] - e.w/2 -e.p[2]/3, e.p[1]*VERTICAL_SCALE+HEIGHT/2-c[1]*VERTICAL_SCALE - e.h*e.fp -e.p[2]/1.5)
		#e.draw(screen, e.p[0]-c[0] + WIDTH/2 - e.w/2, e.p[1]*VERTICAL_SCALE-e.p[2]-c[1]*VERTICAL_SCALE + HEIGHT/2 - e.h*e.fp)
		renderQueue.append(e)

		#Input
		if(e == player):
			pressed = pygame.key.get_pressed()
			acc = (0,0,0)
			if pressed[k[0]]: acc = sub(acc, (0,1,0))
			if pressed[k[1]]: acc = sub(acc, (1,0,0))
			if pressed[k[2]]: acc = add(acc, (0,1,0))
			if pressed[k[3]]: acc = add(acc, (1,0,0))

			if mag(acc) != 0:
				acc = setMag(e.acc, acc)
				e.v = add(e.v, acc)

			if pressed[k[4]] and e.grounded:
				e.v = add(e.v, (0,0,e.jump))
				e.grounded = False
				e.setAnim(2)

			tc = player.p
			direction = arg(   (pygame.mouse.get_pos()[0]-( e.p[0]+WIDTH/2-c[0] ),   pygame.mouse.get_pos()[1]-( e.p[1]*VERTICAL_SCALE+HEIGHT/2-c[1]/2 ),0)   )
			#if direction > 315: direction = 0
			e.d = round(0 if direction>315 else direction/45)

			if pygame.mouse.get_pressed()[0]: player.attack(hazards, direction)

		#Drag
		e.v = sub(e.v, fac(sqrt(mag(e.v))*DRAG_SCALE, uni(e.v)))

		#Movement
		e.p = add(e.p, e.v)

		if mag(e.v)>1 and e.anim == 0: e.setAnim(1)
		elif mag(e.v)<0.5 and e.anim == 1: e.setAnim(0)

		#Gravity
		if not e.grounded:
			e.v = add(e.v, g)
			if e.p[2] <= 0:
				e.p = (e.p[0],e.p[1],0)
				e.v = (e.v[0],e.v[1],0)
				e.grounded = True
				e.setAnim(0)
	screen.blit(shade, (0,0))

	renderQueue.sort(key=lambda x: x.p[1], reverse=False)
	for e in renderQueue:
		e.draw(screen, e.p[0]-c[0] + WIDTH/2, (e.p[1]-c[1])*VERTICAL_SCALE - e.p[2] + HEIGHT/2)

	dc = fac(0.05, sub(tc,c))
	if mag(dc) > 5: c = add(c,dc)
	#c = add(c,fac(mag(dc), dc))

	myfont = pygame.font.SysFont("monospace", 15)
	label = myfont.render("FPS: "+str(round(clock.get_fps())), 1, (255,255,0))
	screen.blit(label, (0, 0))

	pygame.display.flip()
	clock.tick(60)
