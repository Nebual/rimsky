import pyglet
import resources

class HUD(object): 
	def __init__(self, window, batch):
		self.window, self.batch = window, batch
		
		group0 = pyglet.graphics.OrderedGroup(0)
		group1 = pyglet.graphics.OrderedGroup(1)
		
		hudX, hudY = window.width-100, window.height-300
		self.sideBG = pyglet.sprite.Sprite(img=resources.loadImage("sidebar.png"), x=hudX, y=hudY, batch=batch, group=group0)
		self.modeLabel = pyglet.text.Label(text="Starmode: 0", font_size=10,x=hudX+50, y=hudY+180, anchor_x="center", batch=batch, group=group1)
		self.fpsLabel = pyglet.text.Label(text="FPS: 0", x=hudX+50, y=hudY+160, anchor_x="center", batch=batch, group=group1)
	def update(self, dt):
		self.fpsLabel.text = "FPS: %.1f" % pyglet.clock.get_fps()
