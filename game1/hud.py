import pyglet
import resources

class HUD(object): 
	selected = None
	def __init__(self, window, batch):
		self.window, self.batch = window, batch
		
		self.hudScale = 1.0
		
		group0 = pyglet.graphics.OrderedGroup(0)
		group1 = pyglet.graphics.OrderedGroup(1)
		
		self.hudX, self.hudY = hudX, hudY = window.width-100, window.height-200 - 100*self.hudScale
		self.minimap = pyglet.sprite.Sprite(img=window.currentSystem.minimap, x=window.width-100*self.hudScale, y=hudY+200, batch=batch, group=group0)
		self.minimap.scale = self.hudScale
		self.minimapPlayer = pyglet.sprite.Sprite(img=resources.loadImage("circle_silver.png"), batch=batch, group=group1)
		
		self.sideBG = pyglet.sprite.Sprite(img=resources.loadImage("sidebar.png"), x=hudX, y=hudY, batch=batch, group=group0)
		self.modeLabel = pyglet.text.Label(text="Starmode: 0", font_size=10,x=hudX+50, y=hudY+180, anchor_x="center", batch=batch, group=group1)
		self.fpsLabel = pyglet.text.Label(text="FPS: 0", x=hudX+50, y=hudY+160, anchor_x="center", batch=batch, group=group1)
		
		self.selectionSprite = pyglet.sprite.Sprite(img=resources.loadImage("selectionbox.png", center=True), x=0, y=0, batch=self.window.mainBatch)
		self.selectionSprite.visible = False
	def update(self, dt):
		self.fpsLabel.text = "FPS: %.1f" % pyglet.clock.get_fps()
		self.minimapPlayer.x = self.window.width+int(max(3, min(94, 50 + self.window.playerShip.x / self.window.currentSystem.radius * 50))-100)*self.hudScale
		self.minimapPlayer.y = self.hudY+200+int(max(3, min(94, 50 + self.window.playerShip.y / self.window.currentSystem.radius * 50)))*self.hudScale
		
	def select(self, sprite):
		self.selected = sprite
		self.selectionSprite.x, self.selectionSprite.y = sprite.x, sprite.y
		self.selectionSprite.scale = (sprite.radius + 20) / 100.0
		self.selectionSprite.visible = True
	def deselect(self):
		self.selected = None
		self.selectionSprite.visible = False
