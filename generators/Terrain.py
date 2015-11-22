from random import *
def generateRandomMap(world):
    GSZ=50
    x=[]
    v=0
    a=(random()-0.5)*2
    for _ in range(GSZ):
        v+=a
        if randint(1,2) == 2:
            a=(random()-0.5)*2
        x.append(int(v))
    y=[]
    v=0
    a=(random()-0.5)*2
    for _ in range(GSZ):
        v+=a
        if randint(1,2) == 2:
            a=(random()-0.5)*2
        y.append(int(v))

    for xv in range(GSZ):
        for yv in range(GSZ):
            GrassBlock((xv,x[xv]+y[yv],yv),world,recompile=False)
            GrassBlock((xv,x[xv]+y[yv]-1,yv),world,recompile=False)
    
