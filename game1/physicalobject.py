import pyglet
from pyglet.window import key
import resources
import math

from mathlib import Vector

class PhysicalObject(pyglet.sprite.Sprite):
	
	def __init__(self, *args, **kwargs):
		super(PhysicalObject, self).__init__(*args, **kwargs)
		
		self.maxSpeed = 600
		self.vel = Vector(0.0, 0.0)
		self.window = pyglet.window.get_platform().get_default_display().get_windows()[0]
		self.gravity = 0
		self.pos = Vector(self.x, self.y)
		
	def update(self, dt):					#updates position, accounting for time elapsed (dt)
		for planet in self.window.planets:
			self.gravitate(dt, planet)
		self.x += self.vel.x * dt
		self.y += self.vel.y * dt
		#self.checkBounds()
		
	def checkBounds(self):					#makes screen wrap. replace eventually.
		minX = -self.image.width/2
		minY = -self.image.height/2
		maxX = self.window.width + self.image.width/2
		maxY = self.window.height + self.image.width/2
		if self.x < minX:
			self.x = maxX
		elif self.x > maxX:
			self.x = minX
		if self.y < minY:
			self.y = maxY
		elif self.y > maxY:
			self.y = minY		
	
	
	"""
	Assume planet.pos = (500,500)
	Assume player.pos = (510,700)
	
	self = playerShip
	self.vel += Vector(-10, -200).normalized()
	self.vel += Vector(-0.01, -0.99) * planet.gravity / (212**2)
	"""
	
	def gravitate(self, dt, planet):
		if planet.gravity != 0:
			distance = Vector(planet.x,planet.y).distance((self.x,self.y))
			distance2 = distance - planet.radius
			if distance2 < 300:
				if distance > planet.radius: 
					speedChange = ((planet.gravity) / distance2**2) * dt
				#else:
				#	speedChange = -((1000000 * planet.gravity) / 200**2) * dt
					if self.thrust: speedChange = min(self.thrust * 0.75 * dt, speedChange)
					self.vel += Vector(planet.x - self.x, planet.y - self.y).normalized() * speedChange
		
class Player(PhysicalObject):
	
	def __init__(self, *args, **kwargs):
		playerImage = resources.loadImage("playership.png", center=True)	#player texture
		super(Player, self).__init__(img=playerImage, *args, **kwargs)
		self.thrust = 300.0
		self.rotateSpeed = 200.0
		self.starmode = 0
		self.keyHandler = key.KeyStateHandler()
		@self.window.event
		def on_key_press(symbol, modifiers):
			self.keyPress(symbol, modifiers)
	
	def keyPress(self, symbol, modifiers):
		"""This function is run once per key press"""
		if symbol == key.V:
			self.starmode += 1
			if self.starmode > 3: self.starmode = 0
			self.window.modeLabel.text = str(self.starmode)
			self.window.background.setNumStars(80, mode=self.starmode)

	def update(self, dt):							#player updater, checks for key presses
		super(Player, self).update(dt)
		
		if self.keyHandler[key.LEFT]:
			self.rotation -= self.rotateSpeed*dt
		if self.keyHandler[key.RIGHT]:
			self.rotation += self.rotateSpeed*dt
		if self.keyHandler[key.UP]:
			self.increaseThrust(dt, 1)
		if self.keyHandler[key.DOWN]:
			self.increaseThrust(dt, -1)
		if self.keyHandler[key.X]:					#brake
			self.vel.x -= (self.vel.x > 0 and 1 or -1) * min(self.thrust * 0.75 * dt, abs(self.vel.x))
			self.vel.y -= (self.vel.y > 0 and 1 or -1) * min(self.thrust * 0.75 * dt, abs(self.vel.y))
		
		self.updateCamera(dt)
		
	def updateCamera(self, dt):
		"""Shift the camera to always follow the Player."""
		if (self.x - self.window.camera.x) > (self.window.width / 1.5):
			self.window.camera.x += ((self.x - self.window.camera.x) - (self.window.width / 1.5)) * 3 * dt
		elif (self.x - self.window.camera.x) < (self.window.width / 3):
			self.window.camera.x += ((self.x - self.window.camera.x) - (self.window.width / 3)) * 3 * dt
		if (self.y - self.window.camera.y) > (self.window.height / 1.5):
			self.window.camera.y += ((self.y - self.window.camera.y) - (self.window.height / 1.5)) * 3 * dt
		elif (self.y - self.window.camera.y) < (self.window.height / 3):
			self.window.camera.y += ((self.y - self.window.camera.y) - (self.window.height / 3)) * 3 * dt
			
	def increaseThrust(self, dt, mul):				#increase speed up to max speed
		angleRadians = -math.radians(self.rotation)
		self.vel += Vector(math.cos(angleRadians), math.sin(angleRadians)) * (self.thrust * dt * mul)
		s = self.vel.length()
		if s > self.maxSpeed:
			self.vel *= self.maxSpeed / s

class Planet(PhysicalObject):
	def __init__(self, *args, **kwargs):
		planetImage = resources.loadImage("planet.png", center=True)     #planet texture
		super(Planet, self).__init__(img=planetImage, *args, **kwargs)
		self.gravity = planetImage.width*planetImage.height*500			 #Gravity scales with size of image
		self.radius = (planetImage.width + planetImage.height) / 4
		print self.radius
		self.window.planets.append(self)

	def update(self, dt):                                                        
		super(Planet, self).update(dt)
