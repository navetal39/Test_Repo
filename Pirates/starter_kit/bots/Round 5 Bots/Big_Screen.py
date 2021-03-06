def compare_islands(i1, i2):
    if i1[0]>i2[0]:
        return i2
    else:
        return i1
def closest_island(game, pirate, enemy_island_list, neutral_island_list, flag):#, occupied_target):
    if game.is_capturing(pirate):
        return pirate.location
    eexists=(len(enemy_island_list)!=0)
    nexists=(len(neutral_island_list)!=0)
    if eexists and nexists:
        if flag=='e':
            island_list=enemy_island_list
        elif flag=='n':
            island_list=neutral_island_list
    elif eexists:
        island_list=enemy_island_list
    elif nexists:
        island_list=neutral_island_list
    else:
        pid=pirate.id
        return (pid,5-pid)
    
    direction_for_island_list=[(game.distance(pirate, i),i) for i in island_list]
    closest=reduce(compare_islands, direction_for_island_list)
    '''if occupied_target and closest[1]==occupied_target and (len(enemy_island_list)+len(neutral_island_list)) >1:
        if closest[1] in enemy_island_list:
            enemy_island_list.remove(closest[1])
        elif closest[1] in neutral_island_list:
            neutral_island_list.remove(closest[1])
        return closest_island(game, pirate, enemy_island_list, neutral_island_list, flag, occupied_target)'''
    for island in (neutral_island_list):
        if game.get_pirate_on(island) and (game.get_pirate_on(island) is pirate):
            return island
    return closest[1]

def is_occupied(game, pirate, direct, ships):
    current_location=pirate.location
    new_location=game.destination(pirate, direct)
    return game.get_pirate_on(new_location) in ships

def replace_direction(game, direct):
        if direct=='n':
            return 'w'
        elif direct=='s':
            return 'e'
        elif direct=='e':
            return 's'
        elif direct=='w':
            return 'n'
        else:
            return direct

def solve_conflict(game, fleet1, fleet2, target, enemy, neutral):
    distance1=game.distance(fleet1[0], target)
    distance2=game.distance(fleet2[0], target)
    
    if target in enemy:
        enemy.remove(target)
    elif target in neutral:
        neutral.remove(target)
        
    if distance1<=distance2:
        newt1=target
        newt2=closest_island(game, fleet2[0], enemy, neutral, 'n')
    else:
        newt1=closest_island(game, fleet1[0], enemy, neutral, 'e')
        newt2=target
    return newt1, newt2

def replace_target(game, fleet, target, enemy, neutral):
    if target in enemy:
        enemy.remove(target)
    elif target in neutral:
        neutral.remove(target)
    return closest_island(game, fleet[0], enemy, neutral, 'e')
    
def do_turn(game):
    global fleet1_target
    global fleet2_island
    fleet1=[]
    fleet2=[]
    for n in [0,1,2,3]:
        fleet1.append(game.get_my_pirate(n))
    for n in [4,5]:
        fleet2.append(game.get_my_pirate(n))


    
    fleet1_target=closest_island(game, fleet1[0], game.enemy_islands(), game.neutral_islands(), "n")#, None)
    fleet2_target=closest_island(game, fleet2[0], game.enemy_islands(), game.neutral_islands(), "e")#, fleet1_target)

    #if fleet1_target==fleet2_target and len(game.my_islands())<4:
    #    fleet1_target, fleet2_target=solve_conflict(game, fleet1, fleet2, fleet1_target, game.enemy_islands(), game.neutral_islands())


        
    for ship in fleet1:
        try:
            direct=game.get_directions(ship, fleet1_target)[1]
            if not game.is_passable(game.destination(ship, direct)):
                raise
        except:
            direct=game.get_directions(ship, fleet1_target)[0]
        game.set_sail(ship, direct)
    for ship in fleet2:
        try:
            direct=game.get_directions(ship, fleet2_target)[1]
        except:
            direct=game.get_directions(ship, fleet2_target)[0]
        if is_occupied(game, ship, direct, fleet1):
            direct=game.get_directions(ship, replace_target(game, fleet2, fleet2_target, game.enemy_islands(), game.neutral_islands()))[0]
            #fleet2_target=fleet1_target
        game.set_sail(ship, direct)
    

