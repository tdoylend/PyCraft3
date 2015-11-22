def generateRandomMap(world):
    for y in range(5):
        for x in range(-5,5):
            for z in range(-5,5):
                if y > 0 and x >-5 and x < 4 and z > -5 and z < 4:
                    Water((x,y,z),world,recompile=False)
                else:
                    SilverBlock((x,y,z),world,recompile=False)
