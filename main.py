from DrawingWindowStandalone import DrawingWindow
from robot import Robot
from obstacle import Obstacle

if __name__ == "__main__":
	window = DrawingWindow(800,400,0,800,0,400,"test")
	r = Robot(window, 0, 0)
	