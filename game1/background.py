import random
import pyglet
import resources
from mathlib import Vector


class Background(object):
	def __init__(self, stars=80):
		self.stars = []
		self.batch = pyglet.graphics.Batch()
		self.setNumStars(stars)
		self.window = pyglet.window.get_platform().get_default_display().get_windows()[0] #For globals

	def setNumStars(self, num=80):
		del self.stars[:]
		rnd = random.Random()
		im = resources.loadImage("star.png")
		
		for i in range(num):
			rnd.seed(5 + i*10293)
			
			corePos = Vector(rnd.random()*800*1.5, rnd.random()*600*1.5)
			spr = pyglet.sprite.Sprite(im, x=corePos.x, y=corePos.y, batch=self.batch)
			
			size = rnd.random() ** 2.8
			spr.scale = size / 2
			spr.speed = size / 8
			self.stars.append(spr)

	def update(self, dt):
		w, h = self.window.width, self.window.height
		camX, camY = self.window.camera.x, self.window.camera.y
		velX, velY = self.window.playerShip.vel.x * dt, self.window.playerShip.vel.y * dt
		
		for spr in self.stars:
			spr.x -= velX * spr.speed
			if (spr.x + w*0.5) < camX: #going to the right
				spr.x += w*1.5
			if (spr.x - w*1.5) > camX:
				spr.x -= w*1.5
			spr.y -= velY * spr.speed
			if (spr.y + h*0.5) < camY:
				spr.y += h*1.5
			if (spr.y - h*1.5) > camY:
				spr.y -= h*1.5
	def draw(self):
		self.batch.draw()
