from OpenGL.GL import *
from OpenGL.GLU import *
SCREEN_SIZE=[800,600]

##def eventHandler():
##    global thread_run
##    for event in pygame.event.get():
##        if event.type == pygame.QUIT:
##            thread_run=False
##            quit()
##        if event.type == KEYDOWN:
##            if event.key == K_ESCAPE:
##                thread_run=False
##                quit()
RATE=1
class CubeThingy:
    coords_top=[RATE*1,RATE*15,RATE*2,RATE*14]
    coords_btm=[RATE*1,RATE*15,RATE*2,RATE*14]
    coords_lft=[RATE*1,RATE*15,RATE*2,RATE*14]
    coords_rgt=[RATE*1,RATE*15,RATE*2,RATE*14]
    coords_fwd=[RATE*1,RATE*15,RATE*2,RATE*14]
    coords_bck=[RATE*1,RATE*15,RATE*2,RATE*14]
    o_solid=True
    o_dynamic=False
    o_usable=False
    o_changesTo=None
    o_glows=0
    o_breakFall=False
    o_name="Totally Boring"
    def __init__(self,pos,world,create=True,recompile=True):
        self.pos=pos
        #self.world=world
        self.solid=self.o_solid
        self.name=self.o_name
        self.dynamic=self.o_dynamic
        self.usable=self.o_usable
        self.changesTo = self.o_changesTo
        #if self.changesTo: self.countdown=randint(30,60)
        self.glows=self.o_glows
        self.breakFall = self.o_breakFall
        #if create:self.world.setBlockAt(self,recompile)
        #self.render()
    def __str__(self): return self.o_name
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


def resize(width, height):

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(width)/height, .1, 1000.)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init():

    glEnable(GL_TEXTURE_2D)
    glClearColor(0.45, 0.7, 1.0, 0.0)
    glEnable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)
    
def updateThread():
    global world
    world.updateOneRandomBlock()

def buildThread():
    pass

resize(800,600)
init()
def trace(pos,world):
    mycube=CubeThingy(pos,None,False,False)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity();
    glRotate(world.player_angle[0],1,0,0)
    glRotate(world.player_angle[1],0,1,0)
    glTranslate(-world.player_pos[0],-world.player_pos[1],world.player_pos[2])
    #glBindTexture(GL_TEXTURE_2D, texture_id)
    mycube.render_index()
    pixels=[0,0,0,0]
    return tuple(glReadPixels(SCREEN_SIZE[0]/2,SCREEN_SIZE[1]/2,1,1,GL_RGBA,GL_UNSIGNED_BYTE,pixels))
    
    
