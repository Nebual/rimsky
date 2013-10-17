__all__ = ["colorama", "colourize", "winchr", "clear", "UP", "DOWN", "RIGHT", "LEFT", "getKey"]
import sys, os
try: 
	import colorama; colorama.init() #Allows console colours on Windows
except ImportError: pass
else:
	def colourize(text, colour="GREEN"):
		return colorama.Fore.__dict__[colour] + text + colorama.Fore.RESET
def winchr(num):
	""" Takes a CP850 character int, and returns the unicode string
		Windows's Terminal's extended ASCII is quite nonstandard...
	"""
	if sys.platform != 'win32' and num < 32:
		if num == 1: return unichr(9786)
		elif num == 5: return unichr(9827)
	return unicode(chr(num), "CP850")

UP = "\xe0H"
DOWN = "\xe0P"
RIGHT = "\xe0M"
LEFT = "\xe0K"

def clear():
	os.system(os.name == "nt" and "cls" or "clear")

try:
	import msvcrt, time
	#Okay the import succeeded, we're Windows
	
	def getKey(timeout=0):
		endtime = timeout + time.time()
		while time.time() < endtime:
			if msvcrt.kbhit():
				ch = msvcrt.getch()
				if ord(ch) == 224:
					ch += msvcrt.getch()
				return ch
			else:
				time.sleep(0.01)
		return None
except ImportError: #Linux
	import sys, tty, termios, select
	
	def getch():
		ch = sys.stdin.read(1)
		if ch == chr(27):
			ch += sys.stdin.read(2) #For arrow keys
			if   ch[2] == "A": ch = UP
			elif ch[2] == "B": ch = DOWN
			elif ch[2] == "C": ch = RIGHT
			elif ch[2] == "D": ch = LEFT
		elif ch == chr(3):
			raise KeyboardInterrupt
		return ch
	
	def getKey(timeout=0):
		"""Gets a single character from standard input.  Does not echo to the screen."""
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			if timeout: 
				stdinReady,_,_ = select.select([sys.stdin],[],[],timeout)
				if stdinReady:
					ch = getch()
				else:
					ch = None
			else: ch = getch()
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch

if __name__ == "__main__":
	while True:
		print "Demo: Press two keys, I'll print their char. qq to quit."
		Q = (getKey(3),getKey(0.5))
		print Q
		if Q == ("q","q"): break
