import processing.core.PVector as PVector
from quaternion import Quaternion
from math import sqrt

class ArcBall(object):
    """
    Class contains ArcBall logic see test_arcball.py for usage
    """
    def __init__(self, cx, cy, radius):
        """
        Initialize instance of ArcBall with no constraint on axis of rotation
        """
        self.center_x = cx
        self.center_y = cy
        self.radius = radius
        self.v_down = PVector()
        self.v_drag = PVector()
        self.q_now = Quaternion()
        self.q_down = Quaternion()
        self.q_drag = Quaternion() 
        self.axisSet = [PVector(1.0, 0.0, 0.0), PVector(0.0, 1.0, 0.0), PVector(0.0, 0.0, 1.0)]
        self.axis = -1  
        
    def selectAxis(self,  axis):
        """
        call this from sketch (typically in keyPressed() to constrain rotation to one axis)
        valid input 0, 1, 2 or -1
        """
        self.axis = axis
        
    def __mouse2sphere(self, x, y):
        """
        private map mouse to ArcBall (sphere)
        """
        v = PVector()
        v.x = (x - self.center_x) / self.radius
        v.y = (y - self.center_y) / self.radius
        mag = v.x * v.x + v.y * v.y
        if (mag > 1.0) :
            v.normalize()
        else:
            v.z = sqrt(1.0 - mag)
        return  v  if (self.axis == -1) else (self.__constrain(v, self.axisSet[self.axis]))
    
    def mousePressed(self, x, y):
        """
        pass in mouse.x and mouse.y parameters from sketch
        """
        self.v_down = self.__mouse2sphere(x, y)
        self.q_down.copy(self.q_now)
        self.q_drag.reset()

    def mouseDragged(self, x, y):
        """
        pass in mouse.x and mouse.y parameters from sketch
        """
        self.v_drag = self.__mouse2sphere(x, y)
        self.q_drag.set(PVector.dot(self.v_down, self.v_drag), self.v_down.cross(self.v_drag))
        
    def __constrain(self, vector, axis):
        """
        private constrain (used to constrain axis)
        """
        res = PVector.sub(vector, PVector.mult(axis, PVector.dot(axis, vector)))
        res.normalize()
        return res
        
    def update(self):
        """
        Call this function in the sketch draw loop to get rotation matrix as an array 
        """
        self.q_now = Quaternion.mult(self.q_drag, self.q_down)
        return self.__quat2matrix(self.q_now)

    def __quat2matrix(self,  q) :
        """
        private return matrix as array
        """
        rot = q.getValue()
        return rot