import numpy as np
class Obstacle:
    def __init__(self, window, points):
        self.window = window
        # A list of points, in CW order
        self.points = points
        self.lines = []
        self.normals = self.computeNormals()
        self.draw()

    def draw(self):
        lastIndex = len(self.points) - 1
        for i in range(len(self.points)):
            if i == lastIndex:
                pt1, pt2 = self.points[i], self.points[0]
            else: pt1, pt2 = self.points[i], self.points[i+1]
            pt1_x, pt1_y = pt1
            pt2_x, pt2_y = pt2
            self.window.drawPoint(pt1_x, pt1_y)
            self.window.drawPoint(pt2_x, pt2_y)
            self.window.drawLineSeg(pt1_x, pt1_y, pt2_x, pt2_y)
            self.window.update()

    def computeNormals(self):
        normals = []
        lastIndex = len(self.points) - 1
        for i in range(len(self.points)):
            if i == lastIndex:
                pt1, pt2 = self.points[i], self.points[0]
            else: pt1, pt2 = self.points[i], self.points[i+1]
            pt1_x, pt1_y = pt1
            pt2_x, pt2_y = pt2

            vector = np.array([ (pt2_x - pt1_x) / 2, (pt2_y - pt1_y) / 2])
            # the normal of a vector is [-b, a]
            normal = np.array([ -vector[1], vector[0] ])
            normals.append(normal)
        return normals