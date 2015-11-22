#glEnable(GL_POINT_SMOOTH)
#glPointSize(10)


class SimpleParticle:
    def __init__(self,world,pos,color,abscolor=False):
        self.pos=list(pos)
        self.color=color
        self.world=world
        self.lifespan = randint(60,90)
        self.vel = [(random()-0.5)/5,random()/5,(random()-0.5)/5]
        self.orient = randint(1,3)
        self.abscolor = abscolor
    def update(self):
        self.vel[1] -= 0.01
        o = self.pos[0]
        self.pos[0] += self.vel[0]
        try:
            if self.world.getBlockAt((int(round(self.pos[0])),int(round(self.pos[1])),int(round(self.pos[2])))).solid:
                self.vel[0] = -self.vel[0]
                self.pos[0] = o
        except:
            pass
        o=self.pos[1]
        self.pos[1] += self.vel[1]
        try:
            if self.world.getBlockAt((int(round(self.pos[0])),int(round(self.pos[1])),int(round(self.pos[2])))).solid:
                self.pos[1]=o
                self.vel = [0,0,0]
        except:
            pass

        o=self.pos[2] 
        self.pos[2] += self.vel[2]
        try:
            if self.world.getBlockAt((int(round(self.pos[0])),int(round(self.pos[1])),int(round(self.pos[2])))).solid:
                self.vel[2] = -self.vel[2]
                self.pos[2] = o
        except:
            pass

        self.lifespan -= 1
        if self.lifespan == 0: self.world.particles.remove(self)
    def render(self):
        glColor(1,1,1)
        if not self.abscolor: glTexCoord2d(*self.color)
        else:
            #glDisable(GL_TEXTURE_2D)
            glColor(*self.color)
        glVertex3d(*self.pos)
        #glEnable(GL_TEXTURE_2D)
class ExplosionParticle(SimpleParticle):
    def __init__(self,world,pos,color):
        self.pos=list(pos)
        self.color=color
        self.world=world
        self.lifespan=randint(60,90)
        self.vel = [(random()-0.5)/3,(random()-0.1)/3,(random()-0.5)/3]
        self.orient = randint(1,3)
        self.abscolor = False
        
        
