import pyglet
import resources

class HUD(object): 
	def __init__(self, window, batch):
		self.window, self.batch = window, batch
		
		group0 = pyglet.graphics.OrderedGroup(0)
		group1 = pyglet.graphics.OrderedGroup(1)
		
		self.hudX, self.hudY = hudX, hudY = window.width-100, window.height-300
		self.minimap = pyglet.sprite.Sprite(img=window.currentSystem.minimap, x=hudX, y=hudY+200, batch=batch, group=group0)
		self.minimapPlayer = pyglet.sprite.Sprite(img=resources.loadImage("circle_silver.png"), x=hudX+int(50 + window.playerShip.x / window.currentSystem.radius * 50), y=hudY+200+int(50 + window.playerShip.y / window.currentSystem.radius * 50), batch=batch, group=group1)
		
		self.sideBG = pyglet.sprite.Sprite(img=resources.loadImage("sidebar.png"), x=hudX, y=hudY, batch=batch, group=group0)
		self.modeLabel = pyglet.text.Label(text="Starmode: 0", font_size=10,x=hudX+50, y=hudY+180, anchor_x="center", batch=batch, group=group1)
		self.fpsLabel = pyglet.text.Label(text="FPS: 0", x=hudX+50, y=hudY+160, anchor_x="center", batch=batch, group=group1)
	def update(self, dt):
		self.fpsLabel.text = "FPS: %.1f" % pyglet.clock.get_fps()
		self.minimapPlayer.x = self.hudX+int(50 + self.window.playerShip.x / self.window.currentSystem.radius * 50)
		self.minimapPlayer.y = self.hudY+200+int(50 + self.window.playerShip.y / self.window.currentSystem.radius * 50)
