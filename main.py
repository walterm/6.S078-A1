from DrawingWindowStandalone import DrawingWindow
from robot import Robot
from obstacle import Obstacle
import node

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

    goal = [30, 20]

    robot.plan = node.search(robot.loc, goal)

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

        print "new location", robot.loc
        print "path remaining", robot.plan
        raw_input()


    # for i in range(len(robot.plan)):
    #     replanning = False
    #     target = robot.plan[i]
    #     if goalTest(target, robot.loc):
    #         continue
    #     targetx, targety = target
    #     targetx *= delta_x
    #     targety *= delta_y

    #     _dir = direction(robot.loc, target)
    #     print _dir, i, robot.plan[i]
    #     if _dir is "left":
    #         pixel_delta = abs(targetx - robot.loc[0] * delta_x)
    #         sets_of_points = [robot.translate( (-1 * x, 0)) for x in range(1, pixel_delta) ]
    #         if testCollision(sets_of_points, obstacles):
    #             print "could't move left"
    #             # cut off the plan up until the bad state
    #             node.BadLocations.addBadLoc(robot.plan[i])
    #             robot.plan = robot.plan[:i]
    #             #replan
    #             robot.plan += node.search(robot.plan[-1], goal)
                
    #             replanning = True


                        
    #     elif _dir is "right":
    #         pixel_delta = abs(targetx - robot.loc[0] * delta_x)
    #         sets_of_points = [robot.translate( (x, 0)) for x in range(1, pixel_delta) ]
    #         if testCollision(sets_of_points, obstacles):
    #             print "could't move right"
    #             node.BadLocations.addBadLoc(target)
    #             robot.plan = robot.plan[:i]
    #             robot.loc = robot.plan[-1]
    #             robot.update( (robot.plan[-1][0] * delta_x, robot.plan[-1][1] * delta_y) )
    #             #replan
    #             robot.plan += node.search(robot.plan[-1], goal)
    #             replanning = True
                        

                    
    #     elif _dir is "up":
    #         pixel_delta = abs(targety - robot.loc[1] * delta_y)
    #         sets_of_points = [robot.translate( (0, y)) for y in range(1, pixel_delta) ]
    #         if testCollision(sets_of_points, obstacles):
    #             print "could't move up"
    #             # cut off the plan up until the bad state
    #             node.BadLocations.addBadLoc(target)
    #             print robot.plan[i], "bad state"
    #             robot.plan = robot.plan[:i]
    #             robot.loc = robot.plan[-1]
    #             print robot.loc, "backed into"
    #             print "ref", robot.ref
    #             robot.update( (robot.plan[-1][0] * delta_x, robot.plan[-1][1] * delta_y) )
    #             print "after updating", robot.ref
    #             #replan
    #             robot.plan += node.search(robot.plan[-1], goal)
    #             replanning = True
    #     else:
    #         pixel_delta = abs(targety - robot.loc[1] * delta_y)
    #         sets_of_points = [robot.translate( (0, -1 * y)) for y in range(1, pixel_delta) ]
    #         if testCollision(sets_of_points, obstacles):
    #             print "could't move down"
    #             # cut off the plan up until the bad state
    #             robot.plan = robot.plan[:i]
    #             #replan
    #             robot.plan += node.search(robot.plan[-1], goal)
    #             replanning = True

    #     if not replanning:
    #         robot.update((targetx, targety))
    #         robot.loc = target

    #     raw_input()

        # print target

        # x, y = target
        # x0, y0 = robot.getLocation()
        # if x != x0:
        #     # new is on our left
        #     if x < x0:
        #         direction = "left"
        #     else: direction = "right"
        # else:
        #     if y < y0:
        #         direction = "down"
        #     else: direction = "up"

        # # converting the grid back to pixel
        # targetx = target[0] * delta_x
        # targety = target[1] * delta_y

        # if direction is "left":
        #     pointsToCheck = [ (nx, targety) for nx in range(targetx, x0, -1) ]
        # elif direction is "right":
        #     pointsToCheck = [ (nx, targety) for nx in range(x0, targetx) ]
        # elif direction is "down":
        #     pointsToCheck = [ (targetx, ny) for ny in range(y0, targety) ]
        # else:
        #     pointsToCheck = [ (targetx, ny) for ny in range(targety, y0, -1) ]

        # prevPoint = None
        # for obs in obstacles:
        #     # the point is not in a collision space
        #     if not obs.containsPoint((targetx, targety)):
        #         # move there
        #         canMove = []
        #         for pt in robot.points:
        #             canMove.append(not obs.containsPoint(pt))

        #         if False in canMove:
        #             print "failed target", target
        #             print "replanning"
        #             robot.loc = prevPoint
        #             robot.update(prevPoint)
        #             node.BadLocations.addBadLoc(robot.loc)
        #             node.BadLocations.addBadLoc(target)
        #             robot.plan = node.search(robot.loc, goal)
        #             test = raw_input()
                    
        #     else:
        #         # all four points can move there
        #         robot.update((targetx, targety))
        #         robot.loc = target
        #         prevPoint = target
        #         print "prevPoint", prevPoint

        #         print "robot is now at", robot.loc

        #         # update internal state
        #     else:
        #         # replan
        #         robot.plan = node.search(robot.getLocation(), goal)
        #         BadLocations.addBacLock(target)