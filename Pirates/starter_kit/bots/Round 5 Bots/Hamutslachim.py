class GroupState:
	CATCH = 0
	ATTACK = 1
	RUN = 2
class GameState:
	NORMAL = 0
def tryMove(game, ship, direction):
	if (not ship.is_lost):
		game.set_sail(ship, direction);

def getClosestIslandTo(game, ship, dist_num):
	if(len(game.not_my_islands())==0):
		return -1
	if(len(game.not_my_islands())==1):
		return game.not_my_islands()[0].id

	islands = game.not_my_islands()
	flag = True
	while (flag):
		flag = False
		for i in range(0,len(islands)-1):
			if( game.distance(ship, islands[i]) > game.distance(ship, islands[i+1]) ):
				island_ = islands[i]
				islands[i] = islands[i+1]
				islands[i+1] = island_
				flag=True
	return islands[min(dist_num, len(islands)-1)].id
	
def getLivePirateIn(game,group_id):
	global groups
	for pirate in groups[group_id]:
		if(not game.get_my_pirate(pirate).is_lost):
			return pirate
	return -1
	

def init(game):
	global initted
	initted = True
	
	global gameState
	gameState = GameState.NORMAL
	
	global group_states
	group_states = [ GroupState.CATCH, GroupState.CATCH, GroupState.CATCH ]
	
	global groups
	groups = []
	groups.append( [0,1] )
	groups.append( [2,3] )
	groups.append( [4,5] )
	global group_targets
	group_targets = [-1,-1,-1]

def getClosestGroupSizeDist(game, group_id):

	if(getLivePirateIn(game, group_id) < 0):
		return (-1,-1)

	global groups
	pirates = game.enemy_pirates()
	
	flag = True
	while (flag):
		flag = False
		for i in range(0,len(pirates)-2):
			if( game.distance([0,0], pirates[i]) > game.distance([0,0], pirates[i+1]) ):
				pirate_ = pirates[i]
				pirates[i] = pirates[i+1]
				pirates[i+1] = pirate_
				flag=True
	group_size = 1
	flag = True
	for i in range(1,len(pirates)-1):
		if(game.distance(pirates[i-1],pirates[i]) < 3) and flag:
			group_size +=1
		else:
			flag = False
	
	return (group_size, game.distance( game.get_my_pirate(groups[group_id][0]) ,pirates[0]))

def onIsle(game,group_id):
	global groups
	return (game.is_capturing(game.get_my_pirate(groups[group_id][0])))

def timeToCap(game, group_id):
	global groups
	for island in game.not_my_islands():
		if(game.in_range(game.get_my_pirate(groups[group_id][0]), island)):
			ttc = 0
			if(island.owner == game.ENEMY):
				ttc+=20
			ttc+=island.capture_duration
			return ttc
	return -1

def modeNormal(game):
	if( len(game.not_my_islands()) != 0 ) :
		for group_id in range(3):
			if( (not game.get_my_pirate(groups[group_id][0]).is_lost) or (not game.get_my_pirate(groups[group_id][1]).is_lost) ):
			
				if(group_states[group_id] == GroupState.RUN) and (group_targets[group_id] == -2):
					group_states[group_id] = GroupState.CATCH
					group_targets[group_id] = -1
				if(group_states[group_id] == GroupState.RUN) and (group_targets[group_id] == -1):
					for island in game.islands():
						
				if( (group_targets[group_id] == -1) or (game.get_island(group_targets[group_id]).owner == game.ME) ):
					group_targets[group_id] = getClosestIslandTo(game,
													game.get_my_pirate(getLivePirateIn(game, group_id)),
													group_id)
					
					#game.debug("Group " + str(group_id) + " getClosestTo: " + str(group_targets[group_id]))
					
				if (group_targets[group_id] != -1):
				
					if(group_states[group_id] == GroupState.CATCH):
						closestGroupSize,distance = getClosestGroupSizeDist(game, group_id)
						if(closestGroupSize != -1 or distance != -1):
							if((onIsle(game,group_id) and (distance < timeToCap(game,group_id)+10) and closestGroupSize > len(groups[group_id]))
								or (distance < 25 and closestGroupSize > len(groups[group_id]))):
									#group_targets[group_id] = getClosestIslandTo(game,
									#						game.get_my_pirate(getLivePirateIn(game, group_id)),
									#						1)
								group_states[group_id] = GroupState.RUN
								group_targets[group_id] = -1
					elif(group_states[group_id] == GroupState.RUN):
						
				
					#game.debug("Group " + str(group_id) + " ship 0, to: " + str(group_targets[group_id]))
					if(group_states[group_id] == GroupState.CATCH):
						for ship in groups[group_id]:
							if(not game.get_my_pirate(ship).is_lost):
								tryMove(game,
									game.get_my_pirate(ship),
									game.get_directions(
										game.get_my_pirate(ship),
										game.get_island(group_targets[group_id])
										)[0]
									)
								
def do_turn(game):

	if(not 'initted' in globals()):
		init()

	global groups
	global mode
	global group_targets

	modeNormal(game)
