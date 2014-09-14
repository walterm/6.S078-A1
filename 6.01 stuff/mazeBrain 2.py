import maze
reload(maze)
import search
reload(search)
import lib601.util as util
import lib601.sonarDist as sonarDist
import time
import math
from soar.io import io
import soar.outputs.simulator as sim
import random
from maze import DynamicRobotMaze
###### SETUP

NOISE_ON = True

bigFrustrationWorld = [0.2, util.Point(7.0, 1.0), (-0.5, 8.5, -0.5, 8.5)]
frustrationWorld = [0.15, util.Point(3.5, 0.5), (-0.5, 5.5, -0.5, 5.5)]
raceWorld = [0.18, util.Point(2.0, 5.5), (-0.5, 5.5, -0.5, 8.5)]
bigPlanWorld = [0.25, util.Point(3.0, 1.0), (-0.5, 10.5, -0.5, 10.5)]
                                                                 
THE_WORLD = bigFrustrationWorld
(gridSquareSize, goalPoint, (xMin, xMax, yMin, yMax)) = THE_WORLD

###### SOAR CONTROL
# this function is called when the brain is (re)loaded 
def setup():
    #initialize robot's internal map
    width = int((xMax-xMin)/gridSquareSize)
    height = int((yMax-yMin)/gridSquareSize)
    robot.map = maze.DynamicRobotMaze(height,width,xMin,yMin,xMax,yMax)
    robot.map.redrawWorld()
    robot.map.update()
    sim.SONAR_VARIANCE = (lambda mean: 0.001) if NOISE_ON else (lambda mean: 0) #sonars are accurate to about 1 mm
    robot.plan = None

# this function is called when the start button is pushed
def brainStart():
    robot.count = 0
    robot.startTime = time.time()

# this function is called 10 times per second
def step():
    robot.count += 1
    inp = io.SensorInput(cheat=True)
    for c in ('orange','cyan','blue','red'):
        robot.map.clearColor(c)

    # discretize sonar readings
    # each element in discreteSonars is a tuple (d, cells)
    # d is the distance measured by the sonar
    # cells is a list of grid cells (r,c) between the sonar and the point d meters away
    discreteSonars = []
    for (sonarPose,d) in zip(sonarDist.sonarPoses,inp.sonars):
        if NOISE_ON:
            r = random.random()
            if d != 5:
                if r > .99:
                    d = 5
                elif r > .97:
                    d = random.uniform(gridSquareSize,d)
            else:
                if r > .98:
                    d = random.uniform(gridSquareSize,1.5)
        discreteSonars.append((d,util.lineIndices(robot.map.pointToIndices(inp.odometry.transformPose(sonarPose)), robot.map.pointToIndices(sonarDist.sonarHit(d, sonarPose, inp.odometry)))))
    
    # update map
    for (d,cells) in discreteSonars:
        if d != 5:
            robot.map.set(cells[-1])
            for index in range(0, len(cells)-1):
                robot.map.clear(cells[index])
        

    # if necessary, make new plan
    if robot.plan is None or not all(robot.map.isPassable(i) for i in robot.plan):
        print 'REPLANNING'
        robot.plan = search.ucSearch(search.MazeSearchNode(robot.map,
                              robot.map.pointToIndices(inp.odometry.point()),None,0), 
                              lambda x: x == robot.map.pointToIndices(goalPoint), 
                              lambda x: 0)
        

    # graphics (draw robot's plan, robot's location, goalPoint)
    robot.map.markCells(robot.plan,'blue')
    robot.map.markCell(robot.map.pointToIndices(inp.odometry.point()),'red')
    robot.map.markCell(robot.map.pointToIndices(goalPoint),'green')

    # move to target point (similar to driving task in DL2)
    currentPoint = inp.odometry.point()
    currentAngle = inp.odometry.theta
    destinationPoint = robot.map.indicesToPoint(robot.plan[0])
    while currentPoint.isNear(destinationPoint,0.1) and len(robot.plan)>1:
        robot.plan.pop(0)
        destinationPoint = robot.map.indicesToPoint(robot.plan[0])

    if not currentPoint.isNear(destinationPoint,0.1):
        angle = util.fixAnglePlusMinusPi(currentPoint.angleTo(destinationPoint)-currentAngle)
        if abs(angle)<0.1:
            #if close enough to pointing, use proportional control on forward velocity
            fv = 2*currentPoint.distance(destinationPoint)
            rv = 0
        else:
            #otherwise, use proportional control on angular velocity
            fv = 0
            rv = 2*angle
    else:
        raise Exception, 'Goal Reached!'

    robot.map.update()
    io.Action(fvel=fv,rvel=rv).execute()

# called when the stop button is pushed
def brainStop():
    stopTime = time.time()
    print 'Total steps:', robot.count
    print 'Elapsed time in seconds:', stopTime - robot.startTime
