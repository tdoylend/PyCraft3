#from random import *

def generateRandomMap(world):
    GSZ=32
    seed = randint(1,10000000000000)

    o=OpenSimplex(seed)

    for x in range(GSZ):
        for z in range(GSZ):
            y = o.noise2d(x/10.0,z/10.0)
            y *= 5
            y = int(y)
            GrassBlock((x,y,z),world,recompile=False)
