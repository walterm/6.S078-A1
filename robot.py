class Robot:
    def __init__(self, window, ref, pts, deltas, multi=False):
        self.original = pts
        new_pts = [(pt[0] + ref[0]* deltas[0], pt[1] + ref[1] * deltas[1]) for pt in pts]
        self.points = new_pts
        self.window = window
        self.body = None
        self.multi=multi
        self.tri = False
        self.loc = ref
        self.deltas = deltas
        self.draw()
        
        self.plan = None
        

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
        if self.multi and not self.tri:
            tri = [(0,21), (35, 35), (35,21)]
            map(lambda x: self.original.append(x), tri)
            self.points += map(lambda pt: (pt[0] + self.loc[0]* self.deltas[0], pt[1] + self.loc[1] * self.deltas[1]), tri )
            lastIndex = len(tri) - 1
            for i in range(len(tri)):
                if i == lastIndex:
                    pt1, pt2 = tri[i], tri[0]
                else: pt1, pt2 = tri[i], tri[i+1]
                pt1_x, pt1_y = pt1
                pt2_x, pt2_y = pt2
                body.append(self.window.drawPoint(pt1_x, pt1_y))
                body.append(self.window.drawPoint(pt2_x, pt2_y))
                body.append(self.window.drawLineSeg(pt1_x, pt1_y, pt2_x, pt2_y))
            self.tri = True


        self.window.update()
        self.body = body

    def translate(self, x, y):
        translated = [ (point[0] + x * self.deltas[0], point[1] + y * self.deltas[1]) for point in self.original]
        self.points = translated
        self.loc = (x,y)
        self.draw()

    def potentialPoints(self, x, y):
        translated = [ (point[0] + x, point[1] + y) for point in self.points]
        return translated