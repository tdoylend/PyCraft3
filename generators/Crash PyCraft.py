def generateRandomMap(world):
    h=-1
    for h in range(-10,0):
        for y in range(-7,3):
            for x in range(-7,3):
                #print x,"\t",h,"\t",y
                Dynamite((x,h,y),world,recompile=False)
