from random import *

def generateRandomMap(world):
    h=-1
    for y in range(-5,5):
        print y
        for x in range(-5,5):
            GrassBlock((x,h,y),world,recompile=False)
    for _ in range(6):
        x = randint(-5,4)
        z = randint(-5,4)
        for y in range(3):
            GrayCloth((x,y,z),world,recompile=False)
    
