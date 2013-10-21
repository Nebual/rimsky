import random, actor

def populate(encounterList):
	"""
	Gets an encounter from a list of possible encounters and creates up to 3 monster objects.
	"""
	selection = encounterList[random.randint(0, len(encounterList)-1)]
	monsters = []

	for name in selection:
		monsters.append(actor.Monster(name))		#append a monster object to a list 'monsters'
	
	num = 1											#assigns a number to each monster for targeting purposes
	for monster in monsters:
		monster.combatNumber = num
		num += 1
	return monsters

def playerTurn(player, monsters):					#make sure to pass the monster list, not just one monster
	while True:	
		playerMove = raw_input("fight, item, or flee? ")
		print
		if playerMove == "fight":
			target = pickTar(monsters)
			dmg = player.attack(target)
			if target.hp == 0:
				print "You did", dmg, "damage to", target.name, "!", target.name, "died!"
			else:
				print "You did", dmg, "damage to", target.name, "! It has", target.hp, "hp left."
			return playerMove
		elif playerMove == "item":
			player.hp += 20
			print "Potion heals you for 20 hp! You have", player.hp, "hp left!"
			return playerMove
		elif playerMove == "flee":
			return playerMove
		else:
			print "Sorry, I didn't understand that. Please try again"
			print

def pickTar(monsters):
	while True:
		choice = input("Attack which monster? (enter 1, 2, or 3) ")
		print	
		for monster in monsters:					#finds monster with that number (assigned in populate())
			if monster.combatNumber == choice and monster.hp !=0:
				return monster 
		print "Sorry, that's not a valid monster. Please try again."
		print

def monsterTurn(player, monster):					#just pass the current monster here, not the list
	dmg = monster.attack(player)
	print monster.name, "attacks you for", dmg, "damage! You have", player.hp, "hp left."

def outcome(player, playerMove):
	"""determines if player won, lost, or fled"""

	if playerMove == "flee":
		return "You fled the battle!"
	elif player.hp > 0:
		return "You win!"
	else:
		return "You lose!"

def main():

	player = actor.Player()							#eventually can pass player obj to this module

	encounterList = [['orc', 'orc', 'goblin'], ['goblin', 'goblin'], ['dragon']]

	monsters = populate(encounterList)

	deadMonsters = 0

	print "You are fighting", len(monsters), "monsters:"
	for monster in monsters:
		print monster.name

	while True:
		print
		playerMove = playerTurn(player, monsters)
		if playerMove == "flee":
			break
		print
		for monster in monsters:
			if monster.hp != 0:
				monsterTurn(player, monster)
			else:
				deadMonsters += 1
		if deadMonsters == len(monsters):
			break
		deadMonsters = 0
		print
	print outcome(player, playerMove)


