def generateRandomMap(world):
    h=-1
    for h in range(-1,0):
        for y in range(-1,0):
            for x in range(-3,250):
                #print x,"\t",h,"\t",y
                Dynamite((x,h,y),world,recompile=False)
