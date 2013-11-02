import os, sys
sys.path.append("..")
import pyglet

import physicalobject, resources, solarsystem, hud
from background import Background
from mathlib import Vector

pyglet.clock.set_fps_limit(60)
gameWindow = pyglet.window.Window(800, 600, style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS)

gameWindow.mainBatch = pyglet.graphics.Batch() #"Misc" drawables
gameWindow.hudBatch = pyglet.graphics.Batch() #Drawn after everything

background = Background()
gameWindow.background = background
playerShip = physicalobject.Player(x=400, y=200)
gameWindow.playerShip = playerShip
gameWindow.push_handlers(playerShip.keyHandler)

gameWindow.camera = Vector(0,0)
gameWindow.currentSystem = solarsystem.SolarSystem(x=400, y=300)

gameWindow.hud = hud.HUD(window=gameWindow, batch=gameWindow.hudBatch)


def update(dt):
	playerShip.update(dt)
	background.update(dt)
	gameWindow.hud.update(dt)
	
@gameWindow.event
def on_draw():
	pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
	
	pyglet.gl.glLoadIdentity() #Set camera to middle
	pyglet.gl.glTranslatef(-gameWindow.camera[0], -gameWindow.camera[1], 0.5) #Set camera position

	background.draw()
	gameWindow.currentSystem.batch.draw()
	gameWindow.mainBatch.draw()
	playerShip.draw()
	
	pyglet.gl.glLoadIdentity()
	gameWindow.hudBatch.draw()
	
if __name__ == '__main__':
	pyglet.clock.schedule_interval(update, 1/60.0)
	pyglet.app.run()
