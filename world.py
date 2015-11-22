

class Player:
    def __init__(self,spawn,name="Anonymous",health=10):
        self.name=name
        self.health=health
        self.pos=spawn
        self.angle=[0,0,0]
        self.spawn=spawn
        self.accel=0

    def move(self,w,a,s,d):
        pass
        

class BasicWorldManager2:
    def __init__(self,options):
        self.blocks = {}
        self.display_list = glGenLists(1)
        self.new = glGenLists(1)
        self.changeables = []
        #glNewList(self.display_list, GL_COMPILE)
##        for y in range(-3,4):
##            for x in range(-3,4):
##                self.setBlockAt(choice(options)((x,-1,y),self,False))
                #self.blocks[(x,-2,y)].render()
        #glEndList()
        self.recompile()
        self.needs_update=False
        self.saveName=None
        self.background = 0.45, 0.7, 1.0
        self.sky = 1.0
        self.sky_inc = -0.0005
        self.dynamicules = []
        self.particles = []
    

    
    def trackPointer(self):
        pos = [self.player_pos[0],self.player_pos[1],-self.player_pos[2]][:]
        vel = self.getVelocity()
        for _ in range(500):
            y= self.getBlockAt(self.getARB_RP(pos[0],pos[1],pos[2]))
            if y:
                if y.name != "Water":break
            pos[0]+=vel[0]
            pos[1]+=vel[1]
            pos[2]+=vel[2]
            pass
        return self.getBlockAt(self.getARB_RP(pos[0],pos[1],pos[2]))

    def save(self):
        f=open("worlds/"+self.saveName,"w")
        s=self.spawn_point[:]
        f.write(str(s[0])+" "+str(s[1])+" "+str(s[2])+"\n")
        for block_at in self.blocks.keys():
            if self.blocks[block_at].index > -1 :
                f.write(str(self.blocks[block_at].index)+" ")
            #except Exception as e: print "Error: "+str(exception)
                f.write(str(block_at[0])+" ")
                f.write(str(block_at[1])+" ")
                f.write(str(block_at[2])+" ")
                #print str(self.blocks[block_at].getState())
                f.write(str(self.blocks[block_at].getState()))
                f.write("\n")
        f.close()
    
    def getVelocity(self):
        y,x,z = self.player_angle
        return (sin(radians(x))*cos(radians(y))*0.05,
                 -sin(radians(y))*0.05,
                 -cos(radians(x))*cos(radians(y))*0.05)
    
    def setBlockAt(self,block,recompile=False):
        if block.pos in self.blocks.keys(): self.killBlock(self.blocks[block.pos],shrapnel=False)
        self.blocks[block.pos] = block
        if block.changesTo:self.changeables.append(block.pos)
        #self.display_list = glGenLists(1)
        #print self.display_list
        if recompile: self.recompile("A "+block.name)
        if block.dynamic:
            #print "Init dynamicule"
            self.dynamicules.append(block)
        
    
    def killBlock(self,block,recompile=False,polite=True,shrapnel=True):
        if shrapnel:
            for _ in range(randint(3,7)):
                r=[block.pos[0]+random()-0.5,block.pos[1]+random()-0.5,block.pos[2]+random()-0.5]
                self.particles.append(SimpleParticle(self,r,choice(block.particle_colors)))
        del self.blocks[block.pos]
        if block.changesTo:self.changeables.remove(block.pos)
        if polite: block.on_kill()
        if recompile: self.recompile()
        if block.dynamic:
            #print "Kill dynamicule"
            self.dynamicules.remove(block)

    def getNeighboringCurrents(self,pos):
        currents = [0,0,0,0,0,0]
        y=self.getBlockAt((pos[0]-1,pos[1],pos[2]))
        if y: currents[0] = y.getE()[0]
        y=self.getBlockAt((pos[0]+1,pos[1],pos[2]))
        if y: currents[1] = y.getE()[1]
        y=self.getBlockAt((pos[0],pos[1]+1,pos[2]))
        if y: currents[2] = y.getE()[2]
        y=self.getBlockAt((pos[0],pos[1]-1,pos[2]))
        if y: currents[3] = y.getE()[3]
        y=self.getBlockAt((pos[0],pos[1],pos[2]+1))
        if y: currents[4] = y.getE()[4]
        y=self.getBlockAt((pos[0],pos[1],pos[2]-1))
        if y: currents[5] = y.getE()[5]
        return tuple(currents)
    
    def collideTest(self,p):
        if p in self.blocks.keys():
            if self.blocks[p].solid:
                return True
        return False

    def getAmbient(self):
        y=self.getBlockAt(self.getRoundedPos())
        if y:
            if y.name == "Water":
                return (0.6,0.6,1.0,1.0)
        #if self.player_pos[1] < -1:
        #    return (0.6,0.6,1.0,1.0)
        return (1.0,1.0,1.0,1.0)
        
    
    def getRoundedPos(self,off_x=0,off_y=0,off_z=0):
        return (int(round(self.player_pos[0]+off_x)),int(round(self.player_pos[1]+off_y)),int(round(-self.player_pos[2]+off_z)))
    def getARB_RP(self,x,y,z):
        return (int(round(x)),int(round(y)),int(round(z)))
    def getCollide(self):
        return self.collideTest(self.getRoundedPos(-.1,0,-.1)) or \
                self.collideTest(self.getRoundedPos(.1,0,-.1)) or \
                self.collideTest(self.getRoundedPos(.1,0,.1)) or \
                self.collideTest(self.getRoundedPos(-.1,0,.1)) or \
                self.collideTest(self.getRoundedPos(-.125,0,0)) or \
                self.collideTest(self.getRoundedPos(.125,0,0)) or \
                self.collideTest(self.getRoundedPos(0,0,-.125)) or \
                self.collideTest(self.getRoundedPos(0,0,.125)) or \
                self.collideTest(self.getRoundedPos(-.1,-0.75,-.1)) or \
                self.collideTest(self.getRoundedPos(.1,-0.75,-.1)) or \
                self.collideTest(self.getRoundedPos(.1,-0.75,.1)) or \
                self.collideTest(self.getRoundedPos(-.1,-0.75,.1)) or \
                self.collideTest(self.getRoundedPos(-.125,-0.75,0)) or \
                self.collideTest(self.getRoundedPos(.125,-0.75,0)) or \
                self.collideTest(self.getRoundedPos(0,-0.75,-.125)) or \
                self.collideTest(self.getRoundedPos(0,-0.75,.125)) or \
                self.collideTest(self.getRoundedPos(-.1,-1.5,-.1)) or \
                self.collideTest(self.getRoundedPos(.1,-1.5,-.1)) or \
                self.collideTest(self.getRoundedPos(.1,-1.5,.1)) or \
                self.collideTest(self.getRoundedPos(-.1,-1.5,.1)) or \
                self.collideTest(self.getRoundedPos(-.125,-1.5,0)) or \
                self.collideTest(self.getRoundedPos(.125,-1.5,0)) or \
                self.collideTest(self.getRoundedPos(0,-1.5,-.125)) or \
                self.collideTest(self.getRoundedPos(0,-1.5,.125))
    
    def createBlock(self,block):
        self.blocks[block.pos] = block
    def getBlockAt(self,pos):
        try: return self.blocks[pos]
        except KeyError: return None
    
    def updateBlocks(self):
        for block in self.blocks.keys():
            b = self.blocks[block]
            if b.name != "Totally Boring":pass #print b.name
            if b.changesTo:
                #print "tink!"
                if b.countdown: b.countdown -= 1
                else:
                    #b.countdown=randint(30,60)
                    b.changesTo(b.pos,self)
    
    def updateOneRandomBlock(self):
            if not self.changeables and not self.dynamicules: return
            if self.changeables:
                block = choice(self.changeables)
                b = self.blocks[block]
                #if b.name != "Totally Boring":print b.name
                if b.changesTo:
                    #print "tink!"
                    if b.countdown: b.countdown -= 1
                    else:
                        b.countdown=randint(30,60)
                        b.changesTo(b.pos,self)
            #if self.dynamicules:
                #b2 = choice(self.dynamicules)
            #n = self.
            cnt = len(self.dynamicules)/5+1
            for b2i in self.dynamicules[:cnt]:
                if b2i in self.dynamicules:
                    #print self.dynamicules
                    self.dynamicules.remove(b2i)
                    self.dynamicules.append(b2i)
                    b2i.on_dynamic_update()

    def recompile(self,sender="Anonymous"):
        #logdata("A recompile occurred; it took "+str(
        start = time()
        glNewList(self.display_list, GL_COMPILE)
        glBegin(GL_QUADS)
        nblocks = len(self.blocks.keys())
        i = 0
        for block in self.blocks.keys():
            #print i,"\t",nblocks
            i+=1
            if not self.blocks[block].dynamic:self.blocks[block].render()
        glEnd()
        glEndList()
        end = time()
        elapse = end-start
        
        if nblocks == 0: nblocks = -1
        #print type(elapse),type(nblocks)
        dat = ("%.3f\t" % ((end-start)*1000)) + \
              (str(len(list(self.blocks.keys())))+"\t") + \
              str(elapse / nblocks)
        logdata(dat)

    def doSky(self):
        self.sky += self.sky_inc
        if self.sky < 0:
            self.sky = 0
            self.sky_inc = -self.sky_inc
        if self.sky > 1:
            self.sky = 1
            self.sky_inc = -self.sky_inc
        
        #glClearColor(background[0]*sky,background[1]*sky,background[2]*sky,1.0)
        glClearColor(max(self.background[0]-self.sky,0),max(self.background[1]-self.sky,0),max(self.background[2]-self.sky,0),1.0)
            
    def render(self):
        #3333#print "RENDER"
        #print self.needs_update
            #thread.start_new_thread(buildThread,tuple())
        glCallList(self.display_list)
        self.needs_update=False
        glBegin(GL_QUADS)
        for b in self.dynamicules:
            #print "Hup!"
            b.render()
        glEnd()

class BasicWorldManager:
    def __init__(self,options):
        self.player_pos = [1,10,0]
        self.player_angle= [0,0,0]
        self.blocks = {}
        self.display_list = glGenLists(1)
        self.new = glGenLists(1)
        self.changeables = []
        #glNewList(self.display_list, GL_COMPILE)
##        for y in range(-3,4):
##            for x in range(-3,4):
##                self.setBlockAt(choice(options)((x,-1,y),self,False))
                #self.blocks[(x,-2,y)].render()
        #glEndList()
        self.recompile()
        self.needs_update=False
        self.player_accel=0
        self.saveName=None
        self.spawn_point = [0,10,0]
        self.background = 0.45, 0.7, 1.0
        self.sky = 1.0
        self.sky_inc = -0.0005
        self.dynamicules = []
        self.particles = []
    

    
    def trackPointer(self):
        pos = [self.player_pos[0],self.player_pos[1],-self.player_pos[2]][:]
        vel = self.getVelocity()
        for _ in range(500):
            y= self.getBlockAt(self.getARB_RP(pos[0],pos[1],pos[2]))
            if y:
                if y.name != "Water":break
            pos[0]+=vel[0]
            pos[1]+=vel[1]
            pos[2]+=vel[2]
            pass
        return self.getBlockAt(self.getARB_RP(pos[0],pos[1],pos[2]))

    def save(self):
        f=open("worlds/"+self.saveName,"w")
        s=self.spawn_point[:]
        f.write(str(s[0])+" "+str(s[1])+" "+str(s[2])+"\n")
        for block_at in self.blocks.keys():
            if self.blocks[block_at].index > -1 :
                f.write(str(self.blocks[block_at].index)+" ")
            #except Exception as e: print "Error: "+str(exception)
                f.write(str(block_at[0])+" ")
                f.write(str(block_at[1])+" ")
                f.write(str(block_at[2])+" ")
                #print str(self.blocks[block_at].getState())
                f.write(str(self.blocks[block_at].getState()))
                f.write("\n")
        f.close()
    
    def getVelocity(self):
        y,x,z = self.player_angle
        return (sin(radians(x))*cos(radians(y))*0.05,
                 -sin(radians(y))*0.05,
                 -cos(radians(x))*cos(radians(y))*0.05)
    
    def setBlockAt(self,block,recompile=False):
        if block.pos in self.blocks.keys(): self.killBlock(self.blocks[block.pos],shrapnel=False)
        self.blocks[block.pos] = block
        if block.changesTo:self.changeables.append(block.pos)
        #self.display_list = glGenLists(1)
        #print self.display_list
        if recompile: self.recompile("A "+block.name)
        if block.dynamic:
            #print "Init dynamicule"
            self.dynamicules.append(block)
        
    
    def killBlock(self,block,recompile=False,polite=True,shrapnel=True):
        if shrapnel:
            for _ in range(randint(3,7)):
                r=[block.pos[0]+random()-0.5,block.pos[1]+random()-0.5,block.pos[2]+random()-0.5]
                self.particles.append(SimpleParticle(self,r,(block.coords_lft[0]+(random()*RATE),block.coords_lft[3]+(random()*RATE))))
        del self.blocks[block.pos]
        if block.changesTo:self.changeables.remove(block.pos)
        if polite: block.on_kill()
        if recompile: self.recompile()
        if block.dynamic:
            #print "Kill dynamicule"
            self.dynamicules.remove(block)

    def getNeighboringCurrents(self,pos):
        currents = [0,0,0,0,0,0]
        y=self.getBlockAt((pos[0]-1,pos[1],pos[2]))
        if y: currents[0] = y.getE()[0]
        y=self.getBlockAt((pos[0]+1,pos[1],pos[2]))
        if y: currents[1] = y.getE()[1]
        y=self.getBlockAt((pos[0],pos[1]+1,pos[2]))
        if y: currents[2] = y.getE()[2]
        y=self.getBlockAt((pos[0],pos[1]-1,pos[2]))
        if y: currents[3] = y.getE()[3]
        y=self.getBlockAt((pos[0],pos[1],pos[2]+1))
        if y: currents[4] = y.getE()[4]
        y=self.getBlockAt((pos[0],pos[1],pos[2]-1))
        if y: currents[5] = y.getE()[5]
        return tuple(currents)
    
    def collideTest(self,p):
        if p in self.blocks.keys():
            if self.blocks[p].solid:
                return True
        return False

    def getAmbient(self):
        y=self.getBlockAt(self.getRoundedPos())
        if y:
            if y.name == "Water":
                return (0.6,0.6,1.0,1.0)
        return (1.0,1.0,1.0,1.0)
        
    
    def getRoundedPos(self,off_x=0,off_y=0,off_z=0):
        return (int(round(self.player_pos[0]+off_x)),int(round(self.player_pos[1]+off_y)),int(round(-self.player_pos[2]+off_z)))
    def getARB_RP(self,x,y,z):
        return (int(round(x)),int(round(y)),int(round(z)))
    def getCollide(self):
        return self.collideTest(self.getRoundedPos(-.1,0,-.1)) or \
                self.collideTest(self.getRoundedPos(.1,0,-.1)) or \
                self.collideTest(self.getRoundedPos(.1,0,.1)) or \
                self.collideTest(self.getRoundedPos(-.1,0,.1)) or \
                self.collideTest(self.getRoundedPos(-.125,0,0)) or \
                self.collideTest(self.getRoundedPos(.125,0,0)) or \
                self.collideTest(self.getRoundedPos(0,0,-.125)) or \
                self.collideTest(self.getRoundedPos(0,0,.125)) or \
                self.collideTest(self.getRoundedPos(-.1,-0.75,-.1)) or \
                self.collideTest(self.getRoundedPos(.1,-0.75,-.1)) or \
                self.collideTest(self.getRoundedPos(.1,-0.75,.1)) or \
                self.collideTest(self.getRoundedPos(-.1,-0.75,.1)) or \
                self.collideTest(self.getRoundedPos(-.125,-0.75,0)) or \
                self.collideTest(self.getRoundedPos(.125,-0.75,0)) or \
                self.collideTest(self.getRoundedPos(0,-0.75,-.125)) or \
                self.collideTest(self.getRoundedPos(0,-0.75,.125)) or \
                self.collideTest(self.getRoundedPos(-.1,-1.5,-.1)) or \
                self.collideTest(self.getRoundedPos(.1,-1.5,-.1)) or \
                self.collideTest(self.getRoundedPos(.1,-1.5,.1)) or \
                self.collideTest(self.getRoundedPos(-.1,-1.5,.1)) or \
                self.collideTest(self.getRoundedPos(-.125,-1.5,0)) or \
                self.collideTest(self.getRoundedPos(.125,-1.5,0)) or \
                self.collideTest(self.getRoundedPos(0,-1.5,-.125)) or \
                self.collideTest(self.getRoundedPos(0,-1.5,.125))
    
    def createBlock(self,block):
        self.blocks[block.pos] = block
    def getBlockAt(self,pos):
        try: return self.blocks[pos]
        except KeyError: return None
    
    def updateBlocks(self):
        for block in self.blocks.keys():
            b = self.blocks[block]
            if b.name != "Totally Boring":pass #print b.name
            if b.changesTo:
                #print "tink!"
                if b.countdown: b.countdown -= 1
                else:
                    #b.countdown=randint(30,60)
                    b.changesTo(b.pos,self)
    
    def updateOneRandomBlock(self):
            if not self.changeables and not self.dynamicules: return
            if self.changeables:
                block = choice(self.changeables)
                b = self.blocks[block]
                #if b.name != "Totally Boring":print b.name
                if b.changesTo:
                    #print "tink!"
                    if b.countdown: b.countdown -= 1
                    else:
                        b.countdown=randint(30,60)
                        b.changesTo(b.pos,self)
            #if self.dynamicules:
                #b2 = choice(self.dynamicules)
            #n = self.
            cnt = len(self.dynamicules)/5+1
            for b2i in self.dynamicules[:cnt]:
                if b2i in self.dynamicules:
                    #print self.dynamicules
                    self.dynamicules.remove(b2i)
                    self.dynamicules.append(b2i)
                    b2i.on_dynamic_update()

    def recompile(self,sender="Anonymous"):
        #logdata("A recompile occurred; it took "+str(
        start = time()
        glNewList(self.display_list, GL_COMPILE)
        glBegin(GL_QUADS)
        nblocks = len(self.blocks.keys())
        i = 0
        for block in self.blocks.keys():
            #print i,"\t",nblocks
            i+=1
            if not self.blocks[block].dynamic:self.blocks[block].render()
        glEnd()
        glEndList()
        end = time()
        elapse = end-start
        
        if nblocks == 0: nblocks = -1
        #print type(elapse),type(nblocks)
        dat = ("%.3f\t" % ((end-start)*1000)) + \
              (str(len(list(self.blocks.keys())))+"\t") + \
              str(elapse / nblocks)
        logdata(dat)

    def doSky(self):
        self.sky += self.sky_inc
        if self.sky < 0:
            self.sky = 0
            self.sky_inc = -self.sky_inc
        if self.sky > 1:
            self.sky = 1
            self.sky_inc = -self.sky_inc
        
        #glClearColor(background[0]*sky,background[1]*sky,background[2]*sky,1.0)
        glClearColor(max(self.background[0]-self.sky,0),max(self.background[1]-self.sky,0),max(self.background[2]-self.sky,0),1.0)
            
    def render(self):
        #3333#print "RENDER"
        #print self.needs_update
            #thread.start_new_thread(buildThread,tuple())
        glCallList(self.display_list)
        self.needs_update=False
        glBegin(GL_QUADS)
        for b in self.dynamicules:
            #print "Hup!"
            b.render()
        glEnd()

#A TEST LINE

