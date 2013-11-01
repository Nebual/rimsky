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
		
		dist = 100
		for i in range(self.rand.randint(1, 15)):
			#Find a random new position that isn't too close to any other planets
			dist += 200 + self.rand.random()*200
			newX, newY = Vector(self.rand.random()*2 -1, self.rand.random()*2 -1).normalized() * dist
			
			planetImage = resources.loadImage("planets/"+self.rand.choice(planetImages), center=True)
			newPlanet = physicalobject.Planet(x=self.star.x, y=self.star.y, img=planetImage, batch=self.batch)
			newPlanet.x = self.star.x + newX
			newPlanet.y = self.star.y + newY
			self.planets.append(newPlanet)
		self.radius = dist
		
		self.minimap = pyglet.image.Texture.create(100,100)
		greenCircle = resources.loadImage("circle_green.png", center=True)
		self.minimap.blit_into(resources.loadImage("circle_gold.png", center=True).image_data, 50, 50, 0)
		for planet in self.planets:
			self.minimap.blit_into(greenCircle.image_data, int(50 + planet.x / dist * 50), int(50 + planet.y / dist * 50), 0)
	
	def farEnough(self, x, y):
		for planet in self.planets:
			if Vector(x, y).distance((planet.x, planet.y)) < 300:
				return False
		return True
