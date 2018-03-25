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

        self.cone_width = 5 # Radians
        self.obstacle_width = 5 # cm 
        self.new_log_odds = log_odds
        self.x = x
        self.y = y
        

    def update(self, rangefinder_reading, log_odds, x, y):
        #print(rangefinder_reading)
        #print("Log odds: ", log_odds)
        
        # Log odds calculation
        for i in range(0, 127):
            for j in range(0, 127):
                r = math.sqrt( (x**2) + (y**2) )
                theta = math.atan2(y,x)
                if log_odds[i][j] == 0:
                    return 0
                else:
                    self.new_log_odds[i][j] = np.log(log_odds[i][j] / (1. - log_odds[i][j])) 
                    return self.new_log_odds

        
