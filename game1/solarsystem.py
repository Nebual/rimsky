import pyglet
import random
import physicalobject, resources
from mathlib import Vector

class SolarSystem(object):
	
	def __init__(self, x=0, y=0):
		self.batch = pyglet.graphics.Batch()
		self.x = 0
		self.y = 0
		starImage = resources.loadImage("sun.png", center=True) 
		self.star = physicalobject.Planet(x= self.x, y=self.y, img=starImage, batch=self.batch)
		self.planets = range(random.randint(1, 15))
		for newPlanet in self.planets:
			planetImage = resources.loadImage("planet.png", center=True)
			newPlanet = physicalobject.Planet(x=self.star.x, y=self.star.y, img=planetImage, batch=self.batch)
			randX = random.randint(500, 1000)*random.choice([1, -1])
			randY = random.randint(500, 1000)*random.choice([1, -1])
			newPlanet.x = self.star.x + randX
			newPlanet.y = self.star.y + randY
			
	def draw(self):
		self.batch.draw()
