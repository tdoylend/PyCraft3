import pygame,pgext
images = [
    "AdventureCraft.png"]
for imagename in images:
    image = pygame.image.load(imagename)
    # set 40% alpha
    pgext.color.multiply(image,1,False,False,True)
    pgext.color.multiply(image,0.7,True,True,False)
    pygame.image.save(image, imagename[:-4]+"W"+imagename[-4:])
