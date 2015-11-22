def parseMap(world,map,recompile=False):
    blocklist=[BasicBlock,DirtBlock,GrassBlock,WoodBlock,RockBlock,LeafBlock,ApplesNLeavesBlock,
    RedCloth,OrangeCloth,YellowCloth,GreenCloth,CyanCloth,BlueCloth,
    PurpleCloth,BlackCloth,GrayCloth,WhiteCloth,PlankBlock,DoorShutBottom,
    DoorOpenBottom,Dynamite,Snow,Cake,SwissCheese,Glass,GoldBlock,
    SilverBlock,Water,BrickBlock,HatchShut,HatchOpen,WaterBucket,SandBlock,
    Generator,LED,Switch,Wire,AND,NOT,XOR,Spout,
    ExperimentalPusherRight,ExperimentalPusherLeft,
    ExperimentalPusherUp,ExperimentalPusherBack,
    ExperimentalPusherFront,Button,DyedSand,StickyPusherFront,StickyPusherUp,StickyPusherBack,
    StickyPusherRight,StickyPusherLeft,Chemicals,Bush]#,ExperimentalPusherLeft]
    blocks = map.split("\n")
    pos= blocks.pop(0).split(" ")
    world.player = Player([0,0,0])
    world.player.pos = [float(pos[0]),float(pos[1]),float(pos[2])]
    world.player.spawn = [float(pos[0]),float(pos[1]),float(pos[2])]
    m = len(blocks)
    i = 1
    for block in blocks:
        #print "Parsed ",i,"of",m,"blocks."
        i+=1
        if not block.strip(): continue
        data = block.split(" ")
        try:data= (int(data[0]),int(data[1]),int(data[2]),int(data[3]),int(data[4]))
        except:data= (int(data[0]),int(data[1]),int(data[2]),int(data[3]),0)
        s = data[4]
        #print s
        #print "Wahooy!"
        blocklist[data[0]](data[1:4],world,recompile=False,state=s)
    if recompile: world.recompile()
