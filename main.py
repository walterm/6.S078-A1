from DrawingWindowStandalone import DrawingWindow
from robot import Robot
from obstacle import Obstacle
import node
import sys

def direction(current, target):
    x, y = target
    x0, y0 = current

    hor, vert = None, None
    # new is on our left
    if x < x0:
        hor =  -1
    elif x > x0: 
        hor = 1
    else:
        hor = 0

    if y < y0:
        vert = -1
    elif y > y0:
        vert = 1
    else:
        vert = 0
    return (hor, vert)

def goalTest(loc, goal):
    return loc[0] == goal[0] and loc[1] == goal[1]

def testCollision(points, obstacles):
    result = []
    for obs in obstacles:
        # were any of the points in an obstacle?
        temp = map(lambda pt: obs.containsPoint(pt), points)
        #if so, then note that
        result.append(True in temp)
    # if there was ever a point in an obstacle, then this is a collision
    return True in result


if __name__ == "__main__":
    window = DrawingWindow(800,800,0,800,0,800,"test")

    grid_size = 50
    delta_x = window.windowWidth / grid_size
    delta_y = window.windowHeight / grid_size
    
    pts = [ (0,0), (0,10), (10,10)]
    robot = Robot(window, (0,0), pts, (delta_x, delta_y))

    pts = [(100,210), (150,350), (250, 300)]
    o = Obstacle(window, pts)

    pts = [ (400, 400), (450, 400), (450, 450)]
    o1 = Obstacle(window, pts)

    goal = [20, 20]

    cells = node.all_points()
    robot.plan = node.search(robot.loc, goal)

    if robot.plan is None:
        print "No plan was found."
        sys.exit()

    obstacles = [o, o1]

    safe = [robot.loc]

    # while it's not at the goal state
    while goalTest(robot.loc, goal) == False:
        target = robot.plan.pop(0)

        

        # make sure that point itself has space
        obsCheck = map(lambda o: o.containsPoint(target), obstacles)
        if True in obsCheck:
            print "was in obstacle, replanning"
            safe.pop()
            x, y = safe.pop()
            robot.translate(x, y)
            robot.plan = node.search(robot.loc, goal)
            node.BadLocations.addBadLoc(target)

            continue

        # make sure every place along that path is possible

        targetx = target[0] * delta_x
        targety = target[1] * delta_y

        currentx = robot.loc[0] * delta_x
        currenty = robot.loc[1] * delta_y

        # we're headed
        _dir = direction(robot.loc, target)
        dx, dy = _dir
        points = []
        for i in range(abs(targetx - currentx)):
            for j in range(abs(targety - currenty)):
                # list of lists
                points += [robot.potentialPoints(dx * i, dy * j)]
        check = map(lambda s: testCollision(s, obstacles), points)

        if True in check:
            print "potential configuration was not safe"
            safe.pop()
            x, y = safe.pop()
            robot.translate(x, y)
            robot.plan = node.search(robot.loc, goal)
            node.BadLocations.addBadLoc(target)
            continue

        # otherwise we're clear
        robot.translate(target[0], target[1])
        safe.append(target)
