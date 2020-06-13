import math
from ws_utils.wmath import mapRange

class vector3:
    #make vector 3 instance
    def __init__(self, e0, e1, e2):
        self.e = [e0, e1, e2]
    
    #get x component from vector
    def x(self):
        return self.e[0]
    
    #get y component from vector
    def y(self):
        return self.e[1]

    #get z component from vector
    def z(self):
        return self.e[2]
    
    #handle negative in front of vector
    def __neg__(self):
        return vector3(-self.e[0], -self.e[1], -self.e[2])
    
    #get component by index as in array[i]
    def get(self, i):
        return self.e[i]
    
    #handle vector additions
    def __add__(self, other):
        return vector3(self.e[0] + other.e[0], self.e[1] + other.e[1], self.e[2] + other.e[2])
    
    #hanlde vector subtractions
    def __sub__(self, other):
        return vector3(self.e[0] - other.e[0], self.e[1] - other.e[1], self.e[2] - other.e[2])
    
    #handle vector multiplication
    def __mul__(self, other):
        #vector * vector
        if isinstance(other, vector3):
            return vector3(self.e[0] * other.e[0], self.e[1] * other.e[1], self.e[2] * other.e[2])
        #vector * float
        else:
            return vector3(self.e[0] * other, self.e[1] * other, self.e[2] * other)
    #handle vector division
    def __truediv__(self, other):
        #vector / vector
        if isinstance(other, vector3):
            return vector3(self.e[0]/other.e[0], self.e[1]/other.e[1], self.e[2]/other.e[2])
        #vector / float
        else:
            return vector3(self.e[0]/other, self.e[1]/other, self.e[2]/other)
    
    #get length of vector
    def length(self):
        return math.sqrt((self.e[0]*self.e[0]) + (self.e[1] * self.e[1]) + (self.e[2] * self.e[2]))

    #get length squared of vector
    def length_squared(self):
        return (self.e[0]*self.e[0]) + (self.e[1] * self.e[1]) + (self.e[2] * self.e[2])


point3 = vector3 #3d point
color = vector3 #rgb color

def dot(u:vector3, v:vector3):
    return (u.e[0] * v.e[0]) + (u.e[1] * v.e[1]) + (u.e[2] * v.e[2])

def cross(u:vector3, v:vector3):
    return vector3(
        (u.e[0] * v.e[2]) - (u.e[2] * v.e[1]),
        (u.e[2] * v.e[0]) - (u.e[0] * v.e[2]),
        (u.e[0] * v.e[1]) - (u.e[1] * v.e[0])
    )

def unit_vector(v:vector3):
    return v/v.length()

def get_color(pixel_color:color):
    r = mapRange(pixel_color.x(), 0, 1, 0, 255)
    g = mapRange(pixel_color.y(), 0, 1, 0, 255)
    b = mapRange(pixel_color.z(), 0, 1, 0, 255)
    return (int(r), int(g), int(b))