from DrawingWindowStandalone import DrawingWindow
from robot import Robot
from obstacle import Obstacle
import node

if __name__ == "__main__":
    window = DrawingWindow(800,800,0,800,0,800,"test")
    pts = [(100,210), (150,350), (250, 300)]

    # r = Robot(window, (10,10), pts)
    # pts = [(50, 50), (50, 100), (100,50), (100,100)]
    o = Obstacle(window, pts)

    grid_size = 20
    delta_x = window.windowWidth / grid_size
    delta_y = window.windowHeight / grid_size

    r.setLocation((0,0))

    goal = [15, 15]

    robot.plan = node.search(r.location, goal)

    while r.getLocation() != goal:
        target = robot.plan.pop(0)






