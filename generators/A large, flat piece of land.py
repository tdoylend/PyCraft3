def generateRandomMap(world):
    h=-1
    for y in range(-25,25):
        print y
        for x in range(-25,25):
            GrassBlock((x,h,y),world,recompile=False)
