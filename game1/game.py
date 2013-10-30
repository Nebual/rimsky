import os, sys
sys.path.append("..")
import pyglet

import physicalobject, resources
from background import Background
from mathlib import Vector

gameWindow = pyglet.window.Window(800, 600)
mainBatch = pyglet.graphics.Batch() #"Misc" drawables
planetBatch = pyglet.graphics.Batch() #Drawn just after Background

text1 = pyglet.text.Label(text="Center", x=400, y=300, anchor_x="center", batch=mainBatch)

background = Background()
playerShip = physicalobject.Player(x=400, y=200)
gameWindow.playerShip = playerShip
gameWindow.push_handlers(playerShip.keyHandler)

gameWindow.camera = Vector(0,0)
gameWindow.planets = [] #Will need to be moved to like, solarsystem.planets later

physicalobject.Planet(x=1200, y=300, batch=planetBatch, gravity=5.0)


def update(dt):
	playerShip.update(dt)
	background.update(dt)
	
@gameWindow.event
def on_draw():
	gameWindow.clear()
	
	pyglet.gl.glLoadIdentity() #Set camera to middle
	pyglet.gl.glTranslatef(-gameWindow.camera[0], -gameWindow.camera[1], 0.5) #Set camera position

	background.draw()
	planetBatch.draw()	
	mainBatch.draw()
	playerShip.draw()
	
if __name__ == '__main__':
	pyglet.clock.schedule_interval(update, 1/120.0)
	pyglet.app.run()
