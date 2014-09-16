from DrawingWindowStandalone import DrawingWindow
from robot import Robot
from obstacle import Obstacle
import node

if __name__ == "__main__":
    window = DrawingWindow(800,800,0,800,0,800,"test")
    pts = [(100,210), (150,350), (250, 300)]

    robot = Robot(window, (10,10), pts)
    pts = [(50, 50), (50, 100), (100,50), (100,100)]
    o = Obstacle(window, pts)

    grid_size = 20
    delta_x = window.windowWidth / grid_size
    delta_y = window.windowHeight / grid_size

    r.setLocation((0,0))

    goal = [15, 15]

    robot.plan = node.search(r.location, goal)
    obstacles = [o]

    while robot.getLocation() != goal:
        target = robot.plan.pop(0)

        x, y = target
        x0, y0 = robot.getLocation()
        if x != x0:
            # new is on our left
            if x < x0:
                direction = "left"
            else: direction = "right"
        else:
            if y < y0:
                direction = "down"
            else: direction = "up"

        # converting the grid back to pixel
        targetx = target[0] * delta_x
        targety = target[1] * delta_y

        if direction is "left":
            pointsToCheck = [ (nx, targety) for nx in range(targetx, x0, -1) ]
        elif direction is "right":
            pointsToCheck = [ (nx, targety) for nx in range(x0, targetx) ]
        elif direction is "down":
            pointsToCheck = [ (targetx, ny) for ny in range(y0, targety) ]
        else:
            pointsToCheck = [ (targetx, ny) for ny in range(targety, y0, -1) ]]


        for obs in obstacles:
            # the point is not in a collision space
            if not obs.containsPoint((targetx, targety)):
                # move there
                for point in robot:
                    if obs.containsPoint(point):
                        robot.plan = node.search(robot.getLocation(), goal)
                        BadLocations.addBacLock(target)
                        break

                    # all four points can move there
                    robot.update((targetx, targety))
                    robot.loc = target

                # update internal state
            else:
                # replan
                robot.plan = node.search(robot.getLocation(), goal)
                BadLocations.addBacLock(target)