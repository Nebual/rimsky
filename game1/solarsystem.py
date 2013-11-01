import pyglet
import random, os
import physicalobject, resources
from mathlib import Vector

planetImages = [x for x in os.listdir("resources/planets/") if "png" in x or "jpg" in x]

class SolarSystem(object):
	
	def __init__(self, x=0, y=0, seed=0):
		self.batch = pyglet.graphics.Batch()
		self.x = 0
		self.y = 0
		starImage = resources.loadImage("sun.png", center=True) 
		self.star = physicalobject.Planet(x= self.x, y=self.y, img=starImage, batch=self.batch)
		self.planets = []
		self.rand = random.Random()
		self.rand.seed(73789 + seed*14032)
		for i in range(self.rand.randint(1, 15)):
			#Find a random new position that isn't too close to any other planets
			while True:
				newX = self.rand.randint(500, 1000)*self.rand.choice([1, -1])
				newY = self.rand.randint(500, 1000)*self.rand.choice([1, -1])			
				if self.farEnough(newX, newY):
					break	
			
			
			planetImage = resources.loadImage("planets/"+self.rand.choice(planetImages), center=True)
			newPlanet = physicalobject.Planet(x=self.star.x, y=self.star.y, img=planetImage, batch=self.batch)
			newPlanet.x = self.star.x + newX
			newPlanet.y = self.star.y + newY
			self.planets.append(newPlanet)
	
	def farEnough(self, x, y):
		for planet in self.planets:
			if Vector(x, y).distance((planet.x, planet.y)) < 300:
				return False
		return True
