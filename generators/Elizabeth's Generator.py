def generateRandomMap(world):
    h=-1
    for y in range(-10,10):
        print y
        for x in range(-10,10):
            GreenCloth((x,h,y),world,recompile=False)
