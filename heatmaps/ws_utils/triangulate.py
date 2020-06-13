from ws_utils import vector2
class triangulator:
    def __init__(self, pt1:vector2, pt2:vector2, pt3:vector2):
        #Define points of triangle, using the vector2 class
        self.pt1 = pt1
        self.pt2 = pt2
        self.pt3 = pt3
    
    def finddists_kp(self, pt:vector2):
        #subtract vectors from eachother, and get the length
        d1 = (self.pt1 - pt).length()
        d2 = (self.pt2 - pt).length()
        d3 = (self.pt3 - pt).length()

        #find the slopes of 2 lines
        if self.pt1.y() - self.pt2.y() == 0:
            r1 = 0
        else:
            r1 = (self.pt1.x() - self.pt2.x()) / (self.pt2.y() - self.pt1.y())
        if self.pt2.y() - self.pt3.y() == 0:
            r2 = 0
        else:
            r2 = (self.pt2.x() - self.pt3.x()) / (self.pt3.y() - self.pt2.y())
        #get intercept for those lines
        s1 = ((d1*d1)+(self.pt2.x()*self.pt2.x())+(self.pt2.y()*self.pt2.y())-(self.pt1.x()*self.pt1.x())-(self.pt1.y()*self.pt1.y())-(d2*d2))/(2*(self.pt2.y()-self.pt1.y()))
        s2 = ((d2*d2)+(self.pt3.x()*self.pt3.x())+(self.pt3.y()*self.pt3.y())-(self.pt2.x()*self.pt2.x())-(self.pt2.y()*self.pt2.y())-(d3*d3))/(2*(self.pt3.y()-self.pt2.y()))
        print(pt.x(), pt.y())
        x = (s2-s1)/(r1-r2)
        y = (r1*x)+s1
        print(x, y)
    
    def finddists(self, d1, d2, d3): #find the slopes of 2 lines
        if self.pt1.y() - self.pt2.y() == 0:
            r1 = 0
        else:
            r1 = (self.pt1.x() - self.pt2.x()) / (self.pt2.y() - self.pt1.y())
        if self.pt2.y() - self.pt3.y() == 0:
            r2 = 0
        else:
            r2 = (self.pt2.x() - self.pt3.x()) / (self.pt3.y() - self.pt2.y())
        #get intercept for those lines
        s1 = ((d1*d1)+(self.pt2.x()*self.pt2.x())+(self.pt2.y()*self.pt2.y())-(self.pt1.x()*self.pt1.x())-(self.pt1.y()*self.pt1.y())-(d2*d2))/(2*(self.pt2.y()-self.pt1.y()))
        s2 = ((d2*d2)+(self.pt3.x()*self.pt3.x())+(self.pt3.y()*self.pt3.y())-(self.pt2.x()*self.pt2.x())-(self.pt2.y()*self.pt2.y())-(d3*d3))/(2*(self.pt3.y()-self.pt2.y()))
        x = (s2-s1)/(r1-r2)
        y = (r1*x)+s1
        print(x, y)