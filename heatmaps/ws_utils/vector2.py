import math

class vector2:
    def __init__(self, x, y):
        self.e = [x, y]

    def length(self):
        return math.sqrt((self.e[0] * self.e[0]) + (self.e[1] * self.e[1]))

    def length_squared(self):
        return (self.e[0] * self.e[0]) + (self.e[1] * self.e[1])
    
    def __neg__(self):
        return vector2(-self.e[0], -self.e[1])

    def __add__(self, other):
        x = self.e[0] + other.e[0]
        y = self.e[1] + other.e[1]
        return vector2(x, y)
    
    def __sub__(self, other):
        x = self.e[0] - other.e[0]
        y = self.e[1] - other.e[1]
        return vector2(x, y)
    
    def __mul__(self, other):
        if isinstance(other, vector2):
            x = self.e[0] * other.e[0]
            y = self.e[1] * other.e[1]
        else:
            x = self.e[0] * other
            y = self.e[1] * other
        return vector2(x, y)

    def __truediv__(self, other):
        if isinstance(other, vector2):
            x = self.e[0] / other.e[0]
            y = self.e[1] / other.e[1]
        else:
            x = self.e[0] / other
            y = self.e[1] / other
        return vector2(x, y)
    
    def x(self):
        return self.e[0]
    
    def y(self):
        return self.e[1]
    
    def get(self, i):
        return self.e[i]
    
point2 = vector2