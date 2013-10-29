import pyglet
import physicalobject
import resources

gameWindow = pyglet.window.Window(800, 600)
mainBatch = pyglet.graphics.Batch()

text1 = pyglet.text.Label(text="some text", x=400, y=300, anchor_x="center", batch=mainBatch)
playerShip = physicalobject.Player(x=400, y=200, batch=mainBatch)
gameWindow.push_handlers(playerShip.keyHandler)


def update(dt):
	playerShip.update(dt)
	
@gameWindow.event
def on_draw():
	gameWindow.clear()
	mainBatch.draw()
	
if __name__ == '__main__':
	pyglet.clock.schedule_interval(update, 1/120.0)
	pyglet.app.run()
