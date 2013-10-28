import pyglet, random, math
import resources, physicalobject, asteroid
from util import distance

def distance(point_1=(0,0), point_2=(0,0)):
	"""Returns the distance between two points"""
	return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)
	
def asteroids(num_asteroids, player_position, batch=None):
	asteroids = []
	for i in range(num_asteroids):
		asteroid_x, asteroid_y = player_position
		while distance((asteroid_x, asteroid_y), player_position) < 100:
			asteroid_x = random.randint(0, 800)
			asteroid_y = random.randint(0, 600)
		new_asteroid = asteroid.Asteroid(x=asteroid_x, y=asteroid_y, batch=batch)
		new_asteroid.rotation = random.randint(0, 360)
		new_asteroid.velocity_x = random.random()*40
		new_asteroid.velocity_y = random.random()*40
		asteroids.append(new_asteroid)
	return asteroids
	
def player_lives(num_icons, batch=None):
	player_lives = []
	for i in range(num_icons):
		new_sprite = pyglet.sprite.Sprite(img=resources.player_image, x=785-i*30, y=585, batch=batch)
		new_sprite.scale = 0.5
		player_lives.append(new_sprite)
	return player_lives
