def do_turn(game):

    if len(game.not_my_islands()) == 0:
        return

    island = game.not_my_islands()[0]
    game.debug("going to island " + str(island.id))

    pirates = game.my_pirates()
    for pirate in pirates:
        direction = game.get_directions(pirate, island)[0]
        game.set_sail(pirate, direction)
