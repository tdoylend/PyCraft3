#!/usr/bin/python

"""
__version__ = "$Revision: 1.3 $"
__date__ = "$Date: 2004/04/14 02:38:47 $"
"""
import os,pygame
from PythonCard import model
from mods import modList

class MyBackground(model.Background):

    def on_initialize(self, event):
        data = os.listdir("texture packs/")
        for line in data:
            if line.endswith(".png"):self.components.texlist.append(line.split(".")[0])
        pass
        self.components.modList.items = list(modList.keys())
        self.components.modList.stringSelection="vanilla"
        self.components.texlist.stringSelection="Original"
        self.on_texlist_select(None)
        self.on_modList_select(None)
    def on_texlist_select(self,event):
        print "sel"
        s=pygame.image.load("texture packs/"+self.components.texlist.stringSelection+".png").get_size()
        self.d = s[0]
        self.components.texdat.text = self.components.texlist.stringSelection+"\n"+str(self.d)+"x"+str(self.d)
    def on_saveIt_mouseClick(self,event):
        print "Ok"
        f = open("settings.ini","w")
        f.write(self.components.texlist.stringSelection+"\n")
        f.write(modList[self.components.modList.stringSelection].file)
        f.close()
    def on_modList_select(self,event):
        print "sel2"
        self.components.modData.text = modList[self.components.modList.stringSelection].description
        
        


if __name__ == '__main__':
    app = model.Application(MyBackground)
    app.MainLoop()
