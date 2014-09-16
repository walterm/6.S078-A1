class Robot:
    def __init__(self, window, ref, pts, deltas):
        self.original = pts
        new_pts = [(pt[0] + ref[0]* deltas[0], pt[1] + ref[1] * deltas[1]) for pt in pts]
        self.points = new_pts
        self.window = window
        self.body = None
        self.draw()
        self.loc = ref
        self.plan = None
        self.deltas = deltas

    def __redraw(self):
        x,y = self.ref
        for elem in self.body:
            self.window.delete(elem)
        self.body = self.draw()

    def update(self, (x,y)):
        delta_x = x - self.ref[0]
        delta_y = y - self.ref[1]
        self.ref = (x,y)
        print self.points
        for i in range(len(self.points)):
            self.points[i] = (self.points[i][0] + delta_x, self.points[i][1] + delta_y )
        print self.points
        self.__redraw()

    def draw(self):
        if self.body != None:
            for elem in self.body:
                self.window.delete(elem)
        lastIndex = len(self.points) - 1
        body = []
        for i in range(len(self.points)):
            if i == lastIndex:
                pt1, pt2 = self.points[i], self.points[0]
            else: pt1, pt2 = self.points[i], self.points[i+1]
            pt1_x, pt1_y = pt1
            pt2_x, pt2_y = pt2
            body.append(self.window.drawPoint(pt1_x, pt1_y))
            body.append(self.window.drawPoint(pt2_x, pt2_y))
            body.append(self.window.drawLineSeg(pt1_x, pt1_y, pt2_x, pt2_y))
        self.window.update()
        self.body = body


    def translate(self, x, y):
        translated = [ (point[0] + x * self.deltas[0], point[1] + y * self.deltas[1]) for point in self.original]
        self.points = translated
        self.loc = (x,y)
        self.draw()
