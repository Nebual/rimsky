from consolelib import *
from mathlib import *

def drawScreen(G, Visible, Pos):
	S = "=" * 12
	S += "\n="
	Count = 0
	for item in G.Inventory:
		if Count % 10 == 0 and Count != 0:
			S += "=\n="
		if Visible and Count == Pos:
			S += winchr(219)
		else:
			S += item.char
		Count += 1
	for x in range(Count, Count/10*10 + 10):
		if Visible and x == Pos:
			S += winchr(219)
		else:
			S += " "
	S += "=\n" + "="*12
	S += "\nCtrl-C to return"
	clear()
	print S

def main(G):
	Visible = True
	Pos = 0
	while True:
		key = getKey(timeout=0.5)
		
		if not key:
			Visible = not Visible
		else:
			Visible = True
			if key == UP: Pos += -10
			elif key == DOWN: Pos += 10
			elif key == RIGHT: Pos += 1
			elif key == LEFT: Pos += -1
			
			if Pos < 0: Pos = 0
			if Pos > (len(G.Inventory)/10 + 1)*10 - 1: Pos = (len(G.Inventory)/10 + 1)*10 - 1
			print Pos
		drawScreen(G, Visible=Visible, Pos=Pos)
