def generateRandomMap(world):
    GSZ=15
    for x in range(GSZ):
        for z in range(GSZ):
            for y in range(GSZ):
                if z==0 or z==GSZ-1 or x==0 or x==GSZ-1 or y==0 or y==GSZ-1:   
                    BlackCloth((x-2,y,z-2),world,recompile=False)
