pygame.mixer.init(channels=64)
#kaboom = pygame.mixer.Sound("sounds/EXPLODE.WAV")

class BlockError(Exception): pass

PASTELS = [
        (0.8,0.8,0.8,1.0),
        (0.7,0.9,1.0,1.0),
        (0.7,0.9,0.9,1.0),
        (0.9,0.7,0.8,1.0),
        (0.7,0.9,0.8,1.0),
        (0.7,1.0,0.7,1.0)]

def ro(): return (random()-0.5)*0.2

class BasicBlock:
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
    index=0
    ag=False
    trans = False
    cutoff = True
    dcutoff=True
    o_combust = -1
    particle_colors = [(0.5,0.5,0.5,1.0),(0.75,0.75,0.75,1.0)]
    def getState(self):
        #print "Ungghhhh!"
        return 0
    def getE(self):
        return (0,0,0,0,0,0)
    #o_linked=[]
    def __init__(self,pos,world,create=True,recompile=True,state=0):
        self.pos=pos
        self.world=world
        self.solid=self.o_solid
        self.name=self.o_name
        self.dynamic=self.o_dynamic
        self.usable=self.o_usable
        self.changesTo = self.o_changesTo
        if self.changesTo: self.countdown=randint(30,60)
        self.glows=self.o_glows
        self.breakFall = self.o_breakFall
        if create:self.world.setBlockAt(self,recompile)
        self.render()
        self.linked=[]
        self.burn_counter = 0

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

    def render(self):
        #glBegin(GL_QUADS)
        #glColor(0.5,0.5,0.5,1.0);
        glNormal3f(0,0,-1)
        glColor(0.8,0.8,0.8)

        try:
            if not self.world.getBlockAt((self.pos[0],self.pos[1],self.pos[2]+1)).cutoff: raise BlockError
        except:
            #p#rint "Front!"
            glTexCoord2d(self.coords_fwd[0],self.coords_fwd[3]); glVertex3f(self.pos[0]+ -0.5,self.pos[1]+-0.5,self.pos[2]+0.5) #Front
            glTexCoord2d(self.coords_fwd[2],self.coords_fwd[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
            glTexCoord2d(self.coords_fwd[2],self.coords_fwd[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
            glTexCoord2d(self.coords_fwd[0],self.coords_fwd[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glNormal3f(0,0,1)
        glColor(0.6,0.6,0.6)
        try:
            if not self.world.getBlockAt((self.pos[0],self.pos[1],self.pos[2]-1)).cutoff: raise BlockError
        except:
            glTexCoord2d(self.coords_bck[2],self.coords_bck[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
            glTexCoord2d(self.coords_bck[0],self.coords_bck[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5) #Back
            glTexCoord2d(self.coords_bck[0],self.coords_bck[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
            glTexCoord2d(self.coords_bck[2],self.coords_bck[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glNormal3f(0,-1,0)
        try:
            if not self.world.getBlockAt((self.pos[0],self.pos[1]-1,self.pos[2])).cutoff: raise BlockError
        except:
            glTexCoord2d(self.coords_btm[2],self.coords_btm[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5) #Bottom
            glTexCoord2d(self.coords_btm[0],self.coords_btm[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
            glTexCoord2d(self.coords_btm[0],self.coords_btm[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
            glTexCoord2d(self.coords_btm[2],self.coords_btm[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glNormal3f(0,1,0)
        glColor(1,1,1)
        try:
            if not self.world.getBlockAt((self.pos[0],self.pos[1]+1,self.pos[2])).cutoff: raise BlockError
        except:
            glTexCoord2d(self.coords_top[0],self.coords_top[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #Top
            glTexCoord2d(self.coords_top[2],self.coords_top[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
            glTexCoord2d(self.coords_top[2],self.coords_top[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
            glTexCoord2d(self.coords_top[0],self.coords_top[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glNormal3f(-1,0,0)
        glColor(0.8,0.8,0.8)
        try:
            if not self.world.getBlockAt((self.pos[0]-1,self.pos[1],self.pos[2])).cutoff: raise BlockError
        except:
            glTexCoord2d(self.coords_lft[0],self.coords_lft[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
            glTexCoord2d(self.coords_lft[0],self.coords_lft[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #left
            glTexCoord2d(self.coords_lft[2],self.coords_lft[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
            glTexCoord2d(self.coords_lft[2],self.coords_lft[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glNormal3f(1,0,0)
        glColor(0.7,0.7,0.7)
        try:
            if not self.world.getBlockAt((self.pos[0]+1,self.pos[1],self.pos[2])).cutoff: raise BlockError
        except:
            glTexCoord2d(self.coords_rgt[2],self.coords_rgt[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
            glTexCoord2d(self.coords_rgt[2],self.coords_rgt[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #right
            glTexCoord2d(self.coords_rgt[0],self.coords_rgt[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
            glTexCoord2d(self.coords_rgt[0],self.coords_rgt[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        #glEnd() 

    def on_kill(self):
        pass

class Bush(BasicBlock):
    o_dynamic= False
    cutoff = False
    index = 54
    trans= True
    coords_fwd=[RATE*0,RATE*4,RATE*1,RATE*3]
    coords_lft=[RATE*0,RATE*4,RATE*1,RATE*3]

    coords_top=[RATE*0,RATE*4,RATE*1,RATE*3]
    coords_btm=[RATE*0,RATE*4,RATE*1,RATE*3]
    coords_rgt=[RATE*0,RATE*4,RATE*1,RATE*3]
    coords_bck=[RATE*0,RATE*4,RATE*1,RATE*3]
    def render(self):
        glTexCoord2f(self.coords_lft[0],self.coords_lft[3]); glVertex3f(self.pos[0],self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_lft[0],self.coords_lft[1]); glVertex3f(self.pos[0],self.pos[1]+0.5,self.pos[2]+-0.5) #left
        glTexCoord2f(self.coords_lft[2],self.coords_lft[1]); glVertex3f(self.pos[0],self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_lft[2],self.coords_lft[3]); glVertex3f(self.pos[0],self.pos[1]+-0.5,self.pos[2]+0.5)
        
        glTexCoord2f(self.coords_fwd[0],self.coords_fwd[3]); glVertex3f(self.pos[0]+ -0.5,self.pos[1]+-0.5,self.pos[2]) #Front
        glTexCoord2f(self.coords_fwd[2],self.coords_fwd[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2])
        glTexCoord2f(self.coords_fwd[2],self.coords_fwd[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2])
        glTexCoord2f(self.coords_fwd[0],self.coords_fwd[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2])

class Chemicals(BasicBlock):
    particle_colors = [(0,1,0),(0,0.5,0),(0,0.75,0)]
    o_dynamic = True
    coords_top=[RATE*0,RATE*3,RATE*1,RATE*2]
    coords_btm=[RATE*0,RATE*3,RATE*1,RATE*2]
    coords_lft=[RATE*1,RATE*3,RATE*2,RATE*2]
    coords_rgt=[RATE*1,RATE*3,RATE*2,RATE*2]
    coords_fwd=[RATE*1,RATE*3,RATE*2,RATE*2]
    coords_bck=[RATE*1,RATE*3,RATE*2,RATE*2]
    index = 53
    cutoff = False
    o_solid=False
    def __init__(self,pos,world,create=True,recompile=True,state=0):
        self.count = randint(0,7)
        self.mcount=randint(0,3)
        self.burnmode = [1,1,1,1]
        BasicBlock.__init__(self,pos,world,create,False)
    def on_dynamic_update(self):
        pass
        if randint(1,5)==2:
            if randint(1,3)==2: delta = choice(([-1,0,0],[1,0,0],[0,0,1],[0,0,-1],[0,1,0],[-1,1,0],[1,1,0],[0,1,1],[0,1,-1]))
            else:delta = choice(([0,1,0],[-1,1,0],[1,1,0],[0,1,1],[0,1,-1]))
            block = self.world.getBlockAt((self.pos[0]+delta[0],self.pos[1]+delta[1],self.pos[2]+delta[2]))
            if not block:
                delta2 = choice(([-1,0,0],[1,0,0],[0,0,1],[0,0,-1],[0,-1,0]))
                block2 = self.world.getBlockAt((self.pos[0]+delta[0]+delta2[0],self.pos[1]+delta[1]+delta2[1],self.pos[2]+delta[2]+delta2[2]))
                if block2:
                    if block2.index != 53:
                        y=Chemicals((self.pos[0]+delta[0],self.pos[1]+delta[1],self.pos[2]+delta[2]),self.world,recompile=False)
                        #if delta2[0]-delta[0] == 1:
                        #    y.burnmode=1
        rdelta = choice(((-1,0,0),(1,0,0),(0,0,1),(0,0,-1),(0,-1,0)))
        block = self.world.getBlockAt((self.pos[0]+rdelta[0],self.pos[1]+rdelta[1],self.pos[2]+rdelta[2]))
        if block:
            #print rdelta, block.index
            if block.index != 53:
                if self.burnmode != None:
                    if rdelta == (0,0,-1):
                        #print "!!!!!" 
                        self.burnmode[3] = 1
                    elif rdelta==(0,0,1):
                        self.burnmode[2] = 1
                    elif rdelta==(-1,0,0):
                        self.burnmode[1] = 1
                    elif rdelta==(1,0,0):
                        self.burnmode[0] = 1
                    elif rdelta==(0,-1,0):
                        self.burnmode = None
            if block.index==20:
                if block.countdown == -1:
                    block.on_use()
        else:
            if self.burnmode != None:
                if rdelta == (0,0,-1):
                    #print "!!!!!"
                    self.burnmode[3] = 0
                elif rdelta==(0,0,1):
                    self.burnmode[2] = 0
                elif rdelta==(-1,0,0):
                    self.burnmode[1] = 0
                elif rdelta==(1,0,0):
                    self.burnmode[0] = 0
                elif rdelta==(0,-1,0):
                    self.burnmode = [1,1,1,1]
    def render(self):
        self.mcount+=1
        if self.mcount==4:
            self.mcount=0
            self.count += 1
        self.count = self.count % 8
        if self.burnmode==None:
            glTexCoord2f(self.coords_lft[0]+(RATE*self.count),self.coords_lft[3]); glVertex3f(self.pos[0]-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
            glTexCoord2f(self.coords_lft[0]+(RATE*self.count),self.coords_lft[1]); glVertex3f(self.pos[0]-0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #left
            glTexCoord2f(self.coords_lft[2]+(RATE*self.count),self.coords_lft[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
            glTexCoord2f(self.coords_lft[2]+(RATE*self.count),self.coords_lft[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
            
            glTexCoord2f(self.coords_fwd[0]+(RATE*self.count),self.coords_fwd[3]); glVertex3f(self.pos[0]+ -0.5,self.pos[1]+-0.5,self.pos[2]+0.5) #Front
            glTexCoord2f(self.coords_fwd[2]+(RATE*self.count),self.coords_fwd[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]-0.5)
            glTexCoord2f(self.coords_fwd[2]+(RATE*self.count),self.coords_fwd[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]-0.5)
            glTexCoord2f(self.coords_fwd[0]+(RATE*self.count),self.coords_fwd[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        else:
            if self.burnmode[0]:
                glTexCoord2f(self.coords_fwd[0]+(RATE*self.count),self.coords_fwd[3]); glVertex3f(self.pos[0]+ -0.5,self.pos[1]+-0.5,self.pos[2]-0.5) #Front
                glTexCoord2f(self.coords_fwd[2]+(RATE*self.count),self.coords_fwd[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]-0.5)
                glTexCoord2f(self.coords_fwd[2]+(RATE*self.count),self.coords_fwd[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]-0.4)
                glTexCoord2f(self.coords_fwd[0]+(RATE*self.count),self.coords_fwd[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]-0.4)
            if self.burnmode==[1]:
                glTexCoord2f(self.coords_fwd[0]+(RATE*self.count),self.coords_fwd[3]); glVertex3f(self.pos[0]+ -0.5,self.pos[1]+-0.5,self.pos[2]+0.5) #Front
                glTexCoord2f(self.coords_fwd[2]+(RATE*self.count),self.coords_fwd[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
                glTexCoord2f(self.coords_fwd[2]+(RATE*self.count),self.coords_fwd[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.4)
                glTexCoord2f(self.coords_fwd[0]+(RATE*self.count),self.coords_fwd[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.4)
            if self.burnmode==[2]:
                glTexCoord2f(self.coords_fwd[0]+(RATE*self.count),self.coords_fwd[3]); glVertex3f(self.pos[0] -0.5,self.pos[1]+-0.5,self.pos[2]+0.5) #Front
                glTexCoord2f(self.coords_fwd[2]+(RATE*self.count),self.coords_fwd[3]); glVertex3f(self.pos[0]-0.5,self.pos[1]+-0.5,self.pos[2]-0.5)
                glTexCoord2f(self.coords_fwd[2]+(RATE*self.count),self.coords_fwd[1]); glVertex3f(self.pos[0]-0.4,self.pos[1]+0.5,self.pos[2]-0.5)
                glTexCoord2f(self.coords_fwd[0]+(RATE*self.count),self.coords_fwd[1]); glVertex3f(self.pos[0]-0.4,self.pos[1]+0.5,self.pos[2]+0.5)
            if self.burnmode==[3]:
                glTexCoord2f(self.coords_fwd[0]+(RATE*self.count),self.coords_fwd[3]); glVertex3f(self.pos[0] +0.5,self.pos[1]+-0.5,self.pos[2]+0.5) #Front
                glTexCoord2f(self.coords_fwd[2]+(RATE*self.count),self.coords_fwd[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]-0.5)
                glTexCoord2f(self.coords_fwd[2]+(RATE*self.count),self.coords_fwd[1]); glVertex3f(self.pos[0]+0.4,self.pos[1]+0.5,self.pos[2]-0.5)
                glTexCoord2f(self.coords_fwd[0]+(RATE*self.count),self.coords_fwd[1]); glVertex3f(self.pos[0]+0.4,self.pos[1]+0.5,self.pos[2]+0.5)
class StickyPusherLeft(BasicBlock):
    particle_colors = [(0.3,0.14,0.0)]
    coords_top=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_btm=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_lft=[RATE*8,RATE*14,RATE*9,RATE*13]
    coords_rgt=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_fwd=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_bck=[RATE*6,RATE*13,RATE*7,RATE*12]
    index=52
    o_name="Sticky"
    o_dynamic = True
    def __init__(self,pos,world,create=True,recompile=True,state=0):
        self.state=False
        BasicBlock.__init__(self,pos,world,create,False)
    def on_dynamic_update(self):
        if sum(self.world.getNeighboringCurrents(self.pos)):
            self.state=True
            y= self.world.getBlockAt((self.pos[0]-1,self.pos[1],self.pos[2]))
            d = 1
            shoved = []
            while y:
                self.world.killBlock(y,recompile=False)
                y.pos = (y.pos[0]-1,y.pos[1],y.pos[2])
                #self.world.setBlockAt(y,recompile=False)
                shoved.append(y)
                d+=1
                y= self.world.getBlockAt((self.pos[0]-d,self.pos[1],self.pos[2]))
            for block in shoved: self.world.setBlockAt(block,recompile=False)
            if shoved:self.world.recompile()
        else:
            out = self.world.getBlockAt((self.pos[0]-1,self.pos[1],self.pos[2]))
            out2 = self.world.getBlockAt((self.pos[0]-2,self.pos[1],self.pos[2]))
            if out2 is None: self.state=False
            if out2 and not out:
                try:
                    if out2.name=="Sticky":
                        if not out2.state:raise TypeError,"Huhu!"
                    else:
                        raise TypeError, "Uiyipe!"
                except Exception as e:
                    print e
                    self.state=False
                    self.world.killBlock(out2,recompile=False)
                    out2.pos = (out2.pos[0]+1,out2.pos[1],out2.pos[2])
                    self.world.setBlockAt(out2,recompile=False)
                    self.world.recompile()
            else:self.state=False
class StickyPusherRight(BasicBlock):
    particle_colors = [(0.3,0.14,0.0)]
    coords_top=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_btm=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_lft=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_rgt=[RATE*8,RATE*14,RATE*9,RATE*13]
    coords_fwd=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_bck=[RATE*6,RATE*13,RATE*7,RATE*12]
    index=51
    o_name="Sticky"
    o_dynamic = True
    def __init__(self,pos,world,create=True,recompile=True,state=0):
        self.state=False
        BasicBlock.__init__(self,pos,world,create,False)
    def on_dynamic_update(self):
        if sum(self.world.getNeighboringCurrents(self.pos)):
            self.state=True
            y= self.world.getBlockAt((self.pos[0]+1,self.pos[1],self.pos[2]))
            d = 1
            shoved = []
            while y:
                self.world.killBlock(y,recompile=False)
                y.pos = (y.pos[0]+1,y.pos[1],y.pos[2])
                #self.world.setBlockAt(y,recompile=False)
                shoved.append(y)
                d+=1
                y= self.world.getBlockAt((self.pos[0]+d,self.pos[1],self.pos[2]))
            for block in shoved: self.world.setBlockAt(block,recompile=False)
            if shoved:self.world.recompile()
        else:
            out = self.world.getBlockAt((self.pos[0]+1,self.pos[1],self.pos[2]))
            out2 = self.world.getBlockAt((self.pos[0]+2,self.pos[1],self.pos[2]))
            if out2 is None: self.state=False
            if out2 and not out:
                try:
                    if out2.name=="Sticky":
                        if not out2.state:raise TypeError,"Huhu!"
                    else:
                        raise TypeError, "Uiyipe!"
                except Exception as e:
                    print e
                    self.state=False
                    self.world.killBlock(out2,recompile=False)
                    out2.pos = (out2.pos[0]-1,out2.pos[1],out2.pos[2])
                    self.world.setBlockAt(out2,recompile=False)
                    self.world.recompile()
            else:self.state=False
class StickyPusherBack(BasicBlock):
    particle_colors = [(0.3,0.14,0.0)]
    coords_top=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_btm=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_lft=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_rgt=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_fwd=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_bck=[RATE*8,RATE*14,RATE*9,RATE*13]
    index=50
    o_name="Sticky"
    o_dynamic = True
    def __init__(self,pos,world,create=True,recompile=True,state=0):
        self.state=False
        BasicBlock.__init__(self,pos,world,create,False)
    def on_dynamic_update(self):
        if sum(self.world.getNeighboringCurrents(self.pos)):
            self.state=True
            y= self.world.getBlockAt((self.pos[0],self.pos[1],self.pos[2]-1))
            d = 1
            shoved = []
            while y:
                self.world.killBlock(y,recompile=False)
                y.pos = (y.pos[0],y.pos[1],y.pos[2]-1)
                #self.world.setBlockAt(y,recompile=False)
                shoved.append(y)
                d+=1
                y= self.world.getBlockAt((self.pos[0],self.pos[1],self.pos[2]-d))
            for block in shoved: self.world.setBlockAt(block,recompile=False)
            if shoved:self.world.recompile()
        else:
            out = self.world.getBlockAt((self.pos[0],self.pos[1],self.pos[2]-1))
            out2 = self.world.getBlockAt((self.pos[0],self.pos[1],self.pos[2]-2))
            if out2 is None: self.state=False
            if out2 and not out:
                try:
                    if out2.name=="Sticky":
                        if not out2.state:raise TypeError,"Huhu!"
                    else:
                        raise TypeError, "Uiyipe!"
                except Exception as e:
                    print e
                    self.state=False
                    self.world.killBlock(out2,recompile=False)
                    out2.pos = (out2.pos[0],out2.pos[1],out2.pos[2]+1)
                    self.world.setBlockAt(out2,recompile=False)
                    self.world.recompile()
            else:self.state=False
class StickyPusherUp(BasicBlock):
    particle_colors = [(0.14,0.3,0.0)]
    coords_top=[RATE*8,RATE*14,RATE*9,RATE*13]
    coords_btm=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_lft=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_rgt=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_fwd=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_bck=[RATE*6,RATE*13,RATE*7,RATE*12]
    index=49
    o_name="Sticky"
    o_dynamic = True
    def __init__(self,pos,world,create=True,recompile=True,state=0):
        self.state=False
        BasicBlock.__init__(self,pos,world,create,False)
    def on_dynamic_update(self):
        if sum(self.world.getNeighboringCurrents(self.pos)):
            self.state=True
            y= self.world.getBlockAt((self.pos[0],self.pos[1]+1,self.pos[2]))
            d = 1
            shoved = []
            while y:
                self.world.killBlock(y,recompile=False)
                y.pos = (y.pos[0],y.pos[1]+1,y.pos[2])
                #self.world.setBlockAt(y,recompile=False)
                shoved.append(y)
                d+=1
                y= self.world.getBlockAt((self.pos[0],self.pos[1]+d,self.pos[2]))
            for block in shoved: self.world.setBlockAt(block,recompile=False)
            if shoved:self.world.recompile()
        else:
            out = self.world.getBlockAt((self.pos[0],self.pos[1]+1,self.pos[2]))
            out2 = self.world.getBlockAt((self.pos[0],self.pos[1]+2,self.pos[2]))
            if out2 is None: self.state=False
            if out2 and not out:
                try:
                    if out2.name=="Sticky":
                        if not out2.state:raise TypeError,"Huhu!"
                    else:
                        raise TypeError, "Uiyipe!"
                except Exception as e:
                    print e
                    self.state=False
                    self.world.killBlock(out2,recompile=False)
                    out2.pos = (out2.pos[0],out2.pos[1]-1,out2.pos[2])
                    self.world.setBlockAt(out2,recompile=False)
                    self.world.recompile()
            else:self.state=False
class StickyPusherFront(BasicBlock):
    particle_colors = [(0.3,0.14,0.0)]
    coords_top=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_btm=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_lft=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_rgt=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_fwd=[RATE*8,RATE*14,RATE*9,RATE*13]
    coords_bck=[RATE*6,RATE*13,RATE*7,RATE*12]
    index=48
    o_name="Sticky"
    o_dynamic = True
    def __init__(self,pos,world,create=True,recompile=True,state=0):
        self.state=False
        BasicBlock.__init__(self,pos,world,create,False)
    def on_dynamic_update(self):
        if sum(self.world.getNeighboringCurrents(self.pos)):
            self.state=True
            y= self.world.getBlockAt((self.pos[0],self.pos[1],self.pos[2]+1))
            d = 1
            shoved = []
            while y:
                self.world.killBlock(y,recompile=False)
                y.pos = (y.pos[0],y.pos[1],y.pos[2]+1)
                #self.world.setBlockAt(y,recompile=False)
                shoved.append(y)
                d+=1
                y= self.world.getBlockAt((self.pos[0],self.pos[1],self.pos[2]+d))
            for block in shoved: self.world.setBlockAt(block,recompile=False)
            if shoved:self.world.recompile()
        else:
            out = self.world.getBlockAt((self.pos[0],self.pos[1],self.pos[2]+1))
            out2 = self.world.getBlockAt((self.pos[0],self.pos[1],self.pos[2]+2))
            if out2 is None: self.state=False
            if out2 and not out:
                try:
                    if out2.name=="Sticky":
                        if not out2.state:raise TypeError,"Huhu!"
                    else:
                        raise TypeError, "Uiyipe!"
                except Exception as e:
                    print e
                    self.state=False
                    self.world.killBlock(out2,recompile=False)
                    out2.pos = (out2.pos[0],out2.pos[1],out2.pos[2]-1)
                    self.world.setBlockAt(out2,recompile=False)
                    self.world.recompile()
            else:self.state=False
class DyedSand(BasicBlock):
    particle_colors = [(0.3,0.14,0.0)]
    coords_top=[RATE*9,RATE*15,RATE*10,RATE*14]
    coords_btm=[RATE*9,RATE*15,RATE*10,RATE*14]
    coords_lft=[RATE*9,RATE*15,RATE*10,RATE*14]
    coords_rgt=[RATE*9,RATE*15,RATE*10,RATE*14]
    coords_fwd=[RATE*9,RATE*15,RATE*10,RATE*14]
    coords_bck=[RATE*9,RATE*15,RATE*10,RATE*14]
    index = 47
    o_dynamic=True
    cutoff = False
    def on_dynamic_update(self):
            #print "Update:",
            if not self.world.getBlockAt((self.pos[0],self.pos[1]-1,self.pos[2])):
                #print "Yes"
                self.world.killBlock(self,recompile=False)
                self.pos = (self.pos[0],self.pos[1]-1,self.pos[2])
                self.world.setBlockAt(self,recompile=False)
            else:
                pass
class Button(BasicBlock):
    #particle_colors = [(0.3,0.3,0.0)]
    electric=True
    index=46
    coords_top=[RATE*7,RATE*15,RATE*8,RATE*14]
    coords_btm=[RATE*7,RATE*13,RATE*8,RATE*12]
    coords_lft=[RATE*7,RATE*13,RATE*8,RATE*12]
    coords_rgt=[RATE*7,RATE*13,RATE*8,RATE*12]
    coords_fwd=[RATE*7,RATE*13,RATE*8,RATE*12]
    coords_bck=[RATE*7,RATE*13,RATE*8,RATE*12]
    def getE(self):
        y = self.world.getBlockAt((self.pos[0],self.pos[1]+1,self.pos[2]))==None
        upper = (self.pos[0],self.pos[1]+2,self.pos[2])
        if  (self.world.getRoundedPos() == upper) or not y:
                return [1]*6
        else:
                return [0]*6
class ExperimentalPusherFront(BasicBlock):
    particle_colors = [(0.3,0.14,0.0)]
    coords_top=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_btm=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_lft=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_rgt=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_fwd=[RATE*5,RATE*14,RATE*6,RATE*13]
    coords_bck=[RATE*6,RATE*13,RATE*7,RATE*12]
    index=45
    o_dynamic = True
    def on_dynamic_update(self):
        if sum(self.world.getNeighboringCurrents(self.pos)):
            y= self.world.getBlockAt((self.pos[0],self.pos[1],self.pos[2]+1))
            d = 1
            shoved = []
            while y:
                self.world.killBlock(y,recompile=False)
                y.pos = (y.pos[0],y.pos[1],y.pos[2]+1)
                #self.world.setBlockAt(y,recompile=False)
                shoved.append(y)
                d+=1
                y= self.world.getBlockAt((self.pos[0],self.pos[1],self.pos[2]+d))
            for block in shoved: self.world.setBlockAt(block,recompile=False)
            if shoved:self.world.recompile()
class ExperimentalPusherBack(BasicBlock):
    particle_colors = [(0.3,0.14,0.0)]
    coords_top=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_btm=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_lft=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_rgt=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_fwd=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_bck=[RATE*5,RATE*14,RATE*6,RATE*13]
    index=44
    o_dynamic = True
    def on_dynamic_update(self):
        if sum(self.world.getNeighboringCurrents(self.pos)):
            y= self.world.getBlockAt((self.pos[0],self.pos[1],self.pos[2]-1))
            d = 1
            shoved = []
            while y:
                self.world.killBlock(y,recompile=False)
                y.pos = (y.pos[0],y.pos[1],y.pos[2]-1)
                #self.world.setBlockAt(y,recompile=False)
                shoved.append(y)
                d+=1
                y= self.world.getBlockAt((self.pos[0],self.pos[1],self.pos[2]-d))
            for block in shoved: self.world.setBlockAt(block,recompile=False)
            if shoved:self.world.recompile()
class ExperimentalPusherUp(BasicBlock):
    particle_colors = [(0.3,0.14,0.0)]
    coords_top=[RATE*5,RATE*14,RATE*6,RATE*13]
    coords_btm=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_lft=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_rgt=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_fwd=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_bck=[RATE*6,RATE*13,RATE*7,RATE*12]
    index=43
    o_dynamic = True
    def on_dynamic_update(self):
        if sum(self.world.getNeighboringCurrents(self.pos)):
            y= self.world.getBlockAt((self.pos[0],self.pos[1]+1,self.pos[2]))
            d = 1
            shoved = []
            while y:
                self.world.killBlock(y,recompile=False)
                y.pos = (y.pos[0],y.pos[1]+1,y.pos[2])
                #self.world.setBlockAt(y,recompile=False)
                shoved.append(y)
                d+=1
                y= self.world.getBlockAt((self.pos[0],self.pos[1]+d,self.pos[2]))
            for block in shoved: self.world.setBlockAt(block,recompile=False)
            if shoved:self.world.recompile()
class ExperimentalPusherLeft(BasicBlock):
    particle_colors = [(0.3,0.14,0.0)]
    coords_top=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_btm=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_lft=[RATE*5,RATE*14,RATE*6,RATE*13]
    coords_rgt=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_fwd=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_bck=[RATE*6,RATE*13,RATE*7,RATE*12]
    index=42
    o_dynamic = True
    def on_dynamic_update(self):
        if sum(self.world.getNeighboringCurrents(self.pos)):
            y= self.world.getBlockAt((self.pos[0]-1,self.pos[1],self.pos[2]))
            d = 1
            shoved = []
            while y:
                self.world.killBlock(y,recompile=False)
                y.pos = (y.pos[0]-1,y.pos[1],y.pos[2])
                #self.world.setBlockAt(y,recompile=False)
                shoved.append(y)
                d+=1
                y= self.world.getBlockAt((self.pos[0]-d,self.pos[1],self.pos[2]))
            for block in shoved: self.world.setBlockAt(block,recompile=False)
            if shoved:self.world.recompile()
class ExperimentalPusherRight(BasicBlock):
    particle_colors = [(0.3,0.14,0.0)]
    coords_top=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_btm=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_lft=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_rgt=[RATE*5,RATE*14,RATE*6,RATE*13]
    coords_fwd=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_bck=[RATE*6,RATE*13,RATE*7,RATE*12]
    index=41
    o_dynamic = True
    def on_dynamic_update(self):
        if sum(self.world.getNeighboringCurrents(self.pos)):
            y= self.world.getBlockAt((self.pos[0]+1,self.pos[1],self.pos[2]))
            d = 1
            shoved = []
            while y:
                self.world.killBlock(y,recompile=False)
                y.pos = (y.pos[0]+1,y.pos[1],y.pos[2])
                #self.world.setBlockAt(y,recompile=False)
                shoved.append(y)
                d+=1
                y= self.world.getBlockAt((self.pos[0]+d,self.pos[1],self.pos[2]))
            for block in shoved: self.world.setBlockAt(block,recompile=False)
            if shoved:self.world.recompile()

class Spout(BasicBlock):
    particle_colors = [(0.0,0.0,0.65,1.0)]
    o_name = "Water Fountain"
    ag=True
    wtrans = True
    coords_top=[RATE*0,RATE*11,RATE*1,RATE*10]
    coords_btm=[RATE*0,RATE*11,RATE*1,RATE*10]
    coords_lft=[RATE*0,RATE*11,RATE*1,RATE*10]
    coords_rgt=[RATE*0,RATE*11,RATE*1,RATE*10]
    coords_fwd=[RATE*0,RATE*11,RATE*1,RATE*10]
    coords_bck=[RATE*0,RATE*11,RATE*1,RATE*10]
    o_solid=False
    index=40
    cutoff = False
    trans=False
    o_dynamic = True
    def on_dynamic_update(self):
        if not self.world.getBlockAt((self.pos[0],self.pos[1]-1,self.pos[2])):
            Water((self.pos[0],self.pos[1]-1,self.pos[2]),self.world,recompile=False)
    
class XOR(BasicBlock):
    coords_top=[RATE*9,RATE*16,RATE*10,RATE*15]
    coords_btm=[RATE*8,RATE*15,RATE*9,RATE*14]
    coords_lft=[RATE*7,RATE*15,RATE*8,RATE*14]
    coords_rgt=[RATE*7,RATE*15,RATE*8,RATE*14]
    coords_fwd=[RATE*8,RATE*15,RATE*9,RATE*14]
    coords_bck=[RATE*8,RATE*15,RATE*9,RATE*14]
    o_dynamic = True
    index = 39
    dcutoff = True
    particle_colors = [(1.0,0.0,0.0,1.0),(0.8,0.0,0.0,1.0)]
    def getE(self):
        on = 1 - int(self.last_info[0] == self.last_info[1])
        data = (0,0,on,on,on,on)
        return data
    def on_dynamic_update(self):
        pass
    def render(self):
        self.last_info = self.world.getNeighboringCurrents(self.pos)
        glTexCoord2f(self.coords_fwd[0],self.coords_fwd[3]); glVertex3f(self.pos[0]+ -0.5,self.pos[1]+-0.5,self.pos[2]+0.5) #Front
        glTexCoord2f(self.coords_fwd[2],self.coords_fwd[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_fwd[2],self.coords_fwd[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_fwd[0],self.coords_fwd[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_bck[2],self.coords_bck[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_bck[0],self.coords_bck[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5) #Back
        glTexCoord2f(self.coords_bck[0],self.coords_bck[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_bck[2],self.coords_bck[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_btm[2],self.coords_btm[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5) #Bottom
        glTexCoord2f(self.coords_btm[0],self.coords_btm[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_btm[0],self.coords_btm[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_btm[2],self.coords_btm[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_top[0],self.coords_top[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #Top
        glTexCoord2f(self.coords_top[2],self.coords_top[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_top[2],self.coords_top[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_top[0],self.coords_top[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_lft[0],self.coords_lft[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_lft[0],self.coords_lft[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #left
        glTexCoord2f(self.coords_lft[2],self.coords_lft[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_lft[2],self.coords_lft[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_rgt[2],self.coords_rgt[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_rgt[2],self.coords_rgt[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #right
        glTexCoord2f(self.coords_rgt[0],self.coords_rgt[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_rgt[0],self.coords_rgt[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
    def __init__(self,pos,world,create=True,recompile=True,state=0):
        self.last_info = (0,0,0,0,0,0)
        BasicBlock.__init__(self,pos,world,create,False)
        
class NOT(BasicBlock):
    coords_top=[RATE*8,RATE*16,RATE*9,RATE*15]
    coords_btm=[RATE*8,RATE*15,RATE*9,RATE*14]
    coords_lft=[RATE*8,RATE*15,RATE*9,RATE*14]
    coords_rgt=[RATE*8,RATE*15,RATE*9,RATE*14]
    coords_fwd=[RATE*8,RATE*15,RATE*9,RATE*14]
    coords_bck=[RATE*7,RATE*15,RATE*8,RATE*14]
    o_dynamic = True
    index = 38
    dcutoff = True
    particle_colors = [(1.0,0.0,0.0,1.0),(0.8,0.0,0.0,1.0)]
    def getE(self):
        on = 1 - int(self.last_info[5])
        #print on
        data = (on,on,on,on,0,on)
        return data
    def on_dynamic_update(self):
        pass
    def render(self):
        self.last_info = self.world.getNeighboringCurrents(self.pos)
        glTexCoord2f(self.coords_fwd[0],self.coords_fwd[3]); glVertex3f(self.pos[0]+ -0.5,self.pos[1]+-0.5,self.pos[2]+0.5) #Front
        glTexCoord2f(self.coords_fwd[2],self.coords_fwd[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_fwd[2],self.coords_fwd[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_fwd[0],self.coords_fwd[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_bck[2],self.coords_bck[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_bck[0],self.coords_bck[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5) #Back
        glTexCoord2f(self.coords_bck[0],self.coords_bck[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_bck[2],self.coords_bck[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_btm[2],self.coords_btm[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5) #Bottom
        glTexCoord2f(self.coords_btm[0],self.coords_btm[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_btm[0],self.coords_btm[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_btm[2],self.coords_btm[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_top[0],self.coords_top[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #Top
        glTexCoord2f(self.coords_top[2],self.coords_top[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_top[2],self.coords_top[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_top[0],self.coords_top[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_lft[0],self.coords_lft[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_lft[0],self.coords_lft[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #left
        glTexCoord2f(self.coords_lft[2],self.coords_lft[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_lft[2],self.coords_lft[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_rgt[2],self.coords_rgt[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_rgt[2],self.coords_rgt[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #right
        glTexCoord2f(self.coords_rgt[0],self.coords_rgt[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_rgt[0],self.coords_rgt[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
    def __init__(self,pos,world,create=True,recompile=True,state=0):
        self.last_info = (0,0,0,0,0,0)
        BasicBlock.__init__(self,pos,world,create,False)

class AND(BasicBlock):
    coords_top=[RATE*7,RATE*16,RATE*8,RATE*15]
    coords_btm=[RATE*8,RATE*15,RATE*9,RATE*14]
    coords_lft=[RATE*7,RATE*15,RATE*8,RATE*14]
    coords_rgt=[RATE*7,RATE*15,RATE*8,RATE*14]
    coords_fwd=[RATE*8,RATE*15,RATE*9,RATE*14]
    coords_bck=[RATE*8,RATE*15,RATE*9,RATE*14]
    o_dynamic = True
    index = 37
    dcutoff = True
    particle_colors = [(1.0,0.0,0.0,1.0),(0.8,0.0,0.0,1.0)]
    def getE(self):
        on = int((self.last_info[0] + self.last_info[1]) > 1)
        data = (0,0,on,on,on,on)
        return data
    def on_dynamic_update(self):
        pass
    def render(self):
        self.last_info = self.world.getNeighboringCurrents(self.pos)
        glTexCoord2f(self.coords_fwd[0],self.coords_fwd[3]); glVertex3f(self.pos[0]+ -0.5,self.pos[1]+-0.5,self.pos[2]+0.5) #Front
        glTexCoord2f(self.coords_fwd[2],self.coords_fwd[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_fwd[2],self.coords_fwd[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_fwd[0],self.coords_fwd[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_bck[2],self.coords_bck[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_bck[0],self.coords_bck[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5) #Back
        glTexCoord2f(self.coords_bck[0],self.coords_bck[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_bck[2],self.coords_bck[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_btm[2],self.coords_btm[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5) #Bottom
        glTexCoord2f(self.coords_btm[0],self.coords_btm[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_btm[0],self.coords_btm[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_btm[2],self.coords_btm[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_top[0],self.coords_top[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #Top
        glTexCoord2f(self.coords_top[2],self.coords_top[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_top[2],self.coords_top[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_top[0],self.coords_top[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_lft[0],self.coords_lft[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_lft[0],self.coords_lft[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #left
        glTexCoord2f(self.coords_lft[2],self.coords_lft[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_lft[2],self.coords_lft[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_rgt[2],self.coords_rgt[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_rgt[2],self.coords_rgt[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #right
        glTexCoord2f(self.coords_rgt[0],self.coords_rgt[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_rgt[0],self.coords_rgt[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
    def __init__(self,pos,world,create=True,recompile=True,state=0):
        self.last_info = (0,0,0,0,0,0)
        BasicBlock.__init__(self,pos,world,create,False)

class Wire(BasicBlock):
    coords_top=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_btm=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_lft=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_rgt=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_fwd=[RATE*6,RATE*13,RATE*7,RATE*12]
    coords_bck=[RATE*6,RATE*13,RATE*7,RATE*12]
    o_dynamic=True
    index = 36
    dcutoff = True
    cutoff = False
    trans=True
    particle_colors = [(1.0,0.0,0.0,1.0),(0.8,0.0,0.0,1.0)]
    def getE(self):
        on = min(self.last_info[0]+self.last_info[1]+self.last_info[2]+self.last_info[3]+self.last_info[4]+self.last_info[5],1)
        data = (
            int((not self.last_info[1]) and on),
            int((not self.last_info[0]) and on),
            int((not self.last_info[3]) and on),
            int((not self.last_info[2]) and on),
            int((not self.last_info[5]) and on),
            int((not self.last_info[4]) and on))
        return data
    def on_dynamic_update(self):
        pass
    def render(self):
        #self.cache=None
        self.last_info = self.world.getNeighboringCurrents(self.pos)
        on = min(self.last_info[0]+self.last_info[1]+self.last_info[2]+self.last_info[3]+self.last_info[4]+self.last_info[5],1)
        glTexCoord2f((RATE*on)+self.coords_fwd[0],self.coords_fwd[3]); glVertex3f(self.pos[0]+ -0.5,self.pos[1]+-0.5,self.pos[2]+0.5) #Front
        glTexCoord2f((RATE*on)+self.coords_fwd[2],self.coords_fwd[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_fwd[2],self.coords_fwd[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_fwd[0],self.coords_fwd[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_bck[2],self.coords_bck[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f((RATE*on)+self.coords_bck[0],self.coords_bck[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5) #Back
        glTexCoord2f((RATE*on)+self.coords_bck[0],self.coords_bck[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glTexCoord2f((RATE*on)+self.coords_bck[2],self.coords_bck[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glTexCoord2f((RATE*on)+self.coords_btm[2],self.coords_btm[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5) #Bottom
        glTexCoord2f((RATE*on)+self.coords_btm[0],self.coords_btm[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f((RATE*on)+self.coords_btm[0],self.coords_btm[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_btm[2],self.coords_btm[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_top[0],self.coords_top[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #Top
        glTexCoord2f((RATE*on)+self.coords_top[2],self.coords_top[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glTexCoord2f((RATE*on)+self.coords_top[2],self.coords_top[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_top[0],self.coords_top[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_lft[0],self.coords_lft[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f((RATE*on)+self.coords_lft[0],self.coords_lft[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #left
        glTexCoord2f((RATE*on)+self.coords_lft[2],self.coords_lft[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_lft[2],self.coords_lft[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_rgt[2],self.coords_rgt[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f((RATE*on)+self.coords_rgt[2],self.coords_rgt[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #right
        glTexCoord2f((RATE*on)+self.coords_rgt[0],self.coords_rgt[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_rgt[0],self.coords_rgt[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
    def __init__(self,pos,world,create=True,recompile=True,state=0):
        self.last_info = (0,0,0,0,0,0)
        self.cache = None
        BasicBlock.__init__(self,pos,world,create,False)

class Switch(BasicBlock):
    coords_top=[RATE*6,RATE*14,RATE*7,RATE*13]
    coords_btm=[RATE*6,RATE*14,RATE*7,RATE*13]
    coords_lft=[RATE*6,RATE*14,RATE*7,RATE*13]
    coords_rgt=[RATE*6,RATE*14,RATE*7,RATE*13]
    coords_fwd=[RATE*6,RATE*14,RATE*7,RATE*13]
    coords_bck=[RATE*6,RATE*14,RATE*7,RATE*13]
    index = 35
    cutoff = False
    o_dynamic = True
    o_usable = True
    def getState(self):
        #print "Hah! Gotcha!"
        #print self.on
        return self.on
    def getE(self):
        return [self.on] * 6
    def __init__(self,pos,world,create=True,recompile=True,state=0):
        self.on = state
        BasicBlock.__init__(self,pos,world,create,False)
    def on_dynamic_update(self):
        pass
    def on_use(self):
        self.on = 1 - self.on

    def render(self):
        on = self.on
        glTexCoord2f((RATE*on)+self.coords_fwd[0],self.coords_fwd[3]); glVertex3f(self.pos[0]+ -0.5,self.pos[1]+-0.5,self.pos[2]+0.5) #Front
        glTexCoord2f((RATE*on)+self.coords_fwd[2],self.coords_fwd[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_fwd[2],self.coords_fwd[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_fwd[0],self.coords_fwd[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_bck[2],self.coords_bck[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f((RATE*on)+self.coords_bck[0],self.coords_bck[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5) #Back
        glTexCoord2f((RATE*on)+self.coords_bck[0],self.coords_bck[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glTexCoord2f((RATE*on)+self.coords_bck[2],self.coords_bck[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glTexCoord2f((RATE*on)+self.coords_btm[2],self.coords_btm[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5) #Bottom
        glTexCoord2f((RATE*on)+self.coords_btm[0],self.coords_btm[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f((RATE*on)+self.coords_btm[0],self.coords_btm[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_btm[2],self.coords_btm[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_top[0],self.coords_top[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #Top
        glTexCoord2f((RATE*on)+self.coords_top[2],self.coords_top[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glTexCoord2f((RATE*on)+self.coords_top[2],self.coords_top[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_top[0],self.coords_top[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_lft[0],self.coords_lft[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f((RATE*on)+self.coords_lft[0],self.coords_lft[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #left
        glTexCoord2f((RATE*on)+self.coords_lft[2],self.coords_lft[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_lft[2],self.coords_lft[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_rgt[2],self.coords_rgt[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f((RATE*on)+self.coords_rgt[2],self.coords_rgt[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #right
        glTexCoord2f((RATE*on)+self.coords_rgt[0],self.coords_rgt[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_rgt[0],self.coords_rgt[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)

class WaterBucket(BasicBlock):
    particle_colors = [(0.3,0.14,0.0),(0.0,0.0,0.65,1.0)]
    coords_top=[RATE*6,RATE*16,RATE*7,RATE*15]
    coords_btm=[RATE*5,RATE*14,RATE*6,RATE*13]
    coords_lft=[RATE*5,RATE*14,RATE*6,RATE*13]
    coords_rgt=[RATE*5,RATE*14,RATE*6,RATE*13]
    coords_fwd=[RATE*5,RATE*14,RATE*6,RATE*13]
    coords_bck=[RATE*5,RATE*14,RATE*6,RATE*13]
    index = 31

class SandBlock(BasicBlock):
    particle_colors = [(1.0,1.0,0.6,1.0)]
    coords_top=[RATE*6,RATE*15,RATE*7,RATE*14]
    coords_btm=[RATE*6,RATE*15,RATE*7,RATE*14]
    coords_lft=[RATE*6,RATE*15,RATE*7,RATE*14]
    coords_rgt=[RATE*6,RATE*15,RATE*7,RATE*14]
    coords_fwd=[RATE*6,RATE*15,RATE*7,RATE*14]
    coords_bck=[RATE*6,RATE*15,RATE*7,RATE*14]
    index = 32
    o_dynamic=True
    cutoff = False
    def on_dynamic_update(self):
            #print "Update:",
            if not self.world.getBlockAt((self.pos[0],self.pos[1]-1,self.pos[2])):
                #print "Yes"
                self.world.killBlock(self,recompile=False)
                self.pos = (self.pos[0],self.pos[1]-1,self.pos[2])
                self.world.setBlockAt(self,recompile=False)
            else:
                pass
                #print "No"

##class WaterFountain(BasicBlock):
##    coords_top=[RATE*6,RATE*16,RATE*7,RATE*15]
##    coords_btm=[RATE*6,RATE*16,RATE*7,RATE*15]
##    coords_lft=[RATE*6,RATE*16,RATE*7,RATE*15]
##    coords_rgt=[RATE*6,RATE*16,RATE*7,RATE*15]
##    coords_fwd=[RATE*6,RATE*16,RATE*7,RATE*15]
##    coords_bck=[RATE*6,RATE*16,RATE*7,RATE*15]
##    index = 33

class LED(BasicBlock):
    o_dynamic = True
    coords_top=[RATE*4,RATE*13,RATE*5,RATE*12]
    coords_btm=[RATE*4,RATE*13,RATE*5,RATE*12]
    coords_lft=[RATE*4,RATE*13,RATE*5,RATE*12]
    coords_rgt=[RATE*4,RATE*13,RATE*5,RATE*12]
    coords_fwd=[RATE*4,RATE*13,RATE*5,RATE*12]
    coords_bck=[RATE*4,RATE*13,RATE*5,RATE*12]
    index = 34
    particle_colors = [(0.6,0.6,0.0,1.0)]
    def getE(self):
        return (0,0,0,0,0,0)
    def on_dynamic_update(self):
        pass
    def render(self):
        data = self.world.getNeighboringCurrents(self.pos)
        on = min(data[0]+data[1]+data[2]+data[3]+data[4]+data[5],1)
        glTexCoord2f((RATE*on)+self.coords_fwd[0],self.coords_fwd[3]); glVertex3f(self.pos[0]+ -0.5,self.pos[1]+-0.5,self.pos[2]+0.5) #Front
        glTexCoord2f((RATE*on)+self.coords_fwd[2],self.coords_fwd[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_fwd[2],self.coords_fwd[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_fwd[0],self.coords_fwd[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_bck[2],self.coords_bck[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f((RATE*on)+self.coords_bck[0],self.coords_bck[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5) #Back
        glTexCoord2f((RATE*on)+self.coords_bck[0],self.coords_bck[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glTexCoord2f((RATE*on)+self.coords_bck[2],self.coords_bck[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glTexCoord2f((RATE*on)+self.coords_btm[2],self.coords_btm[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5) #Bottom
        glTexCoord2f((RATE*on)+self.coords_btm[0],self.coords_btm[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f((RATE*on)+self.coords_btm[0],self.coords_btm[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_btm[2],self.coords_btm[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_top[0],self.coords_top[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #Top
        glTexCoord2f((RATE*on)+self.coords_top[2],self.coords_top[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glTexCoord2f((RATE*on)+self.coords_top[2],self.coords_top[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_top[0],self.coords_top[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_lft[0],self.coords_lft[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f((RATE*on)+self.coords_lft[0],self.coords_lft[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #left
        glTexCoord2f((RATE*on)+self.coords_lft[2],self.coords_lft[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_lft[2],self.coords_lft[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_rgt[2],self.coords_rgt[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f((RATE*on)+self.coords_rgt[2],self.coords_rgt[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #right
        glTexCoord2f((RATE*on)+self.coords_rgt[0],self.coords_rgt[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_rgt[0],self.coords_rgt[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
class Generator(BasicBlock):
    particle_colors = [(1.0,1.0,0.0,1.0),(1.0,0.8,0.0,1.0),(1.0,0.6,0.0,1.0),(1.0,0.4,0.0,1.0),(1.0,0.2,0.0,1.0),(1.0,0.1,0.0,1.0)]
    o_dynamic = True
    coords_top=[RATE*2,RATE*12,RATE*3,RATE*11]
    coords_btm=[RATE*2,RATE*12,RATE*3,RATE*11]
    coords_lft=[RATE*2,RATE*12,RATE*3,RATE*11]
    coords_rgt=[RATE*2,RATE*12,RATE*3,RATE*11]
    coords_fwd=[RATE*2,RATE*12,RATE*3,RATE*11]
    coords_bck=[RATE*2,RATE*12,RATE*3,RATE*11]
    index = 33
    cutoff = False
    def getE(self):
        return (1,1,1,1,1,1)
    def __init__(self,pos,world,create=True,recompile=True,state=0):
        print "!!!"
        self.count = 0
        print "!!!!"
        BasicBlock.__init__(self,pos,world,create,False)
    def on_dynamic_update(self):
        pass

    def render(self):
        self.count += 1
        self.count = self.count % 6
        glTexCoord2f(self.coords_fwd[0]+(RATE*self.count),self.coords_fwd[3]); glVertex3f(self.pos[0]+ -0.5,self.pos[1]+-0.5,self.pos[2]+0.5) #Front
        glTexCoord2f(self.coords_fwd[2]+(RATE*self.count),self.coords_fwd[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_fwd[2]+(RATE*self.count),self.coords_fwd[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_fwd[0]+(RATE*self.count),self.coords_fwd[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_bck[2]+(RATE*self.count),self.coords_bck[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_bck[0]+(RATE*self.count),self.coords_bck[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5) #Back
        glTexCoord2f(self.coords_bck[0]+(RATE*self.count),self.coords_bck[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_bck[2]+(RATE*self.count),self.coords_bck[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_btm[2]+(RATE*self.count),self.coords_btm[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5) #Bottom
        glTexCoord2f(self.coords_btm[0]+(RATE*self.count),self.coords_btm[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_btm[0]+(RATE*self.count),self.coords_btm[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_btm[2]+(RATE*self.count),self.coords_btm[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_top[0]+(RATE*self.count),self.coords_top[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #Top
        glTexCoord2f(self.coords_top[2]+(RATE*self.count),self.coords_top[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_top[2]+(RATE*self.count),self.coords_top[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_top[0]+(RATE*self.count),self.coords_top[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_lft[0]+(RATE*self.count),self.coords_lft[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_lft[0]+(RATE*self.count),self.coords_lft[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #left
        glTexCoord2f(self.coords_lft[2]+(RATE*self.count),self.coords_lft[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_lft[2]+(RATE*self.count),self.coords_lft[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_rgt[2]+(RATE*self.count),self.coords_rgt[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_rgt[2]+(RATE*self.count),self.coords_rgt[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #right
        glTexCoord2f(self.coords_rgt[0]+(RATE*self.count),self.coords_rgt[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_rgt[0]+(RATE*self.count),self.coords_rgt[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)        


        
        

class HatchShut(BasicBlock):
    particle_colors = [(0.3,0.14,0.0)]
    coords_top=[RATE*5,RATE*14,RATE*6,RATE*13]
    coords_btm=[RATE*5,RATE*14,RATE*6,RATE*13]
    coords_lft=[RATE*5,RATE*14,RATE*6,RATE*13]
    coords_rgt=[RATE*5,RATE*14,RATE*6,RATE*13]
    coords_fwd=[RATE*5,RATE*14,RATE*6,RATE*13]
    coords_bck=[RATE*5,RATE*14,RATE*6,RATE*13]
    o_name = "HatchShut"
    o_solid = True
    index = 29
    o_usable = True
    counter = None
    cutoff = False
    def on_use(self):
        self.counter(self.pos,self.world)

    def render(self):
        if self.world.getBlockAt((self.pos[0],self.pos[1]-1,self.pos[2])):
            self.solid=False
            #glBegin(GL_QUADS)
            glTexCoord2f(self.coords_top[0],self.coords_top[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]-0.499,self.pos[2]+-0.5) #Top
            glTexCoord2f(self.coords_top[2],self.coords_top[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]-0.499,self.pos[2]+-0.5)
            glTexCoord2f(self.coords_top[2],self.coords_top[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]-0.499,self.pos[2]+0.5)
            glTexCoord2f(self.coords_top[0],self.coords_top[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]-0.499,self.pos[2]+0.5)
            #glEnd()
        else:
            self.solid=True
            #glBegin(GL_QUADS)
            glTexCoord2f(self.coords_top[0],self.coords_top[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.499,self.pos[2]+-0.5) #Top
            glTexCoord2f(self.coords_top[2],self.coords_top[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.499,self.pos[2]+-0.5)
            glTexCoord2f(self.coords_top[2],self.coords_top[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.499,self.pos[2]+0.5)
            glTexCoord2f(self.coords_top[0],self.coords_top[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.499,self.pos[2]+0.5)
            #glEnd()
            
class HatchOpen(BasicBlock):
    particle_colors = [(0.3,0.14,0.0)]
    coords_top=[RATE*5,RATE*14,RATE*6,RATE*13]
    coords_btm=[RATE*5,RATE*14,RATE*6,RATE*13]
    coords_lft=[RATE*5,RATE*14,RATE*6,RATE*13]
    coords_rgt=[RATE*5,RATE*14,RATE*6,RATE*13]
    coords_fwd=[RATE*5,RATE*14,RATE*6,RATE*13]
    coords_bck=[RATE*5,RATE*14,RATE*6,RATE*13]
    o_name = "HatchShut"
    o_solid = False
    index = 30
    trans=True
    o_usable = True
    counter = HatchShut
    cutoff = False
    def on_use(self):
        self.counter(self.pos,self.world)

    def render(self):
        if self.world.getBlockAt((self.pos[0],self.pos[1]-1,self.pos[2])): 
            #glBegin(GL_QUADS)
            glTexCoord2f(self.coords_bck[2],self.coords_bck[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]-0.5,self.pos[2]+-0.499)
            glTexCoord2f(self.coords_bck[0],self.coords_bck[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]-0.5,self.pos[2]+-0.499) #Back
            glTexCoord2f(self.coords_bck[0],self.coords_bck[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.499)
            glTexCoord2f(self.coords_bck[2],self.coords_bck[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.499)
            #glEnd()
        else:
            #glBegin(GL_QUADS)
            glTexCoord2f(self.coords_bck[2],self.coords_bck[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.499)
            glTexCoord2f(self.coords_bck[0],self.coords_bck[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.499) #Back
            glTexCoord2f(self.coords_bck[0],self.coords_bck[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+1.5,self.pos[2]+-0.499)
            glTexCoord2f(self.coords_bck[2],self.coords_bck[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+1.5,self.pos[2]+-0.499)
            #glEnd()

HatchShut.counter=HatchOpen

class Water(BasicBlock):
    o_name = "Water"
    ag=True
    wtrans = True
    coords_top=[RATE*0,RATE*11,RATE*1,RATE*10]
    coords_btm=[RATE*0,RATE*11,RATE*1,RATE*10]
    coords_lft=[RATE*0,RATE*11,RATE*1,RATE*10]
    coords_rgt=[RATE*0,RATE*11,RATE*1,RATE*10]
    coords_fwd=[RATE*0,RATE*11,RATE*1,RATE*10]
    coords_bck=[RATE*0,RATE*11,RATE*1,RATE*10]
    o_solid=False
    index=27
    cutoff = False
    trans=False
    particle_colors = [(0.0,0.0,0.65,1.0)]
    #o_dynamic = True
    def render(self):
        #glBegin(GL_QUADS)
        #glColor(0.5,0.5,0.5,1.0);
        #self.on -= (1/64.0)
        #if self.on == 0: self.on =1
        on = 0
        try:
            if self.world.getBlockAt((self.pos[0],self.pos[1],self.pos[2]+1)).trans: raise BlockError
        except:
            #print "!"
            #p#rint "Front!"
            glTexCoord2f(self.coords_fwd[0],self.coords_fwd[3]-(RATE*on)); glVertex3f(self.pos[0]+ -0.5,self.pos[1]+-0.5,self.pos[2]+0.5) #Front
            glTexCoord2f(self.coords_fwd[2],self.coords_fwd[3]-(RATE*on)); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
            glTexCoord2f(self.coords_fwd[2],self.coords_fwd[1]-(RATE*on)); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
            glTexCoord2f(self.coords_fwd[0],self.coords_fwd[1]-(RATE*on)); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)

        try:
            if self.world.getBlockAt((self.pos[0],self.pos[1],self.pos[2]-1)).trans: raise BlockError
        except:
            glTexCoord2f(self.coords_bck[2],self.coords_bck[3]-(RATE*on)); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
            glTexCoord2f(self.coords_bck[0],self.coords_bck[3]-(RATE*on)); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5) #Back
            glTexCoord2f(self.coords_bck[0],self.coords_bck[1]-(RATE*on)); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
            glTexCoord2f(self.coords_bck[2],self.coords_bck[1]-(RATE*on)); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5)

        try:
            if self.world.getBlockAt((self.pos[0],self.pos[1]-1,self.pos[2])).trans: raise BlockError
        except:
            glTexCoord2f(self.coords_btm[2],self.coords_btm[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5) #Bottom
            glTexCoord2f(self.coords_btm[0],self.coords_btm[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
            glTexCoord2f(self.coords_btm[0],self.coords_btm[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
            glTexCoord2f(self.coords_btm[2],self.coords_btm[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+0.5)

        try:
            if self.world.getBlockAt((self.pos[0],self.pos[1]+1,self.pos[2])).trans: raise BlockError
        except:
            glTexCoord2f(self.coords_top[0],self.coords_top[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #Top
            glTexCoord2f(self.coords_top[2],self.coords_top[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
            glTexCoord2f(self.coords_top[2],self.coords_top[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
            glTexCoord2f(self.coords_top[0],self.coords_top[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)

        try:
            if self.world.getBlockAt((self.pos[0]-1,self.pos[1],self.pos[2])).trans: raise BlockError
        except:
            glTexCoord2f(self.coords_lft[0],self.coords_lft[3]-(RATE*on)); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
            glTexCoord2f(self.coords_lft[0],self.coords_lft[1]-(RATE*on)); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #left
            glTexCoord2f(self.coords_lft[2],self.coords_lft[1]-(RATE*on)); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
            glTexCoord2f(self.coords_lft[2],self.coords_lft[3]-(RATE*on)); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+0.5)

        try:
            if self.world.getBlockAt((self.pos[0]+1,self.pos[1],self.pos[2])).trans: raise BlockError
        except:
            glTexCoord2f(self.coords_rgt[2],self.coords_rgt[3]-(RATE*on)); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
            glTexCoord2f(self.coords_rgt[2],self.coords_rgt[1]-(RATE*on)); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #right
            glTexCoord2f(self.coords_rgt[0],self.coords_rgt[1]-(RATE*on)); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
            glTexCoord2f(self.coords_rgt[0],self.coords_rgt[3]-(RATE*on)); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)  
class BrickBlock(BasicBlock):
    index = 28
    particle_colors = [(0.9,0.1,0.1,1.0)]
    o_name = "Brick"
    coords_top=[RATE*3,RATE*15,RATE*4,RATE*14]
    coords_btm=[RATE*3,RATE*15,RATE*4,RATE*14]
    coords_lft=[RATE*3,RATE*15,RATE*4,RATE*14]
    coords_rgt=[RATE*3,RATE*15,RATE*4,RATE*14]
    coords_fwd=[RATE*3,RATE*15,RATE*4,RATE*14]
    coords_bck=[RATE*3,RATE*15,RATE*4,RATE*14]

class GoldBlock(BasicBlock):
    index = 25
    particle_colors = [(0.5,0.5,0.1,1.0)]
    o_name = "GoldBlock"
    coords_top=[RATE*5,RATE*15,RATE*6,RATE*14]
    coords_btm=[RATE*5,RATE*15,RATE*6,RATE*14]
    coords_lft=[RATE*5,RATE*15,RATE*6,RATE*14]
    coords_rgt=[RATE*5,RATE*15,RATE*6,RATE*14]
    coords_fwd=[RATE*5,RATE*15,RATE*6,RATE*14]
    coords_bck=[RATE*5,RATE*15,RATE*6,RATE*14]

class SilverBlock(BasicBlock):
    index = 26
    o_name="SilverBlock"
    coords_top=[RATE*4,RATE*15,RATE*5,RATE*14]
    coords_btm=[RATE*4,RATE*15,RATE*5,RATE*14]
    coords_lft=[RATE*4,RATE*15,RATE*5,RATE*14]
    coords_rgt=[RATE*4,RATE*15,RATE*5,RATE*14]
    coords_fwd=[RATE*4,RATE*15,RATE*5,RATE*14]
    coords_bck=[RATE*4,RATE*15,RATE*5,RATE*14]

class Glass(BasicBlock):
    index = 24
    trans=True
    coords_top=[RATE*0,RATE*12,RATE*1,RATE*11]
    coords_btm=[RATE*0,RATE*12,RATE*1,RATE*11]
    coords_lft=[RATE*0,RATE*12,RATE*1,RATE*11]
    coords_rgt=[RATE*0,RATE*12,RATE*1,RATE*11]
    coords_fwd=[RATE*0,RATE*12,RATE*1,RATE*11]
    coords_bck=[RATE*0,RATE*12,RATE*1,RATE*11]
    cutoff = False
    dcutoff = False

class Cake(BasicBlock):
    index = 22
    particle_colors = [(0.5,0.25,0.0,1.0),(1.0,1.0,1.0,1.0)]
    coords_top=[RATE*1,RATE*13,RATE*2,RATE*12]
    coords_btm=[RATE*1,RATE*11,RATE*2,RATE*10]
    coords_lft=[RATE*1,RATE*12,RATE*2,RATE*11]
    coords_rgt=[RATE*1,RATE*12,RATE*2,RATE*11]
    coords_fwd=[RATE*1,RATE*12,RATE*2,RATE*11]
    coords_bck=[RATE*1,RATE*12,RATE*2,RATE*11]

class SwissCheese(BasicBlock):
    index = 23
    particle_colors = [(1.0,1.0,0.0,1.0)]
    coords_top=[RATE*2,RATE*13,RATE*3,RATE*12]
    coords_btm=[RATE*2,RATE*13,RATE*3,RATE*12]
    coords_lft=[RATE*2,RATE*13,RATE*3,RATE*12]
    coords_rgt=[RATE*2,RATE*13,RATE*3,RATE*12]
    coords_fwd=[RATE*2,RATE*13,RATE*3,RATE*12]
    coords_bck=[RATE*2,RATE*13,RATE*3,RATE*12]
    
class Snow(BasicBlock):
    o_solid = False
    index = 21
    particle_colors=[(1.0,1.0,1.0,1.0)]
    #trans=True
    coords_top=[RATE*0,RATE*13,RATE*1,RATE*12]
    coords_btm=[RATE*0,RATE*13,RATE*1,RATE*12]
    coords_lft=[RATE*0,RATE*13,RATE*1,RATE*12]
    coords_rgt=[RATE*0,RATE*13,RATE*1,RATE*12]
    coords_fwd=[RATE*0,RATE*13,RATE*1,RATE*12]
    coords_bck=[RATE*0,RATE*13,RATE*1,RATE*12]
    cutoff = False
    def render(self):
        #glBegin(GL_QUADS)
        #glColor(0.5,0.5,0.5,1.0);
        glNormal3f(0,0,1)
        glTexCoord2f(self.coords_fwd[0],self.coords_fwd[3]); glVertex3f(self.pos[0]+ -0.5,self.pos[1]+-0.5,self.pos[2]+0.5) #Front
        glTexCoord2f(self.coords_fwd[2],self.coords_fwd[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_fwd[2],self.coords_fwd[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0,self.pos[2]+0.5)
        glTexCoord2f(self.coords_fwd[0],self.coords_fwd[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0,self.pos[2]+0.5)
        glNormal3f(0,0,-1)
        #glColor(0,1,0,1.0);
        glTexCoord2f(self.coords_bck[2],self.coords_bck[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_bck[0],self.coords_bck[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5) #Back
        glTexCoord2f(self.coords_bck[0],self.coords_bck[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_bck[2],self.coords_bck[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0,self.pos[2]+-0.5)
        glNormal3f(0,-1,0)
        #glColor(0,0,1,1.0);
        glTexCoord2f(self.coords_btm[2],self.coords_btm[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5) #Bottom
        glTexCoord2f(self.coords_btm[0],self.coords_btm[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_btm[0],self.coords_btm[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords_btm[2],self.coords_btm[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glNormal3f(0,1,0)
        #glColor(1,1,0,1.0);
        glTexCoord2f(self.coords_top[0],self.coords_top[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0,self.pos[2]+-0.5) #Top
        glTexCoord2f(self.coords_top[2],self.coords_top[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_top[2],self.coords_top[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0,self.pos[2]+0.5)
        glTexCoord2f(self.coords_top[0],self.coords_top[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0,self.pos[2]+0.5)
        glNormal3f(-1,0,0)
        #glColor(0,1,1,1.0);
        glTexCoord2f(self.coords_lft[0],self.coords_lft[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_lft[0],self.coords_lft[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0,self.pos[2]+-0.5) #left
        glTexCoord2f(self.coords_lft[2],self.coords_lft[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0,self.pos[2]+0.5)
        glTexCoord2f(self.coords_lft[2],self.coords_lft[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glNormal3f(1,0,0)
        #glColor(1,0,1,1.0);
        glTexCoord2f(self.coords_rgt[2],self.coords_rgt[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords_rgt[2],self.coords_rgt[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0,self.pos[2]+-0.5) #right
        glTexCoord2f(self.coords_rgt[0],self.coords_rgt[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0,self.pos[2]+0.5)
        glTexCoord2f(self.coords_rgt[0],self.coords_rgt[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        #glEnd() 

class Dynamite(BasicBlock):
    o_name = "Dynamite"
    o_usable = True
    o_dynamic = True
    index = 20
    #order = 0
    coords_top=[RATE*10,RATE*16,RATE*11,RATE*15]
    coords_btm=[RATE*10,RATE*16,RATE*11,RATE*15]
    coords_lft=[RATE*10,RATE*16,RATE*11,RATE*15]
    coords_rgt=[RATE*10,RATE*16,RATE*11,RATE*15]
    coords_fwd=[RATE*10,RATE*16,RATE*11,RATE*15]
    coords_bck=[RATE*10,RATE*16,RATE*11,RATE*15]
    particle_colors = [(1.0,0.0,0.0,1.0),(0.9,0.0,0.0,1.0),(0.8,0.0,0.0,1.0)]
    def __init__(self,pos,world,create=True,recompile=True,state=0):
        self.countdown = -1
        BasicBlock.__init__(self,pos,world,create,False)
    def on_dynamic_update(self):
        currents = sum(self.world.getNeighboringCurrents(self.pos))
        if currents:
            self.on_use()
        if self.countdown == 0:
            self.fire()
    def on_use(self,dc=None):
        if not dc:
            self.countdown = randint(30,120)
        else:
            self.countdown = dc

    def fire(self):
        #kaboom.play()
        for _ in range(randint(15,25)): self.world.particles.append(ExplosionParticle(self.world,self.pos,(self.coords_lft[0]+(random()*RATE),self.coords_lft[3]+(random()*RATE))))

        #if ch:ch.set_volume(0.5,1.0)
        for y in range(-2,3):
            for x in range(-2,3):
                for z in range(-2,3):
                    if [abs(x),abs(y),abs(z)].count(2) > 1: continue
                    b = self.world.getBlockAt((self.pos[0]+x,self.pos[1]+y,self.pos[2]+z))
                    d = []
                    if b:
                        if b.name != "Dynamite" or b == self:
                            self.world.killBlock(self.world.getBlockAt((self.pos[0]+x,self.pos[1]+y,self.pos[2]+z)))
                        else:
                            d.append(b)
                    for u in d:
                        if u.countdown == -1:
                                u.on_use(dc=randint(3,10))
        self.world.recompile("Dynamite")
    def render(self):
        if self.countdown > 0:
            on = 1 - (self.countdown / 7) % 2
            self.countdown -= 1
        else:
            on = 0
        glTexCoord2f((RATE*on)+self.coords_fwd[0],self.coords_fwd[3]); glVertex3f(self.pos[0]+ -0.5,self.pos[1]+-0.5,self.pos[2]+0.5) #Front
        glTexCoord2f((RATE*on)+self.coords_fwd[2],self.coords_fwd[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_fwd[2],self.coords_fwd[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_fwd[0],self.coords_fwd[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_bck[2],self.coords_bck[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f((RATE*on)+self.coords_bck[0],self.coords_bck[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5) #Back
        glTexCoord2f((RATE*on)+self.coords_bck[0],self.coords_bck[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glTexCoord2f((RATE*on)+self.coords_bck[2],self.coords_bck[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glTexCoord2f((RATE*on)+self.coords_btm[2],self.coords_btm[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5) #Bottom
        glTexCoord2f((RATE*on)+self.coords_btm[0],self.coords_btm[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f((RATE*on)+self.coords_btm[0],self.coords_btm[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_btm[2],self.coords_btm[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_top[0],self.coords_top[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #Top
        glTexCoord2f((RATE*on)+self.coords_top[2],self.coords_top[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glTexCoord2f((RATE*on)+self.coords_top[2],self.coords_top[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_top[0],self.coords_top[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_lft[0],self.coords_lft[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f((RATE*on)+self.coords_lft[0],self.coords_lft[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #left
        glTexCoord2f((RATE*on)+self.coords_lft[2],self.coords_lft[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_lft[2],self.coords_lft[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_rgt[2],self.coords_rgt[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f((RATE*on)+self.coords_rgt[2],self.coords_rgt[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #right
        glTexCoord2f((RATE*on)+self.coords_rgt[0],self.coords_rgt[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f((RATE*on)+self.coords_rgt[0],self.coords_rgt[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
    
    
class DoorShutTop(BasicBlock):
    particle_colors = [(0.3,0.14,0.0)]
    o_name="Shut Door"
    o_solid=False
    o_usable=True
    #trans=True
    index = -1
    cutoff = False
    trans=True
    def __init__(self,pos,world,below,state=0):
        self.linked=[]
        self.below=below
        
        BasicBlock.__init__(self,pos,world,recompile=False)
        #self.render()
    def render(self):
        pass
    def on_kill(self):
        self.world.killBlock(self.below,polite=False,shrapnel=False)
    def on_use(self):
        self.below.on_use()
##    def on_use(self):
##        self.dob((self.pos[0],self.pos[1]-1,self.pos[2]),self.world)
        
        

class DoorShutBottom(BasicBlock):
    particle_colors = [(0.3,0.14,0.0)]
    o_name="Shut Door"
    o_solid=True
    o_usable=True
    cutoff = False
    #trans=True
    coords_top=[RATE*3,RATE*14,RATE*4,RATE*12]
    coords_btm=[RATE*3,RATE*14,RATE*4,RATE*12]
    coords_lft=[RATE*3,RATE*14,RATE*4,RATE*12]
    coords_rgt=[RATE*3,RATE*14,RATE*4,RATE*12]
    coords_fwd=[RATE*3,RATE*14,RATE*4,RATE*12]
    coords_bck=[RATE*3,RATE*14,RATE*4,RATE*12]
    index=18
    trans=True
    def __init__(self,pos,world,create=True,recompile=True,state=0):
        BasicBlock.__init__(self,pos,world,create,recompile)
        t = DoorShutTop((pos[0],pos[1]+1,pos[2]),world,self)
        self.linked=[]
        self.t=t
        self.render()
    def render(self):
        #print "Huhu!"
        #glBegin(GL_QUADS)
        if self.world.getBlockAt((self.pos[0]+1,self.pos[1],self.pos[2])):
            glTexCoord2f(self.coords_fwd[0],self.coords_fwd[3]); glVertex3f(self.pos[0]+ -0.5,self.pos[1]+-0.5,self.pos[2]) #Front
            glTexCoord2f(self.coords_fwd[2],self.coords_fwd[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2])
            glTexCoord2f(self.coords_fwd[2],self.coords_fwd[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+1.5,self.pos[2])
            glTexCoord2f(self.coords_fwd[0],self.coords_fwd[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+1.5,self.pos[2])
        else:
            glTexCoord2f(self.coords_fwd[0],self.coords_fwd[3]); glVertex3f(self.pos[0],self.pos[1]+-0.5,self.pos[2]-0.5) #Front
            glTexCoord2f(self.coords_fwd[2],self.coords_fwd[3]); glVertex3f(self.pos[0],self.pos[1]+-0.5,self.pos[2]+0.5)
            glTexCoord2f(self.coords_fwd[2],self.coords_fwd[1]); glVertex3f(self.pos[0],self.pos[1]+1.5,self.pos[2]+0.5)
            glTexCoord2f(self.coords_fwd[0],self.coords_fwd[1]); glVertex3f(self.pos[0],self.pos[1]+1.5,self.pos[2]-0.5)
        #glEnd()
    def on_kill(self):
        #print t
        self.world.killBlock(self.t,polite=False,shrapnel=False)
    def on_use(self):
        self.counter(self.pos,self.world)





class DoorOpenTop(BasicBlock):
    particle_colors = [(0.3,0.14,0.0)]
    #trans=True
    o_name="Open Door"
    o_solid=False
    o_usable=True
    index = -1
    cutoff = False
    trans=True
    def getE(self):
        return (1,1,1,1,1,1)
    def __init__(self,pos,world,below,state=0):
        self.linked=[]
        self.below=below
        
        BasicBlock.__init__(self,pos,world,recompile=False)
        #self.render()
    def render(self):
        pass
    def on_kill(self):
        self.world.killBlock(self.below,polite=False,shrapnel=False)
    def on_use(self):
        self.below.on_use()
##    def on_use(self):
##        self.dob((self.pos[0],self.pos[1]-1,self.pos[2]),self.world)
        
        

class DoorOpenBottom(BasicBlock):
    particle_colors = [(0.3,0.14,0.0)]
    o_name="Open Door"
    #trans=True
    o_solid=False
    o_usable=True
    cutoff = False
    def getE(self):
        return (1,1,1,1,1,1)
    counter=DoorShutBottom
    coords_top=[RATE*3,RATE*14,RATE*4,RATE*12]
    coords_btm=[RATE*3,RATE*14,RATE*4,RATE*12]
    coords_lft=[RATE*3,RATE*14,RATE*4,RATE*12]
    coords_rgt=[RATE*3,RATE*14,RATE*4,RATE*12]
    coords_fwd=[RATE*3,RATE*14,RATE*4,RATE*12]
    coords_bck=[RATE*3,RATE*14,RATE*4,RATE*12]
    index=19
    trans=True
    def __init__(self,pos,world,create=True,recompile=True,state=0):
        BasicBlock.__init__(self,pos,world,create,recompile)
        t = DoorShutTop((pos[0],pos[1]+1,pos[2]),world,self)
        self.linked=[]
        self.t=t
        #self.render()
    def render(self):
        #print "Huhu!"
        #glBegin(GL_QUADS)
        if self.world.getBlockAt((self.pos[0]+1,self.pos[1],self.pos[2])):
            glTexCoord2f(self.coords_fwd[0],self.coords_fwd[3]); glVertex3f(self.pos[0]-0.499,self.pos[1]+-0.5,self.pos[2]) #Front
            glTexCoord2f(self.coords_fwd[2],self.coords_fwd[3]); glVertex3f(self.pos[0]-0.499,self.pos[1]+-0.5,self.pos[2]+1)
            glTexCoord2f(self.coords_fwd[2],self.coords_fwd[1]); glVertex3f(self.pos[0]-0.499,self.pos[1]+1.5,self.pos[2]+1)
            glTexCoord2f(self.coords_fwd[0],self.coords_fwd[1]); glVertex3f(self.pos[0]-0.499,self.pos[1]+1.5,self.pos[2])
        else:
            glTexCoord2f(self.coords_fwd[0],self.coords_fwd[3]); glVertex3f(self.pos[0],self.pos[1]+-0.5,self.pos[2]-0.499) #Front
            glTexCoord2f(self.coords_fwd[2],self.coords_fwd[3]); glVertex3f(self.pos[0]+1,self.pos[1]+-0.5,self.pos[2]-0.499)
            glTexCoord2f(self.coords_fwd[2],self.coords_fwd[1]); glVertex3f(self.pos[0]+1,self.pos[1]+1.5,self.pos[2]-0.499)
            glTexCoord2f(self.coords_fwd[0],self.coords_fwd[1]); glVertex3f(self.pos[0],self.pos[1]+1.5,self.pos[2]-0.499)
        #glEnd()
    def on_kill(self):
        #print t
        self.world.killBlock(self.t,polite=False,shrapnel=False)
    def on_use(self):
        self.counter(self.pos,self.world)


DoorShutBottom.counter=DoorOpenBottom

    
class PlankBlock(BasicBlock):
    particle_colors = [(1.0,1.0,0.0,1.0),(0.5,0.25,0.0,1.0),(0.3,0.14,0.0)]
    o_name="Planks"
    index=17
    coords_top=[RATE*2,RATE*14,RATE*3,RATE*13]
    coords_btm=[RATE*2,RATE*14,RATE*3,RATE*13]
    coords_lft=[RATE*2,RATE*14,RATE*3,RATE*13]
    coords_rgt=[RATE*2,RATE*14,RATE*3,RATE*13]
    coords_fwd=[RATE*2,RATE*14,RATE*3,RATE*13]
    coords_bck=[RATE*2,RATE*14,RATE*3,RATE*13]
class GrassBlock(BasicBlock):
    particle_colors = [(0.5,0.25,0.0,1.0),(0.0,0.8,0.0,1.0)]
    o_name="Grass"
    index=2
    coords_top=[RATE*0,RATE*15,RATE*1,RATE*14]
    coords_btm=[RATE*0,RATE*16,RATE*1,RATE*15]
    coords_lft=[RATE*0,RATE*14,RATE*1,RATE*13]
    coords_rgt=[RATE*0,RATE*14,RATE*1,RATE*13]
    coords_fwd=[RATE*0,RATE*14,RATE*1,RATE*13]
    coords_bck=[RATE*0,RATE*14,RATE*1,RATE*13]

class DirtBlock(BasicBlock):
    particle_colors = [(0.5,0.25,0.0,1.0)]
    o_name="Dirt"
    index=1
    coords_top=[RATE*0,RATE*16,RATE*1,RATE*15]
    coords_btm=[RATE*0,RATE*16,RATE*1,RATE*15]
    coords_lft=[RATE*0,RATE*16,RATE*1,RATE*15]
    coords_rgt=[RATE*0,RATE*16,RATE*1,RATE*15]
    coords_fwd=[RATE*0,RATE*16,RATE*1,RATE*15]
    coords_bck=[RATE*0,RATE*16,RATE*1,RATE*15]
    o_changesTo=GrassBlock

class RockBlock(BasicBlock):
    particle_colors = [(0.4,0.4,0.4,1.0),(0.5,0.5,0.5,1.0),(0.6,0.6,0.6,1.0)]
    o_name="Rock"
    index=4
    coords_top=[RATE*1,RATE*16,RATE*2,RATE*15]
    coords_btm=[RATE*1,RATE*16,RATE*2,RATE*15]
    coords_lft=[RATE*1,RATE*16,RATE*2,RATE*15]
    coords_rgt=[RATE*1,RATE*16,RATE*2,RATE*15]
    coords_fwd=[RATE*1,RATE*16,RATE*2,RATE*15]
    coords_bck=[RATE*1,RATE*16,RATE*2,RATE*15]
    
class WoodBlock(BasicBlock):
    particle_colors = [(0.3,0.14,0.0,1.0),(0.1,0.25,0.0,1.0)]
    o_name="Wood"
    index=3
    coords_top=[RATE*2,RATE*15,RATE*3,RATE*14]
    coords_btm=[RATE*2,RATE*15,RATE*3,RATE*14]
    coords_lft=[RATE*2,RATE*16,RATE*3,RATE*15]
    coords_rgt=[RATE*2,RATE*16,RATE*3,RATE*15]
    coords_fwd=[RATE*2,RATE*16,RATE*3,RATE*15]
    coords_bck=[RATE*2,RATE*16,RATE*3,RATE*15]

class LeafBlock(BasicBlock):
    particle_colors = [(0.0,0.8,0.0,1.0)]
    o_name="Leaf"
    index=5
    cutoff = False
    dcutoff = False
    trans=True
    coords_top=[RATE*4,RATE*16,RATE*5,RATE*15]
    coords_btm=[RATE*4,RATE*16,RATE*5,RATE*15]
    coords_lft=[RATE*4,RATE*16,RATE*5,RATE*15]
    coords_rgt=[RATE*4,RATE*16,RATE*5,RATE*15]
    coords_fwd=[RATE*4,RATE*16,RATE*5,RATE*15]
    coords_bck=[RATE*4,RATE*16,RATE*5,RATE*15]

class ApplesNLeavesBlock(BasicBlock):
    particle_colors = [(0.0,0.8,0.0,1.0),(0.8,0.0,0.0,1.0)]
    o_name="Apples"
    index=6
    o_changesTo=LeafBlock
    coords_top=[RATE*5,RATE*16,RATE*6,RATE*15]
    coords_btm=[RATE*5,RATE*16,RATE*6,RATE*15]
    coords_lft=[RATE*5,RATE*16,RATE*6,RATE*15]
    coords_rgt=[RATE*5,RATE*16,RATE*6,RATE*15]
    coords_fwd=[RATE*5,RATE*16,RATE*6,RATE*15]
    coords_bck=[RATE*5,RATE*16,RATE*6,RATE*15]
#LeafBlock.o_changesTo = ApplesNLeavesBlock

class RedCloth(BasicBlock):
    particle_colors = [(1.0,0.0,0.0,1.0),(0.8,0.0,0.0,1.0)]
    index=7
    o_name="Cloth"
    coords_top=[RATE*0,RATE*2,RATE*1,RATE*1]
    coords_btm=[RATE*0,RATE*2,RATE*1,RATE*1]
    coords_lft=[RATE*0,RATE*2,RATE*1,RATE*1]
    coords_rgt=[RATE*0,RATE*2,RATE*1,RATE*1]
    coords_fwd=[RATE*0,RATE*2,RATE*1,RATE*1]
    coords_bck=[RATE*0,RATE*2,RATE*1,RATE*1]

class GreenCloth(BasicBlock):
    particle_colors = [(0.0,1.0,0.0,1.0),(0.0,0.75,0.0,1.0),(0.0,0.5,0.0,1.0)]
    o_name="Cloth"
    index=10
    coords_top=[RATE*3,RATE*2,RATE*4,RATE*1]
    coords_btm=[RATE*3,RATE*2,RATE*4,RATE*1]
    coords_lft=[RATE*3,RATE*2,RATE*4,RATE*1]
    coords_rgt=[RATE*3,RATE*2,RATE*4,RATE*1]
    coords_fwd=[RATE*3,RATE*2,RATE*4,RATE*1]
    coords_bck=[RATE*3,RATE*2,RATE*4,RATE*1]

class BlueCloth(BasicBlock):
    particle_colors = [(0.1,0.1,1.0,1.0),(0.0,0.0,1.0,1.0),(0.0,0.0,0.8,1.0)]
    o_name="Cloth"
    index=12
    coords_top=[RATE*5,RATE*2,RATE*6,RATE*1]
    coords_btm=[RATE*5,RATE*2,RATE*6,RATE*1]
    coords_lft=[RATE*5,RATE*2,RATE*6,RATE*1]
    coords_rgt=[RATE*5,RATE*2,RATE*6,RATE*1]
    coords_fwd=[RATE*5,RATE*2,RATE*6,RATE*1]
    coords_bck=[RATE*5,RATE*2,RATE*6,RATE*1]

class OrangeCloth(BasicBlock):
    particle_colors = [(1.0,0.5,0.0,1.0)]
    o_name="Cloth"
    index=8
    coords_top=[RATE*1,RATE*2,RATE*2,RATE*1]
    coords_btm=[RATE*1,RATE*2,RATE*2,RATE*1]
    coords_lft=[RATE*1,RATE*2,RATE*2,RATE*1]
    coords_rgt=[RATE*1,RATE*2,RATE*2,RATE*1]
    coords_fwd=[RATE*1,RATE*2,RATE*2,RATE*1]
    coords_bck=[RATE*1,RATE*2,RATE*2,RATE*1]

class YellowCloth(BasicBlock):
    particle_colors = [(1.0,1.0,0.0,1.0)]
    o_name="Cloth"
    index=9
    coords_top=[RATE*2,RATE*2,RATE*3,RATE*1]
    coords_btm=[RATE*2,RATE*2,RATE*3,RATE*1]
    coords_lft=[RATE*2,RATE*2,RATE*3,RATE*1]
    coords_rgt=[RATE*2,RATE*2,RATE*3,RATE*1]
    coords_fwd=[RATE*2,RATE*2,RATE*3,RATE*1]
    coords_bck=[RATE*2,RATE*2,RATE*3,RATE*1]

class CyanCloth(BasicBlock):
    particle_colors = [(0.0,1.0,1.0,1.0),(0.0,0.9,0.9,1.0)]
    o_name="Cloth"
    index=11
    coords_top=[RATE*4,RATE*2,RATE*5,RATE*1]
    coords_btm=[RATE*4,RATE*2,RATE*5,RATE*1]
    coords_lft=[RATE*4,RATE*2,RATE*5,RATE*1]
    coords_rgt=[RATE*4,RATE*2,RATE*5,RATE*1]
    coords_fwd=[RATE*4,RATE*2,RATE*5,RATE*1]
    coords_bck=[RATE*4,RATE*2,RATE*5,RATE*1]

class PurpleCloth(BasicBlock):
    particle_colors = [(0.5,0.0,0.5,1.0)]
    o_name="Cloth"
    index=13
    coords_top=[RATE*6,RATE*2,RATE*7,RATE*1]
    coords_btm=[RATE*6,RATE*2,RATE*7,RATE*1]
    coords_lft=[RATE*6,RATE*2,RATE*7,RATE*1]
    coords_rgt=[RATE*6,RATE*2,RATE*7,RATE*1]
    coords_fwd=[RATE*6,RATE*2,RATE*7,RATE*1]
    coords_bck=[RATE*6,RATE*2,RATE*7,RATE*1]

class BlackCloth(BasicBlock):
    particle_colors = [(0.0,0.0,0.0,1.0),(0.1,0.1,0.1,1.0),(0.2,0.2,0.2,1.0)]
    o_name="Cloth"
    index=14
    coords_top=[RATE*7,RATE*2,RATE*8,RATE*1]
    coords_btm=[RATE*7,RATE*2,RATE*8,RATE*1]
    coords_lft=[RATE*7,RATE*2,RATE*8,RATE*1]
    coords_rgt=[RATE*7,RATE*2,RATE*8,RATE*1]
    coords_fwd=[RATE*7,RATE*2,RATE*8,RATE*1]
    coords_bck=[RATE*7,RATE*2,RATE*8,RATE*1]

class GrayCloth(BasicBlock):
    particle_colors = [(0.4,0.4,0.4,1.0),(0.5,0.5,0.5,1.0),(0.6,0.6,0.6,1.0)]
    o_name="Cloth"
    index=15
    coords_top=[RATE*8,RATE*2,RATE*9,RATE*1]
    coords_btm=[RATE*8,RATE*2,RATE*9,RATE*1]
    coords_lft=[RATE*8,RATE*2,RATE*9,RATE*1]
    coords_rgt=[RATE*8,RATE*2,RATE*9,RATE*1]
    coords_fwd=[RATE*8,RATE*2,RATE*9,RATE*1]
    coords_bck=[RATE*8,RATE*2,RATE*9,RATE*1]

class WhiteCloth(BasicBlock):
    particle_colors = [(1.0,1.0,1.0,1.0),(0.9,0.9,0.9,1.0),(0.8,0.8,0.8,1.0)]
    o_name="Cloth"
    index=16
    coords_top=[RATE*9,RATE*2,RATE*10,RATE*1]
    coords_btm=[RATE*9,RATE*2,RATE*10,RATE*1]
    coords_lft=[RATE*9,RATE*2,RATE*10,RATE*1]
    coords_rgt=[RATE*9,RATE*2,RATE*10,RATE*1]
    coords_fwd=[RATE*9,RATE*2,RATE*10,RATE*1]
    coords_bck=[RATE*9,RATE*2,RATE*10,RATE*1]
    
class FastCube:
    def __init__(self,pos,vel=(0,0,0)):
        self.coords=[RATE*1,RATE*15,RATE*2,RATE*14]
        self.pos=[-pos[0],pos[1],pos[2]]
        self.vel=vel
    def render(self):
        self.pos[0]+=self.vel[0]
        self.pos[1]+=self.vel[1]
        self.pos[2]+=self.vel[2]
        glBegin(GL_QUADS)
        #glColor(0.5,0.5,0.5,1.0);
        glNormal3f(0,0,1)
        glTexCoord2f(self.coords[0],self.coords[3]); glVertex3f(self.pos[0]+ -0.5,self.pos[1]+-0.5,self.pos[2]+0.5) #Front
        glTexCoord2f(self.coords[2],self.coords[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords[2],self.coords[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords[0],self.coords[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glNormal3f(0,0,-1)
        #glColor(0,1,0,1.0);
        glTexCoord2f(self.coords[2],self.coords[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords[0],self.coords[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5) #Back
        glTexCoord2f(self.coords[0],self.coords[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords[2],self.coords[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glNormal3f(0,-1,0)
        #glColor(0,0,1,1.0);
        glTexCoord2f(self.coords[2],self.coords[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5) #Bottom
        glTexCoord2f(self.coords[0],self.coords[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords[0],self.coords[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords[2],self.coords[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glNormal3f(0,1,0)
        #glColor(1,1,0,1.0);
        glTexCoord2f(self.coords[0],self.coords[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #Top
        glTexCoord2f(self.coords[2],self.coords[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords[2],self.coords[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords[0],self.coords[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glNormal3f(-1,0,0)
        #glColor(0,1,1,1.0);
        glTexCoord2f(self.coords[0],self.coords[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords[0],self.coords[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #left
        glTexCoord2f(self.coords[2],self.coords[1]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords[2],self.coords[3]); glVertex3f(self.pos[0]+-0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glNormal3f(1,0,0)
        #glColor(1,0,1,1.0);
        glTexCoord2f(self.coords[2],self.coords[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+-0.5)
        glTexCoord2f(self.coords[2],self.coords[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+-0.5) #right
        glTexCoord2f(self.coords[0],self.coords[1]); glVertex3f(self.pos[0]+0.5,self.pos[1]+0.5,self.pos[2]+0.5)
        glTexCoord2f(self.coords[0],self.coords[3]); glVertex3f(self.pos[0]+0.5,self.pos[1]+-0.5,self.pos[2]+0.5)
        glEnd() 

def render_lamocube(coords_fwd,coords_bck,coords_btm,coords_top,coords_lft,coords_rgt):
    glBegin(GL_QUADS)
    #glColor(0.5,0.5,0.5,1.0);
    glNormal3f(0,0,1)
    glTexCoord2f(coords_fwd[0],coords_fwd[3]); glVertex3f(+ -0.5,+-0.5,+0.5) #Front
    glTexCoord2f(coords_fwd[2],coords_fwd[3]); glVertex3f(+0.5,+-0.5,+0.5)
    glTexCoord2f(coords_fwd[2],coords_fwd[1]); glVertex3f(+0.5,+0.5,+0.5)
    glTexCoord2f(coords_fwd[0],coords_fwd[1]); glVertex3f(+-0.5,+0.5,+0.5)
    glNormal3f(0,0,-1)
    #glColor(0,1,0,1.0);
    glTexCoord2f(coords_bck[2],coords_bck[3]); glVertex3f(+-0.5,+-0.5,+-0.5)
    glTexCoord2f(coords_bck[0],coords_bck[3]); glVertex3f(+0.5,+-0.5,+-0.5) #Back
    glTexCoord2f(coords_bck[0],coords_bck[1]); glVertex3f(+0.5,+0.5,+-0.5)
    glTexCoord2f(coords_bck[2],coords_bck[1]); glVertex3f(+-0.5,+0.5,+-0.5)
    glNormal3f(0,-1,0)
    #glColor(0,0,1,1.0);
    glTexCoord2f(coords_btm[2],coords_btm[1]); glVertex3f(+-0.5,+-0.5,+-0.5) #Bottom
    glTexCoord2f(coords_btm[0],coords_btm[1]); glVertex3f(+0.5,+-0.5,+-0.5)
    glTexCoord2f(coords_btm[0],coords_btm[3]); glVertex3f(+0.5,+-0.5,+0.5)
    glTexCoord2f(coords_btm[2],coords_btm[3]); glVertex3f(+-0.5,+-0.5,+0.5)
    glNormal3f(0,1,0)
    #glColor(1,1,0,1.0);
    glTexCoord2f(coords_top[0],coords_top[1]); glVertex3f(+-0.5,+0.5,+-0.5) #Top
    glTexCoord2f(coords_top[2],coords_top[1]); glVertex3f(+0.5,+0.5,+-0.5)
    glTexCoord2f(coords_top[2],coords_top[3]); glVertex3f(+0.5,+0.5,+0.5)
    glTexCoord2f(coords_top[0],coords_top[3]); glVertex3f(+-0.5,+0.5,+0.5)
    glNormal3f(-1,0,0)
    #glColor(0,1,1,1.0);
    glTexCoord2f(coords_lft[0],coords_lft[3]); glVertex3f(+-0.5,+-0.5,+-0.5)
    glTexCoord2f(coords_lft[0],coords_lft[1]); glVertex3f(+-0.5,+0.5,+-0.5) #left
    glTexCoord2f(coords_lft[2],coords_lft[1]); glVertex3f(+-0.5,+0.5,+0.5)
    glTexCoord2f(coords_lft[2],coords_lft[3]); glVertex3f(+-0.5,+-0.5,+0.5)
    glNormal3f(1,0,0)
    #glColor(1,0,1,1.0);
    glTexCoord2f(coords_rgt[2],coords_rgt[3]); glVertex3f(+0.5,+-0.5,+-0.5)
    glTexCoord2f(coords_rgt[2],coords_rgt[1]); glVertex3f(+0.5,+0.5,+-0.5) #right
    glTexCoord2f(coords_rgt[0],coords_rgt[1]); glVertex3f(+0.5,+0.5,+0.5)
    glTexCoord2f(coords_rgt[0],coords_rgt[3]); glVertex3f(+0.5,+-0.5,+0.5)
    glEnd() 
