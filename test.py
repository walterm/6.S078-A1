from DrawingWindowStandalone import DrawingWindow

if __name__ == "__main__":
	window = DrawingWindow(800,400,0,800,0,400,"test")
	rect = window.drawRect((0,0),(40,40))
	window.update()
