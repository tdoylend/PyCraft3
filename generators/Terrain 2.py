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
            ox = -3000
            oy = -3000
            GrassBlock((xv,x[xv]+y[yv],yv),world,recompile=False)
            if randint(1,20)==3: Bush((xv,x[xv]+y[yv]+1,yv),world,recompile=False)
            elif randint(1,100) == 53 and (abs(xv-ox)>5 or abs(yx-oy)>5):
                ox=xv
                oy=yv
                WoodBlock((xv,x[xv]+y[yv]+1,yv),world,recompile=False)
                WoodBlock((xv,x[xv]+y[yv]+2,yv),world,recompile=False)
                WoodBlock((xv,x[xv]+y[yv]+3,yv),world,recompile=False)
                LeafBlock((xv-1,x[xv]+y[yv]+3,yv-1),world,recompile=False)
                LeafBlock((xv-0,x[xv]+y[yv]+3,yv-1),world,recompile=False)
                LeafBlock((xv+1,x[xv]+y[yv]+3,yv-1),world,recompile=False)
                LeafBlock((xv-1,x[xv]+y[yv]+3,yv-0),world,recompile=False)
                LeafBlock((xv+1,x[xv]+y[yv]+3,yv-0),world,recompile=False)
                LeafBlock((xv-1,x[xv]+y[yv]+3,yv+1),world,recompile=False)
                LeafBlock((xv-0,x[xv]+y[yv]+3,yv+1),world,recompile=False)
                LeafBlock((xv+1,x[xv]+y[yv]+3,yv+1),world,recompile=False)
                
                LeafBlock((xv-0,x[xv]+y[yv]+4,yv-1),world,recompile=False)
                LeafBlock((xv-1,x[xv]+y[yv]+4,yv-0),world,recompile=False)
                LeafBlock((xv+1,x[xv]+y[yv]+4,yv-0),world,recompile=False)
                LeafBlock((xv+0,x[xv]+y[yv]+4,yv-0),world,recompile=False)
                LeafBlock((xv-0,x[xv]+y[yv]+4,yv+1),world,recompile=False)

                LeafBlock((xv+0,x[xv]+y[yv]+5,yv-0),world,recompile=False)
            #GrassBlock((xv,x[xv]+y[yv]-1,yv),world,recompile=False)
    
