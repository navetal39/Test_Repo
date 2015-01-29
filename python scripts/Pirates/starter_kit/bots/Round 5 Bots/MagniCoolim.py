def do_turn(game):
    t=[4,2,0,1,3]
    if(len(game.enemy_islands())!=0):
        t=[]
        for n_is in game.neutral_islands():
           t.append(n_is.id)
        for e_is in game.enemy_islands():
           t.append(e_is.id)
    game.debug(t)
        
           
    
    y=0
    if len(game.not_my_islands()) == 0:
        return

    pirates=game.my_pirates()
    for pirate in pirates:
        shave = []
        gave=[]
        good_islands=game.neutral_islands()+game.enemy_islands()
        for isl in good_islands:
            shave.append((isl.id, game.distance(pirate, isl)))
            gave.append(game.distance(pirate, isl))
        minl = shave[0][1]
        ind = 0
        p = []
        gave.sort()
        for ga in gave:
            for sh in shave:
                if sh[1]==ga:
                    p.append(sh[0])
        t=p
        count=0
        for pirate1 in game.my_pirates():
            if (pirate1!=pirate and game.distance(pirate,pirate1)<4):
                count=count+1
        if count==0:
            for isli in game.enemy_islands():
                for ene in game.enemy_pirates():
                    if game.distance(ene,isli)==0:
                        t.remove(isli.id)
                
                
        
        l=[]
        for island in game.islands():
            l.append((island,game.distance(pirate,island)))
        

        island=l[t[y]][0]
        
        
        game.debug(t[y])
        
        if game.is_capturing(pirate):
            
            game.debug(y)
            mamis=[]
            mamis.append(game.get_pirate_on(island))
            island_us=game.my_islands()
            
            y=y+1
            game.debug(y)
            while y<(len(t)-1) and l[t[y]][0] in island_us :
                    
                mamis.append(game.get_pirate_on(l[y][0]))

                y=y+1
           
                game.debug("y="+str(y))
            
            for island in game.islands():
                mamis.append(game.get_pirate_on(island))
                z=0
                for pirate in game.my_pirates():
                    if (game.distance(pirate,island)==0):
                        game.debug("if")
                        if (z==0):
                            z=z+1
                            game.debug(z)
                        else:
                            game.debug("mamis")
                            mamis.remove(pirate)
                            
                   
            for pirate in pirates:
                if pirate in mamis:
                    continue
                else:
                    if (y>(len(t)-1)):
                        y=len(t)-1
                    direction = game.get_directions(pirate, l[t[y]][0])[0]
                    game.set_sail(pirate, direction)
            break
        
        direction = game.get_directions(pirate, l[t[y]][0])[0]
        game.set_sail(pirate, direction)
