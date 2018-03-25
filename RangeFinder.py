import pygame
import math
import numpy as np
from RobotLib.Math import *
from cv2 import imread, imwrite
# to install cv2 module: pip install opencv-python

class RangeFinder:
    """
    FORMULAS:

    LogOdds( P(a) ) = log( P(a) / P(~a) )
    Probability for each cell P(m) = 1 - 1 / ( 1 + e^(LogOdds(m)) )
    """

    def __init__(self,rangefinder_reading, log_odds, x, y):

        # alpha = width of rangefinder's cone in radians
        self.cone_width = .785 # Radians

        # beta = width of the region before and after the measured distance to be considered occupied
        self.obstacle_width = 5 # cm 
        
        #self.new_log_odds = np.zeros((128,128))
        self.new_log_odds = log_odds

        # x and y of sonar's center in map frame
        self.x = x
        self.y = y
        

    def update(self, rangefinder_reading, log_odds, x, y):  # Function called from mapping.py in draw()      
        #print(rangefinder_reading)
        #print(log_odds)
        
        a = self.cone_width
        b = self.obstacle_width
        z = rangefinder_reading

        # Log odds calculation
        for i in range(0, 127):
            for j in range(0, 127):

                r = math.sqrt( (x**2) + (y**2) )
                theta = math.atan2(y,x)

                if -b/2 <= theta <= b/2 and z - a/2 <= r <= z + a/2:  #log odds = occluded
                    self.new_log_odds[i][j] = log_odds[i][j] + 5
                    #return self.new_log_odds[i][j]

                elif -b/2 <= theta <= b/2 and 0 <= r < z - a/2:  #log odds = free
                    self.new_log_odds[i][j] = log_odds[i][j] - 5
                    #return log_odds

                #else:  #log odds = L_0  not needed 
                    #return log_odds


        return self.new_log_odds
