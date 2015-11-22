def generateRandomMap(world):
    GSZ=36
    seed = randint(1,10000000000000)

    o1=OpenSimplex(seed)
    o2=OpenSimplex(seed+3234095345)
    o3=OpenSimplex(seed+32057230983)

    for x in range(GSZ):
        print x
        for z in range(GSZ):
            print x,"\t",z
            noisyness = o2.noise2d(x/20.0,z/20.0)
            noisyness+=1
            y = o1.noise2d(x/10.0,z/10.0)
            y *= (noisyness * 10)
            y = int(y)
            #print x,z,y
            for c in xrange(y-15,y):
                v = o3.noise3d(x/4.0,z/4.0,c/8.0)
                v+=1
                v*=128
                v=int(v)
                if v > 64:
                    if c==(y-1):GrassBlock((x,c,z),world,recompile=False)
                    else:RockBlock((x,c,z),world,recompile=False)
