def eventHandler():
    global thread_run
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            thread_run=False
            quit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                thread_run=False
                quit()


def resize(width, height):

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(width)/height, .1, 100000.)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init(clearcolor=(0.45, 0.7, 1.0, 0.0)):

    glEnable(GL_TEXTURE_2D)
    glClearColor(*clearcolor)
    glEnable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)
    glPointSize(50)
    
def updateThread():
    global world
    world.updateOneRandomBlock()

def buildThread():
    pass
