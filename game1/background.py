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
			spr.speed = rnd.random() ** 2.8
			spr.scale = (spr.speed / 2)
			self.stars.append(spr)

	def update(self, dt):
		gameWindow, playerShip = self.window, self.window.playerShip
		for spr in self.stars:
			spr.x -= playerShip.velX * spr.speed * dt
			if (spr.x + 400) < gameWindow.camera.x: #going to the right
				spr.x += 1200# * (1+rnd.random())
			if (spr.x - 1200) > gameWindow.camera.x:
				spr.x -= 1200# * (1+rnd.random())
			spr.y -= playerShip.velY * spr.speed * dt
			if (spr.y + 300) < gameWindow.camera.y:
				spr.y += 900# * (1+rnd.random())
			if (spr.y - 900) > gameWindow.camera.y:
				spr.y -= 900# * (1+rnd.random())
	def draw(self):
		self.batch.draw()
