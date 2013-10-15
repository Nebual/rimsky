import os, sys, math, collections
from consolelib import *
from mathlib import *

try: import Image
except ImportError: 
    print "PIL (Python Image Library, or python-imaging) is required"
    sys.exit()


#This is a lookup table for the level loader, mapping colours to entities
EntityFromColour = {}
#This is a dict of static instances of Entities
Entities = {}

class Entity:
    """ This is a generic entity, all worldmap entities should derive from this """
    name = "?"
    char = "?"
    visible = True
    collision = False
    def __init__(self, name, char="?", collision=False, colour=None):
        self.name = name
        self.char = char
        self.collision = collision
        EntityFromColour[colour] = self
def EntityStatic(*args, **kwargs):
    ent = Entity(*args, **kwargs)
    Entities[ent.name] = ent
    return ent

class Player(Entity):
    pos = Vector(0,0)
    def move(self, adjustment):
        newpos = self.pos + adjustment
        if World[newpos][-1].collision: return
        
        #Move our entry in the World
        try: World[self.pos].remove(self)
        except ValueError: pass
        World[newpos].append(self)
        
        #Update the Camera
        if (newpos[0] - CameraPos[0]) < 5: CameraPos[0] += newpos[0] - CameraPos[0] - 5
        if (newpos[1] - CameraPos[1]) < 5: CameraPos[1] += newpos[1] - CameraPos[1] - 5
        if (newpos[0] - CameraPos[0]) > 14: CameraPos[0] += newpos[0] - CameraPos[0] - 14
        if (newpos[1] - CameraPos[1]) > 10: CameraPos[1] += newpos[1] - CameraPos[1] - 10
        
        #Update ourself
        self.pos = newpos
        self.visible = True


EntityStatic("grass", chr(58))
EntityStatic("tree", colourize(winchr(5), "GREEN"),        colour=(0,255,0))
EntityStatic("chest", colourize(winchr(244), "YELLOW"),    colour=(255,148,43))
EntityStatic("wall", winchr(177),                          colour=(0,0,0), collision=True)

#Load us some terrain
class WorldClass(dict):
    def __missing__(self, key):
        #Defaults to a list containing grass
        self[key] = [Entities["grass"]]
        return self[key]
    def load(self, name):
        level1Image = Image.open(name)
        level1 = level1Image.load()
        
        sizex, sizey = level1Image.size
        for x in range(0,sizex):
            for y in range(0, sizey):
                if level1[x,y] in EntityFromColour: 
                    self[x,y].append(EntityFromColour[level1[x,y]])
        return self
#Player initial position (should be based on level loaded)
CameraPos = Vector(0,0)
Ply = Player("player", winchr(1))
World = WorldClass().load("level1.png")
Ply.move(Vector(1,1))



TextBox = ""
def drawScreen():
    ret = []
    for y in range(CameraPos[1], CameraPos[1]+16):
        for x in range(CameraPos[0], CameraPos[0]+20):
            ret.append(next(obj.char for obj in reversed(World[(x,y)]) if obj.visible))
        ret.append("\n")
    print "".join(ret)
    print TextBox

#The Main Loop
while True:
    key = getKey(timeout=0.5)
    os.system(os.name == "nt" and "cls" or "clear")
    if not key:
        #If getKey returned None, the timeout was reached. Blink the player.
        Ply.visible = not Ply.visible
    else:
        TextBox = ""
        
        #Allow the arrow keys to move the player around
        if key == UP: Ply.move(Vector(0,-1))
        elif key == DOWN: Ply.move(Vector(0,1))
        elif key == RIGHT: Ply.move(Vector(1,0))
        elif key == LEFT: Ply.move(Vector(-1,0))
        
        if key == " ":
            ent = World[Ply.pos][-2]
            if ent.name == "grass":
                TextBox = "You find nothing of interest"
            elif ent.name == "tree":
                TextBox = "You pick up the tree.\nYou have nowhere to put it, so it disintegrates into thin air"
                del World[Ply.pos][-2]
            elif ent.name == "chest":
                TextBox = "You find a treasure chest containing Win!\nCongradulations, there is now world peace!"
    
    drawScreen()
