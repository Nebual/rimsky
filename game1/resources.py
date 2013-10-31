import pyglet
pyglet.resource.path = ['./resources']
pyglet.resource.reindex()

def centerImage(image):
	"""Sets an image's anchor point to its center"""
	image.anchor_x = image.width/2
	image.anchor_y = image.height/2

def loadImage(filename, center=False):
	image = pyglet.resource.image(filename)
	if center == True:
		centerImage(image)
	return image
	

