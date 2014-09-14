from DrawingWindowStandalone import DrawingWindow

if __name__ == "__main__":
	window = DrawingWindow(800,400,0,800,0,400,"test")
	window.drawLineSeg(0,0,50,50)
	window.update()
	x = raw_input()
