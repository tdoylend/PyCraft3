class TechnoFloor(BasicBlock):
    coords_top=[RATE*0,RATE*1,RATE*1,RATE*0]
    coords_btm=[RATE*0,RATE*1,RATE*1,RATE*0]
    coords_lft=[RATE*0,RATE*1,RATE*1,RATE*0]
    coords_rgt=[RATE*0,RATE*1,RATE*1,RATE*0]
    coords_fwd=[RATE*0,RATE*1,RATE*1,RATE*0]
    coords_bck=[RATE*0,RATE*1,RATE*1,RATE*0]

class BloodPuddle(TechnoFloor):
    coords_top=[RATE*1,RATE*1,RATE*2,RATE*0]
    
class TechnoWall(BasicBlock):
    coords_top=[RATE*4,RATE*1,RATE*5,RATE*0]
    coords_btm=[RATE*4,RATE*1,RATE*5,RATE*0]
    coords_lft=[RATE*4,RATE*1,RATE*5,RATE*0]
    coords_rgt=[RATE*4,RATE*1,RATE*5,RATE*0]
    coords_fwd=[RATE*4,RATE*1,RATE*5,RATE*0]
    coords_bck=[RATE*4,RATE*1,RATE*5,RATE*0]

FLOOR_CHOICE = [BloodPuddle] + [TechnoFloor]*7 