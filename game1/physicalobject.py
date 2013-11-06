import pyglet
from pyglet.window import key
import resources, hud
import math, time
import mathlib

from mathlib import Vector

class PhysicalObject(pyglet.sprite.Sprite):
	
	def __init__(self, *args, **kwargs):
		super(PhysicalObject, self).__init__(*args, **kwargs)
		
		self.maxSpeed = 600
		self.vel = Vector(0.0, 0.0)
		self.window = pyglet.window.get_platform().get_default_display().get_windows()[0]
		self.gravity = 0
		
		
	def update(self, dt):					#updates position, accounting for time elapsed (dt)
		for planet in self.window.currentSystem.planets:
			self.gravitate(dt, planet)
		self.x += self.vel.x * dt
		self.y += self.vel.y * dt
		
			
	def pathToDest(self, dt):		#paths to the selected destination
			destination = self.window.hud.selected
			path = Vector(destination.x - self.x, destination.y - self.y)					#line from player to destination
			self.rotateToPath(path, dt)
			if mathlib.approxCoTerminal(self.pathAngle, self.rotation, 10):
				#Are we close enough to start driving?
				if path.length() >= 200:	#if we're further than twice the object away
					self.increaseThrust(dt, 0.25)
				elif path.length() < 25:
					self.brake(dt)				
		
	def rotateToPath(self, path, dt):
		try:
			self.pathAngle = -1*(math.degrees(math.atan2(float(path.y), path.x)))		#angle of path relative to pos x axis. evaluates between 0 and +180 if below the x-axis, otherwise between 0 and -180, so we have to mess with this a bit		
		except ZeroDivisionError:										
			if path.y >= 0:												# if path is directly above us
				self.pathAngle = -90
			elif path.y < 0:											# if path is directly below us
				self.pathAngle = 90				
		angdiff = mathlib.angDiff(self.pathAngle, self.rotation)
		self.rotation += min(self.rotateSpeed * dt, abs(angdiff)) * -mathlib.sign(angdiff)		
				
	
	
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
					speedChange = ((planet.gravity) / distance2**2.5) * dt
				#else:
				#	speedChange = -((1000000 * planet.gravity) / 200**2) * dt
					if self.thrust: speedChange = min(self.thrust * 0.75 * dt, speedChange)
					self.vel += Vector(planet.x - self.x, planet.y - self.y).normalized() * speedChange
					
	def collide(self):
		pass
						
		
class Player(PhysicalObject):
	
	def __init__(self, *args, **kwargs):
		playerImage = resources.loadImage("playership.png", center=True)	#player texture
		super(Player, self).__init__(img=playerImage, *args, **kwargs)
		self.thrust = 300.0
		self.rotateSpeed = 200.0
		self.rotation = 135
		self.starmode = 0
		self.oriented = False							#for pathing
		self.orbit = False
		self.pathAngle = 0
		self.keyHandler = key.KeyStateHandler()
		self.shootTime = time.time()
		@self.window.event
		def on_key_press(symbol, modifiers):
			self.keyPress(symbol, modifiers)
			
		@self.window.event
		def on_key_release(symbol, modifiers):
			self.keyRelease(symbol, modifiers)
			
		@self.window.event
		def on_mouse_press(x, y, button, modifiers): self.mousePress(x, y, button, modifiers)
	
	def mousePress(self, x, y, button, modifiers):
		vec = self.window.camera + (x, y)
		if button == pyglet.window.mouse.LEFT:
			planet = self.window.currentSystem.nearestPlanet(vec)
			if vec.distance((planet.x, planet.y)) < planet.radius:
				self.window.hud.select(planet)
		elif button == pyglet.window.mouse.RIGHT:
			if time.time() > self.shootTime:
				self.turretFire(vec)
				self.shootTime = time.time() + 0.25
	
	def keyPress(self, symbol, modifiers):
		"""This function is run once per key press"""
		if symbol == key.V:
			self.starmode += 1
			if self.starmode > 3: self.starmode = 0
			self.window.hud.modeLabel.text = "Starmode: "+str(self.starmode)
			self.window.background.setNumStars(80, mode=self.starmode)
		elif symbol == key.L:
			planet = self.window.hud.select(self.window.currentSystem.nearestPlanet(Vector(self.x, self.y)))
			if isinstance(planet, Planet):
				if Vector(*self.position).distance(planet.position) < (planet.radius + 20):
					if self.vel.length() < 30:
						self.window.temp = hud.PlanetFrame(planet)
					else:
						print "You're moving too fast to land!" #TODO: These should be displayed ingame
				else:
					print "You're too far from the planet to land!"
		elif symbol == key.Z:
			self.window.hud.deselect()
			
	def keyRelease(self, symbol, modifiers):
		pass
		
	def update(self, dt):							#player updater, checks for key presses
		super(Player, self).update(dt)	
		
		if self.keyHandler[key.LEFT]:
			self.rotation -= self.rotateSpeed * dt
		if self.keyHandler[key.RIGHT]:
			self.rotation += self.rotateSpeed * dt
		if self.keyHandler[key.UP]:
			self.increaseThrust(dt, 1)
		if self.keyHandler[key.DOWN]:
			self.increaseThrust(dt, -1)
		if self.keyHandler[key.X]:					#brake
			self.brake(dt)
		if self.keyHandler[key.T]:
			self.pathToDest(dt)
		if self.keyHandler[key.SPACE]:
			if time.time() > self.shootTime:
				self.fire()
				self.shootTime = time.time() + 0.25
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
			
	def brake(self, dt):
		self.vel.x -= (self.vel.x > 0 and 1 or -1) * min(self.thrust * 0.75 * dt, abs(self.vel.x))
		self.vel.y -= (self.vel.y > 0 and 1 or -1) * min(self.thrust * 0.75 * dt, abs(self.vel.y))		
			
	def fire(self):
		bulletImg = resources.loadImage("bullet.png", center=True)
		bullet = Bullet(x=self.x, y=self.y, img=bulletImg, batch=self.window.mainBatch)
		angleRadians = -math.radians(self.rotation)
		bullet.vel.x = (self.vel.x + math.cos(angleRadians) * bullet.maxSpeed)
		bullet.vel.y = (self.vel.y + math.sin(angleRadians) * bullet.maxSpeed)	
		self.window.currentSystem.tempObjs.append(bullet)
		
	def turretFire(self, tar):
		#tar = tar.normalized()
		#tar.x *= 10
		#tar.y *= 10
		bulletImg = resources.loadImage("bullet.png", center=True)
		bullet = Bullet(x=self.x, y=self.y, img=bulletImg, batch=self.window.mainBatch)
		bullet.vel.x = ((self.vel.x/2) + tar.x - self.x) * bullet.turretSpeed
		bullet.vel.y = ((self.vel.y/2) + tar.y - self.y) * bullet.turretSpeed
		self.window.currentSystem.tempObjs.append(bullet)		

class Planet(PhysicalObject):
	name = "undefined"
	habited = False
	hasTrade = False
	hasMissions = False
	hasParts = False
	hasShipyard = False
	
	def __init__(self, *args, **kwargs): 
		super(Planet, self).__init__(*args, **kwargs)
		self.gravity = self.width*self.height*300			#Gravity scales with size of image
		self.radius = (self.width + self.height) / 4

	def populate(self, rand, kind):
		if "rock" in kind:
			if "garden" in kind:
				self.name = "GDN_%.4d" % rand.randrange(1,9999)
				self.habited = rand.random() < 0.75
				self.hasTrade = self.habited
				self.hasMissions = self.habited
				if self.habited:
					self.hasParts = rand.random() < 0.6
					if self.hasParts: 
						self.hasShipyard = rand.random() < 0.5
			else:
				self.name = "RCK_%.4d" % rand.randrange(1,9999)
				self.habited = rand.random() < 0.25
				self.hasTrade = self.habited
				self.hasMissions = self.habited
		else:
			#Gas
			self.name = "GAS_%.4d" % rand.randrange(1,9999)
		
class Sun(Planet):
	isSun = True

class Bullet(PhysicalObject):
	def __init__(self, *args, **kwargs):
		super(Bullet, self).__init__(*args, **kwargs)
		self.thrust = False
		self.maxSpeed = 600
		self.turretSpeed = 5
		pyglet.clock.schedule_once(self.die, 0.5)		
		
	def update(self, dt):					#updates position, accounting for time elapsed (dt)		
		self.x += self.vel.x * dt
		self.y += self.vel.y * dt
		self.checkCollision()
	
	def die(self, dt=0):
		self.window.currentSystem.tempObjs.remove(self)
		pyglet.clock.unschedule(self.die)
		
	def checkCollision(self):
		for obj in self.window.currentSystem.ships:
			if Vector(self.x, self.y).distance(Vector(obj.x, obj.y)) < obj.width:
				self.collide(obj)		
	
	def collide(self, obj):
		if hasattr(obj, "hp"):
			obj.hp -= 10
			self.die()
			
				
				
class Ship(PhysicalObject):
	def __init__(self, *args, **kwargs):
		super(Ship, self).__init__(*args, **kwargs)
		self.hp = 30
		self.dead = False
		
	def update(self, dt):
		if self.hp <= 0:
			if not self.dead:
				self.dead = True
				self.oldWidth = self.width
				self.image = resources.loadImage("explosion.png", center=True)
				pyglet.clock.schedule_once(self.die, 0.5)
				self.scale = 0.01
			if self.dead:
				if self.scale < self.oldWidth/250.0:
					self.scale += 2 * self.oldWidth/250.0 * dt
					self.opacity -= 400 * dt
			
			
	def die(self, dt):
		self.window.currentSystem.ships.remove(self)
