from random import *

def generateRandomMap(world):
    GSZ=25
    for x in range(GSZ):
        for z in range(GSZ):
            BlackCloth((x-1,-1,z-1),world,recompile=False)
            if x > 2 or z > 2:
                BlackCloth((x-1,3,z-1),world,recompile=False)
            if not (x%2 or z%2):
                for y in range(3):
                    BlackCloth((x-1,y,z-1),world,recompile=False)
            else:
                if (x%2 != z%2) and (randint(1,3) == 2):
                    for y in range(3):
                        BlackCloth((x-1,y,z-1),world,recompile=False)
