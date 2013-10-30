import pyglet
from pyglet.window import key
import resources
import math

class PhysicalObject(pyglet.sprite.Sprite):
	
	def __init__(self, *args, **kwargs):
		super(PhysicalObject, self).__init__(*args, **kwargs)
		
		self.velX, self.velY = 0.0, 0.0
		self.window = pyglet.window.get_platform().get_default_display().get_windows()[0]
		
	def update(self, dt):					#updates position, accounting for time elapsed (dt)
		self.x += self.velX * dt
		self.y += self.velY * dt
		#self.checkBounds()
		self.maxSpeed = 600
		
	def checkBounds(self):					#makes screen wrap. replace eventually.
		minX = -self.image.width/2
		minY = -self.image.height/2
		maxX = 800 + self.image.width/2
		maxY = 600 + self.image.width/2
		if self.x < minX:
			self.x = maxX
		elif self.x > maxX:
			self.x = minX
		if self.y < minY:
			self.y = maxY
		elif self.y > maxY:
			self.y = minY		
		
class Player(PhysicalObject):
	
	def __init__(self, *args, **kwargs):
		playerImage = resources.loadImage("playership.png", center=True)	#player texture
		super(Player, self).__init__(img=playerImage, *args, **kwargs)
		self.thrust = 300.0
		self.rotateSpeed = 200.0
		self.keyHandler = key.KeyStateHandler()

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
			self.velX -= (self.velX > 0 and 1 or -1) * min(self.thrust * 0.75 * dt, abs(self.velX))
			self.velY -= (self.velY > 0 and 1 or -1) * min(self.thrust * 0.75 * dt, abs(self.velY))
		
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
		angleRadianss = -math.radians(self.rotation)
		self.velX += math.cos(angleRadianss) * self.thrust * dt * mul
		self.velY += math.sin(angleRadianss) * self.thrust * dt * mul
		s = (self.velX**2 + self.velY**2) ** 0.5
		if s > self.maxSpeed:
			self.velX *= self.maxSpeed / s
			self.velY *= self.maxSpeed / s
