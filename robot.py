class Robot:
	def __init__(self, window, x, y, length=30):
		self.ref = (x, y)
		self.length = length
		self.window = window
		self.body = self.window.drawRect((x,y),(x+length, y+length))

		self.window.update()
		self.currentLoc = [x,y]

	def getWindow(self):
		return self.window

	def __redraw(self):
		x,y = self.ref
		self.window.delete(self.body)
		self.body = self.window.drawRect((x,y),(x + self.length, y+self.length))
		self.window.update()

	def update(self, (x,y)):
		self.ref = (x,y)
		self.__redraw()
