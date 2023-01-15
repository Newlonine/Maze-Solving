from controller import Motor, Supervisor
from math import pi

wheel_raduis = 0.0205

wheel_dist = ((2 * pi * wheel_raduis) / 0.129) / 6.28
    
class rb_ctrl:
    def __init__(self,supervisor,epuck):
        self.supervisor = supervisor
        self.epuck = epuck
        self.lmotor = self.supervisor.getDevice("left wheel motor")
        self.lmotor.setPosition(float('inf'))
        self.lmotor.setVelocity(0)
        self.lsensor = self.supervisor.getDevice("left wheel sensor")
        self.lsensor.enable(1)

        self.rmotor = self.supervisor.getDevice("right wheel motor")
        self.rmotor.setPosition(float('inf'))
        self.rmotor.setVelocity(0)
        self.rsensor = self.supervisor.getDevice("right wheel sensor")
        self.rsensor.enable(1)
        
        self.roule = False
        
    def get_roule(self):
        return self.roule
        
    def haut(self):
        self.epuck.getField("rotation").setSFRotation([0.0, 0.0, 1.0, pi])
        self.epuck.getField("translation").setSFVec3f([self.epuck.getField("translation").getSFVec3f()[0]-0.125, self.epuck.getField("translation").getSFVec3f()[1], self.epuck.getField("translation").getSFVec3f()[2]])
        
    def bas(self):
        self.epuck.getField("rotation").setSFRotation([0.0, 0.0, 1.0, 0])
        self.epuck.getField("translation").setSFVec3f([self.epuck.getField("translation").getSFVec3f()[0]+0.125, self.epuck.getField("translation").getSFVec3f()[1], self.epuck.getField("translation").getSFVec3f()[2]])
        
    def gauche(self):
        self.epuck.getField("rotation").setSFRotation([0.0, 0.0, 1.0, (-pi)/2])
        self.epuck.getField("translation").setSFVec3f([self.epuck.getField("translation").getSFVec3f()[0], self.epuck.getField("translation").getSFVec3f()[1]-0.125, self.epuck.getField("translation").getSFVec3f()[2]])
        
    def droite(self):
        self.epuck.getField("rotation").setSFRotation([0.0, 0.0, 1.0, pi/2])
        self.epuck.getField("translation").setSFVec3f([self.epuck.getField("translation").getSFVec3f()[0], self.epuck.getField("translation").getSFVec3f()[1]+0.125, self.epuck.getField("translation").getSFVec3f()[2]])
        
    def restart(self, x, y):
        self.epuck.getField("rotation").setSFRotation([0.0, 0.0, 1.0, 0.0])
        self.epuck.getField("translation").setSFVec3f([x*0.125, y*0.125, 0.005])