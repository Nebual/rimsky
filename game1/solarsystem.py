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
		self.planets = []
		for i in range(random.randint(1, 15)):
			newX, newY = self.testPosition()
			planetImage = resources.loadImage("planet.png", center=True)
			newPlanet = physicalobject.Planet(x=self.star.x, y=self.star.y, img=planetImage, batch=self.batch)
			newPlanet.x = self.star.x + newX
			newPlanet.y = self.star.y + newY
			self.planets.append(newPlanet)
	def draw(self):
		self.batch.draw()
	
	def testPosition(self):
		while True:			
			randX = random.randint(500, 1000)*random.choice([1, -1])
			randY = random.randint(500, 1000)*random.choice([1, -1])			
			if self.farEnough(randX, randY):
				return randX, randY	
	
	def farEnough(self, x, y):
		for planet in self.planets:
			if Vector(x, y).distance((planet.x, planet.y)) < 300:
				return False
		return True
