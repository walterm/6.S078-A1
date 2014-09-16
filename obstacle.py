import numpy as np
from math import atan2
import sys
class Obstacle:
    def __init__(self, window, points):
        self.window = window
        # A list of points, in CW order
        self.points = points
        self.lines = []
        self.centroid = self.computeCentroid(points)
        self.xmin, self.xmax = self.findXMinMax(points)
        self.ymin, self.ymax = self.findYMinMax(points)
        self.normals = self.computeNormals()
        self.draw()

    def computeCentroid(self, points):
        x = sum(point[0] for point in points) / len(points)
        y = sum(point[1] for point in points) / len(points)
        return np.array([x, y])
        

    def findXMinMax(self, points):
        sorted_points = sorted(points, key=lambda x: x[0])
        xmin = sorted_points[0][0]
        xmax = sorted_points[-1][0]
        return (xmin, xmax)

    def findYMinMax(self, points):
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
        x, y = self.centroid
        #Sorting points in CCW order
        self.points = sorted(self.points, key=lambda pt: atan2( (pt[1] - y), (pt[0] - x) ) )
        for i in range(len(self.points)):
            if i == lastIndex:
                pt1, pt2 = self.points[0], self.points[i]
            else: pt1, pt2 = self.points[i], self.points[i+1]
            # pt1_x, pt1_y = pt1
            # pt2_x, pt2_y = pt2

            # vector = np.array([ pt2_x - pt1_x, pt2_y - pt1_y])
            # # the normal of a vector is [-b, a]
            # if vector[1] != 0:
            #     normal = np.array([ -vector[1], vector[0] ])
            # # axis case
            # else: normal = np.array([vector[1], -vector[0]])
            # normals.append(normal)

            normals.append([pt1, pt2])
        return normals

    def __raycasting(self, point, edge):
        _eps = 0.00001
        _inf = sys.float_info.max
        _small = sys.float_info.min

        pt1, pt2 = edge

        if pt1[1] > pt2[1]:
            pt1, pt2 = pt2, pt1

        x,y = point

        if x < self.xmin or x > self.xmax or y < self.ymin or y > self.ymax:
            return False

        if x < min(pt1[0], pt2[0]):
            return True

        if point[1] == pt1[1] or point[1] == pt2[1]:
            point = [point[0], point[1] + _eps]

        if abs(pt1[0] - pt2[0]) > _small:
            first_slope = (pt2[1] - pt1[1]) / float(pt2[0] - pt1[0])
        else: first_slope = _inf

        if abs(pt1[0] - point[0]) > _small:
            second_slope = (point[1] - pt1[1]) / float(point[0] - pt1[0])
        else: second_slope = _inf

        return second_slope >= first_slope

    def __isOdd(self, x):
        return x % 2 == 1

    def containsPoint(self, point):

        # triangle case
        if len(self.normals) == 3:
            def sign(p1, p2, p3):
                return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

            test1 = sign(point, self.points[0], self.points[1]) < 0.
            test2 = sign(point, self.points[1], self.points[2]) < 0.
            test3 = sign(point, self.points[2], self.points[0]) < 0.
            return test1 == test2 and test2 == test3
        return self.__isOdd(sum(self.__raycasting(point, edge) for edge in self.normals))


    # def containsPoint(self, (x,y)):
    #     # check axis aligned box for the shape
    #     if x < self.xmin or x > self.xmax or y < self.ymin or y > self.ymax:
    #         return False

    #     # now check the normals
    #     vector = np.array([x,y])
    #     print "vector", vector
    #     for normal in self.normals:
    #         offset = np.dot(normal, self.points[0])
    #         print "normal", normal
    #         print np.dot(normal, vector) - offset
    #         if np.dot(normal, vector) - offset < 0:
    #             return True
    #     return False
