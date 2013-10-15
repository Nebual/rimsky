from consolelib import *
import os

#A bytearray is an editable str, you can pretend its just a str
Screen = bytearray(("*" * 80 + "\n") * 27)
#Position of the caret on the Screen
Pos = 81*5 + 5
#Variables from last frame
PosOld = Pos
PLAYER = "X"
CaretChar = PLAYER
CaretCharOld = "*"

while True:
    PosOld = Pos
    
    key = getKey(timeout=0.5)
    os.system(os.name == "nt" and "cls" or "clear")
    
    if not key:
        #If getKey returned None, the timeout was reached. Blink the caret.
        if CaretChar != PLAYER: 
            CaretChar = PLAYER
        else:
            CaretChar = CaretCharOld
    else:
        CaretChar = PLAYER
    
    #Allow the arrow keys to move the caret around
    if key == UP: Pos -= 81
    elif key == DOWN: Pos += 81
    elif key == RIGHT: Pos += 1
    elif key == LEFT: Pos -= 1
    
    Screen[PosOld] = CaretCharOld
    CaretCharOld = Screen[Pos]
    Screen[Pos] = CaretChar
    
    print Screen

