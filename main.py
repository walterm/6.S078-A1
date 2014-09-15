from DrawingWindowStandalone import DrawingWindow
from robot import Robot
from obstacle import Obstacle

if __name__ == "__main__":
    window = DrawingWindow(800,800,0,800,0,800,"test")
    pts = [(10,10), (10,20), (20, 20), (20, 10)]
    r = Robot(window, (10,10), pts)
    pts = [(50, 50), (50, 100), (100,50), (100,100)]
    o = Obstacle(r.getWindow(), (50,50), pts)

    grid_size = 5
    delta_x = window.windowWidth / grid_size
    delta_y = window.windowHeight / grid_size

