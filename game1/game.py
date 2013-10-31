import os, sys
sys.path.append("..")
import pyglet

import physicalobject, resources, solarsystem
from background import Background
from mathlib import Vector

gameWindow = pyglet.window.Window(800, 600)
mainBatch = pyglet.graphics.Batch() #"Misc" drawables
planetBatch = pyglet.graphics.Batch() #Drawn just after Background

text1 = pyglet.text.Label(text="Center", x=400, y=300, anchor_x="center", batch=mainBatch)
gameWindow.modeLabel = pyglet.text.Label(text="0", x=400, y=350, anchor_x="center", batch=mainBatch)

background = Background()
gameWindow.background = background
playerShip = physicalobject.Player(x=400, y=200)
gameWindow.playerShip = playerShip
gameWindow.push_handlers(playerShip.keyHandler)

gameWindow.camera = Vector(0,0)
gameWindow.planets = [] #Will need to be moved to like, solarsystem.planets later
newSystem = solarsystem.SolarSystem(x=-1000, y=2)
physicalobject.Planet(x=1200, y=300, img=resources.loadImage("planet.png"), batch=planetBatch)


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
	newSystem.draw()	
	mainBatch.draw()
	playerShip.draw()
	
if __name__ == '__main__':
	pyglet.clock.schedule_interval(update, 1/120.0)
	pyglet.app.run()
