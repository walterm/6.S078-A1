import numpy as np
class Obstacle:
    def __init__(self, window, points):
        self.window = window
        # A list of points, in CW order
        self.points = points
        self.lines = []
        self.centroid = computeCentroid(points)
        self.xmin, self.xmax = findXMinMax(points)
        self.ymin, self.ymax = findYMinMax(points)
        self.normals = self.computeNormals()
        self.draw()

    def computeCentroid(points):
        x = sum(point[0] for point in points) / len(points)
        y = sum(point[1] for point in points) / len(points)
        return np.array([x, y])
        

    def findXMinMax(points):
        sorted_points = sorted(points, key=lambda x: x[0])
        xmin = sorted_points[0][0]
        xmax = sorted_points[-1][0]
        return (xmin, xmax)

    def findYMinMax(points):
        sorted_points = sorted(points, key=lambda x: x[1])
        ymin = sorted_points[0][1]
        ymax = sorted_points[-1][1]
        return (ymin, ymax)

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

    def containsPoint(self, (x,y)):
        # check axis aligned box for the shape
        if x < self.xmin or x > self.xmax or y < self.ymin or y > self.ymax:
            return False

        # now check the normals
        vector = np.array([x,y])
        dotProducts = set(map(self.normals, lambda x: np.dot(x, vector) > 0))
        if len(dotProducts) == 1:
            return dotProducts[0]
        return False
