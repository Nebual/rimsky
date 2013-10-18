from random import randint
import os, time
from consolelib import *

ENTER = "e"
FLAG  = "f"

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

def draw_map( w, h, map = [], guesses = [], flags = [], cx = -1, cy = -1, over = False):
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
	print screen

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
		
def run_game(w=None, h=20, mines=20):
	if not w:
		#We weren't passed a width argument, let them pick a difficulty
		difficulty = int_input("Difficulty [1-3, 0 for custom]? ") or 0
		if difficulty == 0:
			w = int_input("Width? ") or 20
			h = int_input("Height? ") or 20
			mines = int_input("How Many Mines? ") or 20
		elif difficulty == 1:
			w = 9
			h = 9
			mines = 10
		elif difficulty == 2:
			w = 16
			h = 16
			mines = 40
		elif difficulty == 3:
			w = 30
			h = 16
			mines = 99
	x = w / 2
	y = h / 2
	guesses = []
	flags = []
	map = []
	draw_map( w, h )
	game_over = False
	cursor_visible = False
	#game loop
	while not game_over:
		key = True
		while not key == ENTER:
			key = getKey( timeout=0.5 )
			if not key:
				#If getKey returned None, the timeout was reached. Blink the player.
				cursor_visible = not cursor_visible
			elif key == FLAG:
				cursor_visible = False
				if (x,y) not in guesses: 
					flags.append((x,y))
			else:
				#Allow the arrow keys to move the player around
				if key == UP: y -= 1
				elif key == DOWN: y += 1
				elif key == RIGHT: x += 1
				elif key == LEFT: x -= 1
				#make sure that the cursor is on the screen
				if x >= w-1: x = w-1
				elif x < 0: x = 0
				if y >= h-1: y = h-1
				elif y < 0: y = 0
				cursor_visible = True
			#redraw the map
			draw_map( w, h, map, guesses, flags, x * ( 1 if cursor_visible else -1 ), y )
		g = add_guess( x, y, map, guesses, w, h, mines )
		if not type( g ) == bool:
			map = g
			g = True
		if not g:
			game_over = True
			draw_map( w, h, map, guesses, flags, over=True )
			print "Game Over!"
		else:
			if (x,y) in flags:
				flags.remove((x,y))
			if len( guesses ) < w * h - mines:
				draw_map( w, h, map, guesses, flags )
			else:
				game_over = True
				draw_map( w, h, map, guesses, flags, over=True )
				print "You Win!"

if __name__ == "__main__":
	run_game()
