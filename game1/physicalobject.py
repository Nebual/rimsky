import pyglet
from pyglet.window import key
import resources
import math

class PhysicalObject(pyglet.sprite.Sprite):
	
	def __init__(self, *args, **kwargs):
		super(PhysicalObject, self).__init__(*args, **kwargs)
		
		self.velocity_x, self.velocity_y = 0.0, 0.0
		
	def update(self, dt):
		self.x += self.velocity_x * dt
		self.y += self.velocity_y * dt
		self.check_bounds()
		
	def check_bounds(self):
		min_x = -self.image.width/2
		min_y = -self.image.height/2
		max_x = 800 + self.image.width/2
		max_y = 600 + self.image.width/2
		if self.x < min_x:
			self.x = max_x
		elif self.x > max_x:
			self.x = min_x
		if self.y < min_y:
			self.y = max_y
		elif self.y > max_y:
			self.y = min_y		
		
class Player(PhysicalObject):
	
	def __init__(self, *args, **kwargs):
		super(Player, self).__init__(img=resources.player_image, *args, **kwargs)
		
		self.thrust = 300.0
		self.rotate_speed = 200.0
		self.key_handler = key.KeyStateHandler()

	def update(self, dt):
		super(Player, self).update(dt)
		
		if self.key_handler[key.LEFT]:
			self.rotation -= self.rotate_speed*dt
		if self.key_handler[key.RIGHT]:
			self.rotation += self.rotate_speed*dt
		if self.key_handler[key.UP]:
			angle_radians = -math.radians(self.rotation)
			force_x = math.cos(angle_radians) * self.thrust * dt
			force_y = math.sin(angle_radians) * self.thrust * dt
			self.velocity_x += force_x
			self.velocity_y += force_y
		if self.velocity_x > 600:
			self.velocity_x = 600
		if self.velocity_y > 600:
			self.velocity_y = 600
