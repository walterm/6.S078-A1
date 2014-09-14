import math
import lib601.util as util
import lib601.soarWorld as soarWorld
import lib601.plotWindow as plotWindow
from soar.io import io
from mazeAnswers import *

#change this line if the world file is in a different location on your system
PATH_TO_WORLD = '/usr/local/lib/python2.7/dist-packages/soar/worlds/mazeWorld.py'
mazeWorld = [i.strip() for i in open('mazeWorld.txt').readlines()]
global firstPoint
firstPoint = True

class RobotMaze(Maze):
    def __init__(self, mapText, x0, y0, x1, y1):
        self.x0=x0
        self.y0=y0
        self.x1=x1
        self.y1=y1
        self.maze=mapText
        #self.width=len(mapText[0])
        #self.height=len(mapText)
        Maze.__init__(self, mapText)
        self.width_of_each_column=(self.x1-self.x0)/self.width
        self.height_of_each_row=(self.y1-self.y0)/self.height
        
    def pointToIndices(self, point):
        
        r=self.height-int(point.y/self.height_of_each_row)-1
        c=int(point.x/self.width_of_each_column)
        return (r,c)

    def indicesToPoint(self, (r,c)):
        location=(r,c)
        x=location[1]*(self.width_of_each_column)+self.width_of_each_column/2
        y=self.y1-(location[0]*(self.height_of_each_row)+self.height_of_each_row/2)
        return util.Point(x,y)

    def isPassable(self, (r,c)):
        #print (r, c)


        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if not Maze.isPassable(self, (r+i, c+j)):
                    return False
        return True


        
##        up,down,left,right=None,None,None,None
##        if not c>=self.width-1:
##            right=self.maze[r][c+1]
##        if not c<=0:
##            left=self.maze[r][c-1]
##        if not r<=self.height-1:
##            down=self.maze[r+1][c]
##        if not r>=0:
##            up=self.maze[r-1][c]
##        nearby=[up,down,left,right]
##        if down:
##            print nearby
##        if self.maze[r][c]=='#':
##            return False
##        elif self.maze[r][c]=='.' and'#' in nearby:
##            return False
##        return True


# this function is called when the brain is loaded
def setup():
    robot.maze = RobotMaze(mazeWorld,0.,0.,10.,10.)
    robot.path = mazeSearch(robot.maze)
    robot.initialLocation = robot.maze.indicesToPoint(robot.maze.start)
    robot.slimeX = []
    robot.slimeY = []
    # graphical window for path and slimeTrail
    robot.window = plotWindow.PlotWindow()
    #show the soar world #plot the soar world
    soarWorld.plotSoarWorld(PATH_TO_WORLD,robot.window)
    #plot the robot's planned path
    robot.window.plot([robot.maze.indicesToPoint(i).x-robot.initialLocation.x for i in robot.path],
                       [robot.maze.indicesToPoint(i).y-robot.initialLocation.y for i in robot.path],'r',
                       label = 'Intended Path')

# this function is called when the start button is pushed
def brainStart():
    pass

def directionDestination(currentPoint, destinationPoint):
    current=robot.maze.pointToIndices(currentPoint)
    dest=robot.maze.pointToIndices(destinationPoint)
    if current[0]<dest[0]:
        return 'down'
    elif current[0]>dest[0]:
        return 'up'
    elif current[1]<dest[1]:
        return 'right'
    elif current[1]>dest[1]:
        return 'left'
    return None

# this function is called 10 times per second
def step():
    global firstPoint
    inp = io.SensorInput()
    global destinationPoint
    #robot.slimeX.append(inp.odometry.x)
    #robot.slimeY.append(inp.odometry.y)

    currentPoint = inp.odometry.point().add(robot.initialLocation)
    currentAngle = inp.odometry.xytTuple()[2]
    destinationPoint = robot.maze.indicesToPoint(robot.path[0])
    
    if currentPoint.isNear(destinationPoint,.075):
        robot.path = robot.path[1:]
        destinationPoint=robot.maze.indicesToPoint(robot.path[0])

    if directionDestination(currentPoint,destinationPoint)=='down' and not (currentAngle<=((3*math.pi)/2+.05) and currentAngle>=(3*math.pi/2-.05)):
        io.Action(fvel=0,rvel=2.5).execute()
    elif directionDestination(currentPoint,destinationPoint)=='left' and not (currentAngle<=((math.pi)+.05) and currentAngle>=(math.pi-.05)):
        io.Action(fvel=0, rvel=2.5).execute()
    elif directionDestination(currentPoint,destinationPoint)=='right' and not (currentAngle<=(+.05) and currentAngle>=(-.06)):
        io.Action(fvel=0,rvel=2.5).execute()
    elif directionDestination(currentPoint,destinationPoint)=='up' and not (currentAngle<=(math.pi/2+.05) and currentAngle>=(math.pi/2-.05)):
        io.Action(fvel=0,rvel=2.5).execute()

    if directionDestination(currentPoint,destinationPoint)=='down' and  (currentAngle<=((3*math.pi)/2+.05) and currentAngle>=(3*math.pi/2-.05)):
        io.Action(fvel=.5,rvel=0).execute()
    elif directionDestination(currentPoint,destinationPoint)=='left' and  (currentAngle<=((math.pi)+.05) and currentAngle>=(math.pi-.05)):
        io.Action(fvel=.5, rvel=0).execute()
    elif directionDestination(currentPoint,destinationPoint)=='right' and  (currentAngle<=(+.05) and currentAngle>=(-.05)):
        io.Action(fvel=.5,rvel=0).execute()
    elif directionDestination(currentPoint,destinationPoint)=='up' and  (currentAngle<=(math.pi/2+.05) and currentAngle>=(math.pi/2-.05)):
        io.Action(fvel=.5,rvel=0).execute()
    
                                                                            
    #io.Action(fvel=0, rvel=0).execute()



# called when the stop button is pushed
def brainStop():
    try:
        robot.window.plot(robot.slimeX, robot.slimeY,'b',label='Slime Trail') #plot the robot's actual traveled path
    except:
        pass

# called when brain or world is reloaded (before setup)
def shutdown():
    pass
