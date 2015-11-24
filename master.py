
data=open("settings.ini","r").readlines()

from time import *
import datetime
from logger import *
logdata("\nPyCraft was started at "+datetime.datetime.ctime(datetime.datetime.now()))

PROJECT_ID = "27000d60d1768c38"

from math import *

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
from random import *
import thread
import easygui
#import picker
import os
#from opensimplex.opensimplex import *
os.environ["SDL_VIDEO_CENTERED"] = '1'
WALK_SPEED = 0.15
SELECTSIZE = 0.505
RATE = 1/16.0
SCREEN_SIZE = (1366,768)

exec open("blocks.py","r").read()
exec open("world.py","r").read()      
exec open("misc.py","r").read()     
exec open("parser.py","r").read()
exec open("particles.py","r").read()
class CubeThingy:
    coords_top=[RATE*1,RATE*15,RATE*2,RATE*14]
    coords_btm=[RATE*1,RATE*15,RATE*2,RATE*14]
    coords_lft=[RATE*1,RATE*15,RATE*2,RATE*14]
    coords_rgt=[RATE*1,RATE*15,RATE*2,RATE*14]
    coords_fwd=[RATE*1,RATE*15,RATE*2,RATE*14]
    coords_bck=[RATE*1,RATE*15,RATE*2,RATE*14]
    def __init__(self,pos,world,create=True,recompile=True):
        self.pos=pos
    def render_index(self):
        glDisable(GL_TEXTURE_2D)
        glBegin(GL_QUADS)
        glColor(0.5,0.5,0.5,1.0);
        glNormal3f(0,0,1)
        glTexCoord2f(self.coords_fwd[0],self.coords_fwd[3]); glVertex3f(self.pos[0]+ -0.5,self.pos[1]+-0.5,self.pos[2]+0.5) #Front
        glTexCoord2f(self.coords_fwd[2],self.coords_fwd[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_fwd[2],self.coords_fwd[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_fwd[0],self.coords_fwd[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glNormal3f(0,0,-1)
        glColor(0,1,0,1.0);
        glTexCoord2f(self.coords_bck[2],self.coords_bck[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_bck[0],self.coords_bck[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5) #Back
        glTexCoord2f(self.coords_bck[0],self.coords_bck[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_bck[2],self.coords_bck[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glNormal3f(0,-1,0)
        glColor(0,0,1,1.0);
        glTexCoord2f(self.coords_btm[2],self.coords_btm[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5) #Bottom
        glTexCoord2f(self.coords_btm[0],self.coords_btm[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_btm[0],self.coords_btm[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_btm[2],self.coords_btm[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glNormal3f(0,1,0)
        glColor(1,1,0,1.0);
        glTexCoord2f(self.coords_top[0],self.coords_top[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #Top
        glTexCoord2f(self.coords_top[2],self.coords_top[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_top[2],self.coords_top[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_top[0],self.coords_top[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glNormal3f(-1,0,0)
        glColor(0,1,1,1.0);
        glTexCoord2f(self.coords_lft[0],self.coords_lft[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_lft[0],self.coords_lft[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #left
        glTexCoord2f(self.coords_lft[2],self.coords_lft[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_lft[2],self.coords_lft[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glNormal3f(1,0,0)
        glColor(1,0,1,1.0);
        glTexCoord2f(self.coords_rgt[2],self.coords_rgt[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_rgt[2],self.coords_rgt[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #right
        glTexCoord2f(self.coords_rgt[0],self.coords_rgt[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_rgt[0],self.coords_rgt[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glEnd() 
        glEnable(GL_TEXTURE_2D)
def trace(pos,world):
    mycube=CubeThingy(pos,None,False,False)
    glColor(1.0,1.0,1.0,1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glDisable(GL_FOG)
    glLoadIdentity();
    glRotate(world.player_angle[0],1,0,0)
    glRotate(world.player_angle[1],0,1,0)
    glTranslate(-world.player_pos[0],-world.player_pos[1],world.player_pos[2])
    #glBindTexture(GL_TEXTURE_2D, texture_id)
    mycube.render_index()
    glEnable(GL_FOG)
    pixels=[0,0,0,0]
    return tuple(glReadPixels(SCREEN_SIZE[0]/2,SCREEN_SIZE[1]/2,1,1,GL_RGBA,GL_UNSIGNED_BYTE,pixels))

def runQuit(world):
    pygame.quit()
    thread_run=False
    world.save()
    easygui.msgbox(title = "Saved",msg = "Your world, \""+world.saveName+",\" has been saved.")
    logdata("PyCraft was closed.")
    quit()

def getFile(world):
    b = easygui.buttonbox("","PyCraft: Select a World", ("Load World","New World","Quit"))
    if b == "Quit":
        logdata("The user quitted immediatly.")
        quit()
    if b == "New World":
        logdata("The user created a new world.")
        name = easygui.enterbox("Pick a name for your world: ")
        logdata("They named it '"+name+"'.")
        gens = os.listdir("generators/")
        for gen in range(len(gens)):
            gens[gen] = gens[gen][:-3]
        gen = easygui.choicebox("Select a world generator: ","",gens)
        logdata("They used the generator '"+gen+"'.")
        exec open("generators/"+gen+".py").read()
        generateRandomMap(world)
        
        world.saveName = name
    if b == "Load World":
        worlds = os.listdir("worlds/")
        world_name = easygui.choicebox("Select a world","Pycraft: Select a World", worlds)
        logdata("They loaded the world named '"+world_name+"'.")
        world_data = open("worlds/"+world_name,"r").read()
        logdata("It contains "+str(len(world_data.split("\n"))-1)+" blocks.")
        parseMap(world,world_data)
        world.saveName = world_name
        

color_index = {
    (255,255,0,255):(0,1,0),
    (0,0,255,255):  (0,-1,0),
    (0,255,255,255): (-1,0,0),
    (255,0,255,255): (1,0,0),
    (128,128,128,255): (0,0,1),
    (0,255,0,255):    (0,0,-1)}

def blockSelector(block_index,block_tex):
    a=0
    glClearColor(0,0,0,255)
    blocklist=[BasicBlock,DirtBlock,WoodBlock,RockBlock,LeafBlock,
    RedCloth,OrangeCloth,YellowCloth,GreenCloth,CyanCloth,BlueCloth,
    PurpleCloth,BlackCloth,GrayCloth,WhiteCloth,PlankBlock,DoorShutBottom,
    Dynamite,Snow,Cake,SwissCheese,Glass,GoldBlock,SilverBlock,Water,
    BrickBlock,HatchShut,WaterBucket,SandBlock,DyedSand,Generator,LED,Switch,Wire,
    AND,NOT,XOR,Spout,ExperimentalPusherRight,ExperimentalPusherLeft,
    ExperimentalPusherUp,ExperimentalPusherBack,ExperimentalPusherFront,Button,
    StickyPusherFront,StickyPusherBack,StickyPusherUp,StickyPusherRight,StickyPusherLeft,Chemicals,Bush]#,ExperimentalPusherLeft]
    #block_index = 0
    mc = pygame.time.Clock()
    glColor(1.0,1.0,1.0,1.0)
    glBindTexture(GL_TEXTURE_2D, block_tex)
    while True:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        glLoadIdentity()
        glTranslate(0,0,-2)
        glRotate(30,1,0,0)
        glRotate(a, 0,1,0)
        cb = blocklist[block_index]
        render_lamocube(cb.coords_fwd,cb.coords_bck,cb.coords_btm,cb.coords_top,cb.coords_lft,cb.coords_rgt)
        pygame.display.flip()
        a+=2
        mc.tick(30)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    glClearColor(0.45, 0.7, 1.0, 0.0)
                    return blocklist[block_index], block_index
                if event.key == K_LEFT:
                    block_index-=1
                    if block_index == -1: block_index=len(blocklist)-1
                if event.key == K_RIGHT:
                    block_index += 1
                    if block_index == len(blocklist): block_index=0

def remote_start(world,textures):
    flying=False
    carrying = BasicBlock
    block_i = 0
    thread_run = True
    waterFirst = True
    pygame.mouse.set_visible(False)
    #pygame.mouse.set_grab(True)
    clock = pygame.time.Clock()
    world.recompile("The Master")
    whammer = FastCube([0,0,0])
    color_data = {}
    background = 0.45, 0.7, 1.0,1.0
    sky = 1.0
    sky_inc = -0.0005
    night = False
    p=pygame.key.get_pressed()
    s=None

    frame_num=0
    while True:
        frame_num+=1
        ms = clock.tick(30)
        GRAVITY_ACCEL = 0.01
        GRAVITY_H2O = 0.0025
        JUMPSTART = -0.2
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runQuit(world)
            if event.type == KEYDOWN:
                if event.key == K_z:
                    night = not night
                if event.key == K_ESCAPE:
                    runQuit(world)
                if event.key == K_b:
                    carrying, block_i = blockSelector(block_i,textures["blocks"])
                if event.key == K_m:
                    world.spawn_point = world.player_pos[:]
                if event.key == K_n:
                    world.player_pos = world.spawn_point[:]
                    world.player_accel=0
                if event.key == K_v:
                    pygame.event.post(pygame.event.Event(MOUSEBUTTONDOWN,button=1))
                if event.key == K_c:
                    pygame.event.post(pygame.event.Event(MOUSEBUTTONDOWN,button=3))
                if event.key == K_e and s:
                    #print "!"
                    
                    if s.usable:
                        #print "!!"
                        s.on_use()
                if event.key == K_F3:
                    flying=not flying
                if event.key == K_SPACE and canjump:
                    world.player_accel = -0.2
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (event.button == 1) and s:
                    world.killBlock(s,True)
                    
                    s=world.trackPointer()
                if (event.button == 3) and s:
                    y = trace(s.pos,world)
                    #print y
                    try:carrying((s.pos[0]+color_index[y][0],s.pos[1]+color_index[y][1],s.pos[2]+color_index[y][2]),world)
                    except Exception as e: print "Error: ", str(e)
                    glClear(GL_COLOR_BUFFER_BIT)

        glClearColor(*background)

        pygame.display.set_caption("PYCRAFT 3            FPS: "+str(clock.get_fps()))
        
        if night: world.doSky()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        
        
        glLoadIdentity();

        glColor(1,1,1)
        glRotate(world.player_angle[0],1,0,0)
        glRotate(world.player_angle[1],0,1,0)
        glTranslate(-world.player_pos[0],-world.player_pos[1],world.player_pos[2])
        #glColor(0,0,0.6)
        glDisable(GL_TEXTURE_2D)
        #glBegin(GL_QUADS)
        #glVertex3d(-1000,,-1000)
        #glVertex3d(1000,0,-1000)
        #glVertex3d(1000,0,1000)
        #glVertex3d(-1000,0,1000)
        #glEnd()
        glEnable(GL_TEXTURE_2D)
        CLOUD = 1000.0
        CLDH = 500.0
        glDisable(GL_FOG)
        glBindTexture(GL_TEXTURE_2D,textures["sky"])
        glBegin(GL_QUADS)
        glTexCoord2f(0.0,0.0); glVertex3f(-CLOUD,CLDH,-CLOUD)
        glTexCoord2f(1.0,0.0); glVertex3f(CLOUD,CLDH,-CLOUD)
        glTexCoord2f(1.0,1.0); glVertex3f(CLOUD,CLDH,CLOUD)
        glTexCoord2f(0.0,1.0); glVertex3f(-CLOUD,CLDH,CLOUD)               
        glEnd()
        glEnable(GL_FOG)
        if world.getAmbient()==(1.0,1.0,1.0,1.0):glBindTexture(GL_TEXTURE_2D, textures["blocks"])
        else: glBindTexture(GL_TEXTURE_2D, textures["water"])
        if world.needs_update: world.recompile("The Master #2")
        #glEnable(GL_LIGHTING)
        #glLight(GL_LIGHT0, GL_POSITION,  (0, 1.25, 1, 0))
        world.render()
        glDisable(GL_LIGHTING)
        #glDisable(GL_TEXTURE_2D)
        #print world.particles
        glPointSize(50)
        glEnable(GL_POINT_SPRITE)
        glPointParameterfv(GL_POINT_DISTANCE_ATTENUATION,(0,0,0.35))
        glBegin(GL_POINTS)
        for particle in world.particles[:]:
            particle.update()
            particle.render()
        glEnd()
        glEnable(GL_TEXTURE_2D)
        world.updateOneRandomBlock()
        s = world.trackPointer()
        #s=None
        if s:
            #print frame_num,"\t", s.pos
            glColor(0,0,0)
            glBegin(GL_LINES)
            glVertex3f(s.pos[0]-SELECTSIZE,s.pos[1]-SELECTSIZE, s.pos[2]-SELECTSIZE); glVertex3f(s.pos[0]+SELECTSIZE,s.pos[1]-SELECTSIZE, s.pos[2]-SELECTSIZE)
            glVertex3f(s.pos[0]+SELECTSIZE,s.pos[1]-SELECTSIZE, s.pos[2]-SELECTSIZE); glVertex3f(s.pos[0]+SELECTSIZE,s.pos[1]-SELECTSIZE, s.pos[2]+SELECTSIZE)
            glVertex3f(s.pos[0]+SELECTSIZE,s.pos[1]-SELECTSIZE, s.pos[2]+SELECTSIZE); glVertex3f(s.pos[0]-SELECTSIZE,s.pos[1]-SELECTSIZE, s.pos[2]+SELECTSIZE)
            glVertex3f(s.pos[0]-SELECTSIZE,s.pos[1]-SELECTSIZE, s.pos[2]+SELECTSIZE); glVertex3f(s.pos[0]-SELECTSIZE,s.pos[1]-SELECTSIZE, s.pos[2]-SELECTSIZE)
            
            glVertex3f(s.pos[0]-SELECTSIZE,s.pos[1]+SELECTSIZE, s.pos[2]-SELECTSIZE); glVertex3f(s.pos[0]+SELECTSIZE,s.pos[1]+SELECTSIZE, s.pos[2]-SELECTSIZE)
            glVertex3f(s.pos[0]+SELECTSIZE,s.pos[1]+SELECTSIZE, s.pos[2]-SELECTSIZE); glVertex3f(s.pos[0]+SELECTSIZE,s.pos[1]+SELECTSIZE, s.pos[2]+SELECTSIZE)
            glVertex3f(s.pos[0]+SELECTSIZE,s.pos[1]+SELECTSIZE, s.pos[2]+SELECTSIZE); glVertex3f(s.pos[0]-SELECTSIZE,s.pos[1]+SELECTSIZE, s.pos[2]+SELECTSIZE)
            glVertex3f(s.pos[0]-SELECTSIZE,s.pos[1]+SELECTSIZE, s.pos[2]+SELECTSIZE); glVertex3f(s.pos[0]-SELECTSIZE,s.pos[1]+SELECTSIZE, s.pos[2]-SELECTSIZE)
            
            glVertex3f(s.pos[0]-SELECTSIZE,s.pos[1]-SELECTSIZE, s.pos[2]-SELECTSIZE); glVertex3f(s.pos[0]-SELECTSIZE,s.pos[1]+SELECTSIZE, s.pos[2]-SELECTSIZE);
            glVertex3f(s.pos[0]+SELECTSIZE,s.pos[1]-SELECTSIZE, s.pos[2]-SELECTSIZE); glVertex3f(s.pos[0]+SELECTSIZE,s.pos[1]+SELECTSIZE, s.pos[2]-SELECTSIZE);
            glVertex3f(s.pos[0]+SELECTSIZE,s.pos[1]-SELECTSIZE, s.pos[2]+SELECTSIZE); glVertex3f(s.pos[0]+SELECTSIZE,s.pos[1]+SELECTSIZE, s.pos[2]+SELECTSIZE);
            glVertex3f(s.pos[0]-SELECTSIZE,s.pos[1]-SELECTSIZE, s.pos[2]+SELECTSIZE); glVertex3f(s.pos[0]-SELECTSIZE,s.pos[1]+SELECTSIZE, s.pos[2]+SELECTSIZE);
            glEnd()     
        glLoadIdentity();
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_TEXTURE_2D)
        glBegin(GL_QUADS);
        glColor(0,0,0.25);
        glVertex3f(0,0.05,-3)
        glVertex3f(0.05,0,-3)
        glVertex3f(0,-0.05,-3)
        glVertex3f(-0.05,0,-3)
        glEnd()
        glEnable(GL_TEXTURE_2D)
        glColor(1,1,1,1)
        glEnable(GL_DEPTH_TEST)
        
        pygame.display.flip()
        
        p=pygame.key.get_pressed()
        m=pygame.mouse.get_rel()
        world.player_angle[1] += m[0] / 2
        world.player_angle[0] += m[1] / 2
        world.player_angle[0] = min(world.player_angle[0],90)
        world.player_angle[0] = max(world.player_angle[0],-90)
        opos = world.player_pos[:]
        if p[K_LSHIFT]: WALK_SPEED = 0.5
        else: WALK_SPEED = 0.15
        if p[K_w]:
            world.player_pos[0] += sin(radians(world.player_angle[1])) *WALK_SPEED
            if world.getCollide(): world.player_pos[0]=opos[0]
            world.player_pos[2] += cos(radians(world.player_angle[1])) *WALK_SPEED
            if world.getCollide(): world.player_pos[2]=opos[2]
        elif p[K_s]:
            world.player_pos[0] -= sin(radians(world.player_angle[1])) *WALK_SPEED
            if world.getCollide(): world.player_pos[0]=opos[0]
            world.player_pos[2] -= cos(radians(world.player_angle[1])) *WALK_SPEED
            if world.getCollide(): world.player_pos[2]=opos[2]
        elif p[K_a]:
            world.player_pos[0] += sin(radians(world.player_angle[1]-90)) *WALK_SPEED
            if world.getCollide(): world.player_pos[0]=opos[0]
            world.player_pos[2] += cos(radians(world.player_angle[1]-90)) *WALK_SPEED
            if world.getCollide(): world.player_pos[2]=opos[2]
        elif p[K_d]:
            world.player_pos[0] -= sin(radians(world.player_angle[1]-90)) *WALK_SPEED
            if world.getCollide(): world.player_pos[0]=opos[0]
            world.player_pos[2] -= cos(radians(world.player_angle[1]-90)) *WALK_SPEED
            if world.getCollide(): world.player_pos[2]=opos[2]
        if p[K_SPACE]:
            if canjump:
                world.player_accel = JUMPSTART
        if p[K_r] and flying: 
            world.player_pos[1] += WALK_SPEED
            if world.getCollide():
                world.player_pos[1] = opos[1]
        if p[K_f] and flying: 
            world.player_pos[1] -= WALK_SPEED
            if world.getCollide():
                world.player_pos[1] = opos[1]
        world.player_accel = min(world.player_accel,0.5)
        world.player_pos[1] -= world.player_accel
        canjump=False
        if not flying:
            if world.getRoundedPos(0,-1.6,0) in world.blocks.keys():
                canjump=True
            if world.getRoundedPos() not in world.blocks.keys():
                waterFirst=True
        if not world.getCollide() and not flying:
            y= world.getBlockAt(world.getRoundedPos())
            if y:
                if y.ag:
                    if waterFirst:
                        waterFirst = False
                        world.player_accel = 0
                    else:
                        #print "!!"
                        world.player_accel += GRAVITY_H2O
                else:
                    world.player_accel += GRAVITY_ACCEL
            else:
                world.player_accel += GRAVITY_ACCEL
        
        if world.getCollide(): 
                world.player_accel=0
                world.player_pos[1] = round(opos[1])+0.001
        
        if p[K_UP]: world.player_angle[0] -=3
        if p[K_DOWN] :world.player_angle[0] += 3
        if p[K_RIGHT] :world.player_angle[1] += 3
        if p[K_LEFT]: world.player_angle[1] -= 3
##        world.particles.append(SimpleParticle(world,
##                                                     (randint(int(world.player_pos[0]-10),int(world.player_pos[0]+10)),
##                                                      randint(int(world.player_pos[1]+10),int(world.player_pos[1]+20)),
##                                                      randint(int(world.player_pos[2]-10),int(world.player_pos[2]+10))),
##                                                     Water.coords_top[:2]))
        
   
def remote_main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE,HWSURFACE|OPENGL|DOUBLEBUF)
    resize(*SCREEN_SIZE)
    init()

    world = BasicWorldManager([])
    getFile(world)

    screen = pygame.display.set_mode(SCREEN_SIZE,HWSURFACE|OPENGL|DOUBLEBUF|FULLSCREEN)
    pygame.event.set_grab(True)
    resize(*SCREEN_SIZE)
    init()
    glEnable(GL_TEXTURE_2D)

    texture_surface = pygame.image.load("texture packs/"+data[0].strip()+".png")
    texture_data = pygame.image.tostring(texture_surface, 'RGBA', True)
    block_tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, block_tex)
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST )
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    width, height = texture_surface.get_rect().size
    t2 = time()
    glTexImage2D( GL_TEXTURE_2D,0,4,width,height,0,GL_RGBA,GL_UNSIGNED_BYTE,texture_data)
    t1 = time()
    #font_surface = pygame.image.load("fonts/ascii_square.png")
    #font_data = pygame.image.tostring(font_surface, 'RGBA', True)
    #font_tex = glGenTextures(1)
    #glBindTexture(GL_TEXTURE_2D, font_tex)
    #glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST )
    #glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST )
    #glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    #wf, hf = font_surface.get_rect().size
    #glTexImage2D( GL_TEXTURE_2D,0,4,wf,hf,0,GL_RGBA,GL_UNSIGNED_BYTE,font_data)
    sky_surface = pygame.image.load("skytop/skytop3.png")
    sky_data = pygame.image.tostring(sky_surface, 'RGB', True)
    sky_tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, sky_tex)
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST )
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    wf2, hf2 = sky_surface.get_rect().size
    glTexImage2D( GL_TEXTURE_2D,0,3,wf2,hf2,0,GL_RGB,GL_UNSIGNED_BYTE,sky_data)
    w_surface = pygame.image.load("texture packs/"+data[0].strip()+"W.png")
    w_data = pygame.image.tostring(w_surface, 'RGB', True)
    w_tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, w_tex)
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST )
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    wf2, hf2 = w_surface.get_rect().size
    glTexImage2D( GL_TEXTURE_2D,0,3,wf2,hf2,0,GL_RGB,GL_UNSIGNED_BYTE,w_data)

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBlendEquation(GL_FUNC_ADD)

    tex_dict = {
        "blocks":block_tex,
        "water":w_tex,
        "sky":sky_tex}
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLight(GL_LIGHT0, GL_POSITION,  (0, 1, 1, 0))
    glEnable(GL_FOG)
    glFogfv(GL_FOG_COLOR, (0.45, 0.7, 1.0, 1.0))
    glFogi(GL_FOG_MODE, GL_LINEAR)
    glFogf(GL_FOG_START, 2)
    glFogf(GL_FOG_END, 40)
    glEnable(GL_ALPHA_TEST)
    glAlphaFunc(GL_GREATER,0.5)
    glLineWidth(1)
    remote_start(world,tex_dict)
    

        

        
        
    
    
    
