import os, sys
import pyglet
import physicalobject, resources

sys.path.append("..")
from mathlib import Vector

gameWindow = pyglet.window.Window(800, 600)
mainBatch = pyglet.graphics.Batch()

text1 = pyglet.text.Label(text="Center", x=400, y=300, anchor_x="center", batch=mainBatch)
playerShip = physicalobject.Player(x=400, y=200, batch=mainBatch)
gameWindow.push_handlers(playerShip.keyHandler)

gameWindow.camera = Vector(0,0)


def update(dt):
	playerShip.update(dt)
	
@gameWindow.event
def on_draw():
	gameWindow.clear()
	
	pyglet.gl.glLoadIdentity() #Set camera to middle
	pyglet.gl.glTranslatef(-gameWindow.camera[0], -gameWindow.camera[1], 0.5) #Set camera position
	
	mainBatch.draw()
	
if __name__ == '__main__':
	pyglet.clock.schedule_interval(update, 1/120.0)
	pyglet.app.run()
