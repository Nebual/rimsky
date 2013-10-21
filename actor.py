import random

class Actor(object):
	name = "Actor"
	maxhp = 1
	_hp = 1
	mp = 1
	minAttack = 1
	maxAttack = 1

	def attack(self, target):
		dmg = random.randint(self.minAttack, self.maxAttack)
		target.hp -= dmg
		return dmg
	
	@property
	def hp(self):
		return self._hp
	
	@hp.setter
	def hp(self, d):
		self._hp = d
		if self._hp > self.maxhp:
			self._hp = self.maxhp
		elif self._hp < 0:
			self._hp = 0

class Player(Actor):
	name = "Player"
	maxhp = 100
	_hp = 100
	mp = 100
	minAttack = 10
	maxAttack = 20

class Monster(Actor):
		
	name = "Default Monster"
	combatNumber = 0				#special number assigned during combat.
	
	def __init__(self, newName):

		self.name = newName
		
		if self.name == 'orc':		#Orc
			self._hp = 30
			self.mp = 0
			self.minAttack = 2
			self.maxAttack = 5
		
		elif self.name == 'goblin':	#Goblin
			self._hp = 20
			self.mp = 0
			self.minAttack = 1
			self.maxAttack = 3
			
		elif self.name == 'dragon':	#Dragon
			self._hp = 100
			self.mp = 50
			self.minAttack = 10
			self.maxAttack = 20
		self.maxhp = self.hp

