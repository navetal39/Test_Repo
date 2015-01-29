def do_turn(game):
    pirates = game.all_my_pirates()
    captains = [pirates[0],pirates[3],pirates[5]]
    isldes = []
    if len(game.not_my_islands()) == 0:
        return
    island = game.not_my_islands()
    i=0
    a = False
    b = False
    if pirates[0].is_lost:
        if not pirates[1].is_lost:
            captains[0]=pirates[1]
            game.set_sail(pirates[2], game.get_directions(pirates[2],pirates[1])[0])
        elif not pirates[2].is_lost:
            captains[0]=pirates[2]
        else:
            a = True
    else:
        game.set_sail(pirates[1], game.get_directions(pirates[1],pirates[0])[0])
        game.set_sail(pirates[2], game.get_directions(pirates[2],pirates[1])[0])
    if pirates[3].is_lost:
        if not pirates[4].is_lost:
            captains[1]=pirates[4]
        else:
            b = True
    else:
        game.set_sail(pirates[4], game.get_directions(pirates[4],pirates[3])[0])
    game.debug(pirates)
    if pirates[5].is_lost:
        captains.remove(pirates[5])
    if b == True:
        captains.remove(pirates[3])
    if a == True:
        captains.remove(pirates[0])
    for captain in captains:   
            if i > len(game.not_my_islands())-1:
                i = 0
            game.debug("going to island " + str(island[i].id))
            isla = [game.distance(captain,island[0]),island[0]]
            for isl in island:
                if game.distance(captain,isl)<isla[0] and isl not in isldes:
                    isla = [game.distance(captain,isl),isl]
            isldes.append(isla[1])
            direction = game.get_directions(captain,isla[1])[0]
            p = game.get_pirate_on(game.destination(captain,direction))
            if p!=None:
                if direction == 'n':
                    direction = 'e'
                elif direction == 'e':
                    direction = 's'
                elif direction == 's':
                    direction = 'w'
                elif direction == 'w':
                    direction = 'n'
            game.set_sail(captain, direction)
            i=i+1
