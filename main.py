from DrawingWindowStandalone import DrawingWindow
from robot import Robot
from obstacle import Obstacle

if __name__ == "__main__":
    window = DrawingWindow(800,400,0,800,0,400,"test")
    robot = Robot(window, 50, 50)
    pts = [(10,0), (10,50), (50, 50), (50, 0)]
    o = Obstacle(robot.getWindow(), pts)
    x = raw_input()