class Robot:
    def __init__(self, window, ref, pts):
        self.ref = ref
        self.points = pts
        self.window = window
        self.body = self.draw()

    def getWindow(self):
        return self.window

    def getRef(self):
        return self.ref

    def __redraw(self):
        x,y = self.ref
        self.window.delete(self.body)
        self.body = self.window.drawRect((x,y),(x + self.length, y+self.length))
        self.window.update()

    def update(self, (x,y)):
        self.ref = (x,y)
        self.__redraw()

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
