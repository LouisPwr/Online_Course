# -*- coding: utf-8 -*-
"""
Problem Set 2 of MIT 6002x
"""

import math
import random
import pylab

# Classes to keep track of which parts of the room have been cleaned and direction of each robot

# Position of Robot
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# Initializing the room in which a robot is inserted
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.
        """
        self.width = width
        self.height = height
        self.cleaned_tiles = []
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.
        """
        tile_x = math.floor(pos.getX())
        tile_y = math.floor(pos.getY())
        
        if (tile_x, tile_y) not in self.cleaned_tiles:
            self.cleaned_tiles.append((tile_x, tile_y))
            
        else: 
            pass
        
        
    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.
        """
        if (m, n) in self.cleaned_tiles:
            return  True
        else:
            return False
    
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.
        """
        return self.width*self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.
        """
        return len(self.cleaned_tiles)

    def getRandomPosition(self):
        """
        Return a random position inside the room.
        """
        pos_x = random.random()*self.width
        pos_y = random.random()*self.height
        
        return Position(pos_x, pos_y)

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.
        """
        if 0 <= pos.x < self.width and 0 <= pos.y < self.height:
            return True
        else:
            return False


# Initializing the robot class, which stores the position and direction of a robot.
class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.
        """
        self.room = room
        self.speed = speed
        self.direction = math.floor(random.random()*360)
        self.position = room.getRandomPosition()
        self.room.cleanTileAtPosition(self.position)


    def getRobotPosition(self):
        """
        Return the position of the robot.
        """
        return self.position
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.
        """
        self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.
        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        self.position = self.position.getNewPosition(self.getRobotDirection(), self.speed)
        self.room.cleanTileAtPosition(self.getRobotPosition())



# Initializing StandardRobot Class
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.
        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        old_position = self.position   
        temp = self.position.getNewPosition(self.getRobotDirection(), self.speed)
        
        if self.room.isPositionInRoom(temp) == False:
            self.direction = math.floor(random.random()*360)
        
        else:
            self.position = old_position.getNewPosition(self.getRobotDirection(), self.speed)
            self.room.cleanTileAtPosition(self.getRobotPosition())
        
           


# Initializing class to run a simulation of robots cleaning a room
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    robot_type: class of robot to be instantiated (StandardRobot vs
                RandomWalkRobot)
    """
    TimeStepsList = []
    for trials in range(num_trials):
        TimeSteps = 0
        robots = []
        count = 1
        room = RectangularRoom(width, height)
        
        for robot in range(1, num_robots+1):
            robot = robot_type(room, speed)
            robots.append(robot)
            count += 1
        for named_robot in robots:

            if room.isTileCleaned(named_robot.getRobotPosition().getX(), named_robot.getRobotPosition().getY()) == False:
                room.cleanTileAtPosition(named_robot.getRobotPosition())
        
        while room.getNumCleanedTiles()/room.getNumTiles() <= min_coverage:
            for named_robot in robots:
                named_robot.updatePositionAndClean()
            TimeSteps += 1
            
        TimeStepsList.append(TimeSteps)  
    return sum(TimeStepsList)/len(TimeStepsList)
                
#print(runSimulation(1, 1.0, 10, 10, 0.75, 30, StandardRobot))


# Initializing RandomWalkRobot class
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        self.direction = math.floor(random.random()*360)
        
        old_position = self.position   
        temp = self.position.getNewPosition(self.getRobotDirection(), self.speed)
        
        if self.room.isPositionInRoom(temp) == False:
            self.direction = math.floor(random.random()*360)
            #self.room.cleanTileAtPosition(self.getRobotPosition())
        
        else:
            self.position = old_position.getNewPosition(self.getRobotDirection(), self.speed)
            self.room.cleanTileAtPosition(self.getRobotPosition())


#print(runSimulation(5, 1, 20, 20, 0.5, 1, StandardRobot))



# Plotting simulation results:
def showPlot1(title, x_label, y_label):
    """
    Comparing types of robots and how much time steps they need to clean the whole room
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print("Plotting", num_robots, "robots...")
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

#showPlot1('Cleaning Speed Vs. Number of Robots', 'Num of Robots', 'Time steps needed')
    
def showPlot2(title, x_label, y_label):
    """
    Comparing type of robots and how much the cleaning speed depends on the aspect ratios of the room.
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300//width
        print("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    

#showPlot2('Cleaning Speed VS. Shape of Room', 'Aspect Ratios', 'Time Steps Needed')