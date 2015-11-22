def generateRandomMap(world):
    for y in range(5):
        for x in range(-5,5):
            for z in range(-5,5):
                if y == 4 and x > -5 and x < 4 and x > -5 and z < 4:
                    Water((x,y,z),world,recompile=False)
                if x == -5 or x == 4 or z == -5 or z == 4:
                    SilverBlock((x,y,z),world,recompile=False)
                if y == 0:
                    SilverBlock((x,y,z),world,recompile=False)

