from random import randint
import os, sys, time
from consolelib import *
import pyglet
from pyglet.window import key

window = pyglet.window.Window()

ENTER = key.E
FLAG  = key.F

StartTime = 0

def int_input( string ):
	try:
		return int( raw_input( string ) )
	except ValueError:
		return int_input( string );
	
def gen_map( x, y, mines, w, h ):
	if ( mines > w * h - 1 ):
		print "Error"
		return
	ops = [ ( a, b ) for a in range( 0, w ) for b in range( 0, h ) ]
	ops.pop( x + y * w )
	l = w * h - 1
	
	map = []
	while mines > 0:
		map.append( ops.pop( randint( 0, l-1 ) ) )
		l -= 1
		mines -= 1
	
	global StartTime
	StartTime = time.time()
	
	return map

def count_beside( map, x, y ):
	num = 0
	pos = [( a, b ) for a in (-1,0,1) for b in (-1,0,1)]
	pos.pop(4)
	for a in pos:
		if map.count( ( x + a[0], y + a[1] ) ) > 0:
			num += 1
	return num


label = pyglet.text.Label('Hello, world',
                          font_name=(sys.platform=='linux2' and 'Monospace' or 'Courier New'),
                          font_size=12,
                          multiline=True, width=window.width,
                          x=0, y=window.height,
                          anchor_x='left', anchor_y='top')

def draw_map(w, h, map = [], guesses = [], flags = [], cx = -1, cy = -1, over = False):
	screen	= ""
	for y in range( 0, h ):
		for x in range( 0, w ):
			if over and map.count( ( x, y ) ) > 0:
				screen += "X"
			elif x == cx and y == cy:
				screen += "#"
			elif (x,y) in guesses:
				char = str( count_beside( map, x, y) )
				if char == "0":
					char = " "
				screen += char
			elif (x,y) in flags:
				screen += "!"
			else:
				screen += "-"
		screen += "\n"
	clear()
	screen += "\nFlags (f): " + str(len(flags))
	screen += "\nLeft (e): " + str(w*h - (len(guesses) + len(flags)))
	if StartTime: screen += "\nTime elapsed: " + str(round(time.time() - StartTime,1))
	if over: screen += "\n"+over+" (r to restart)"
	label.text = screen

@window.event
def on_draw():
	window.clear()
	
	#redraw the map
	if not game_over:
		draw_map( w, h, map, guesses, flags, x * ( 1 if cursor_visible else -1 ), y )
	label.draw()
	
def add_guess( x, y, map, guesses, w, h, mines = 0 ):
	if len( map ) > 0:
		if x >= 0 and y >= 0 and x < w and y < h:
			if (x,y) not in map:
				if (x,y) in guesses:
					return True
				guesses.append( ( x, y ) )
				if count_beside( map, x, y ) == 0:
					pos = [( a, b ) for a in (-1,0,1) for b in (-1,0,1)]
					pos.pop(4)
					for a in pos:
						add_guess( x + a[0], y + a[1], map, guesses, w, h )
				return True
			else:
				return False
		else:
			return True
	else:
		a = gen_map( x, y, mines, w, h )
		add_guess( x, y, a, guesses, w, h)
		return a

w=h=20
x = w / 2
y = h / 2
guesses = []
flags = []
map = []
draw_map( w, h )
game_over = False
cursor_visible = False
@window.event
def on_key_press(symbol, modifiers):
	global map, guesses, flags, w,h,x,y, game_over, cursor_visible
	
	if game_over: 
		if symbol == key.R:
			guesses = []; flags = []; map = []; game_over = False; draw_map(w,h)
		else:
			return
	
	if symbol == ENTER:
		g = add_guess( x, y, map, guesses, w, h, mines )
		if not type( g ) == bool:
			map = g
			g = True
		if not g:
			game_over = "Game Over!"
			draw_map( w, h, map, guesses, flags, over=game_over )
		else:
			if (x,y) in flags:
				flags.remove((x,y))
			if len( guesses ) < w * h - mines:
				draw_map( w, h, map, guesses, flags )
			else:
				game_over = "You Win!"
				draw_map( w, h, map, guesses, flags, over=game_over )
	else:
	#	if not symbol:
	#		#If getKey returned None, the timeout was reached. Blink the player.
	#		cursor_visible = not cursor_visible
		if symbol == FLAG:
			cursor_visible = False
			if (x,y) not in guesses: 
				flags.append((x,y))
		else:
			#Allow the arrow keys to move the player around
			if symbol == key.W: y -= 1
			elif symbol == key.S: y += 1
			elif symbol == key.D: x += 1
			elif symbol == key.A: x -= 1
			#make sure that the cursor is on the screen
			if x >= w-1: x = w-1
			elif x < 0: x = 0
			if y >= h-1: y = h-1
			elif y < 0: y = 0
			cursor_visible = True

def flash_cursor(dt):
	global cursor_visible
	cursor_visible = not cursor_visible
pyglet.clock.schedule_interval(flash_cursor, 0.5)

def run_game(width=None, height=20, minesIn=20):
	global w,h,mines
	if not width:
		#We weren't passed a width argument, let them pick a difficulty
		difficulty = int_input("Difficulty [1-3, 0 for custom]? ") or 0
		if difficulty == 0:
			width = int_input("Width? ") or 20
			height = int_input("Height? ") or 20
			minesIn = int_input("How Many Mines? ") or 20
		elif difficulty == 1:
			width = 9
			height = 9
			minesIn = 10
		elif difficulty == 2:
			width = 16
			height = 16
			minesIn = 40
		elif difficulty == 3:
			width = 30
			height = 16
			minesIn = 99
	w,h,mines = width,height,minesIn
	pyglet.app.run()

if __name__ == "__main__":
	run_game(16,16,40)
