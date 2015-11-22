class Mod:
    def __init__(self,name,description_file,file):
        self.name=name
        self.description=open(description_file,"r").read()
        self.file=file

modList = {"vanilla":Mod("vanilla","mods/vanilla_description.txt","n/a"),
           "Robot Wars!":Mod("Robot Wars!","mods/war_description.txt","mods/war")}

