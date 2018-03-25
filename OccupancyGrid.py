import pygame
import math
import numpy as np
from RobotLib.Math import *
from cv2 import imread, imwrite
# to install cv2 module: pip install opencv-python

class OccupancyGrid:
    """
    FORMULAS:

    LogOdds( P(a) ) = log( P(a) / P(~a) )
    Probability for each cell P(m) = 1 - 1 / ( 1 + e^(LogOdds(m)) )
    """

    def __init__(self,path,max_dist=80):

        # Initialize log odds to 0
        self.log_odds = np.zeros((128,128))  

        self.max_dist = max_dist

        # read map from image
        self.grid = imread(path,0).astype('float32')/255.
      
        self.height = self.grid.shape[0]
        self.width = self.grid.shape[1]
        
    def draw(self,surface): 
        
        # Probability calculation 
        for i in range(0, 127):
            for j in range(0, 127):
                probability = 1 - ( 1 / ( 1 + np.exp(self.log_odds[i][j]) ) )
                self.grid[i][j] = probability
                #print(probability) # Should be 0.5 to start (map is grey)

        """ Draws the obstacle map onto the surface. """
        # transpose grid and convert to 0-255 range
        omap_array = ((1.-self.grid.transpose())*255.).astype('int')
        
        # replicate across RGB channels
        omap_array = np.tile(np.expand_dims(omap_array,axis=-1),[1,1,3])

        # draw grid on the surface
        pygame.surfarray.blit_array(surface,omap_array)
    
    def get_first_hit(self,T_sonar_map):
        """ Calculates distance that sonar would report given current pose.
            Arguments:
                T_sonar_map: sonar-to-map transformation matrix
            Returns:
                First-hit distance or zero if no hit.
        """
        # iterate over possible range of distances
        for i in range(self.max_dist):
            # get point in sonar reference frame
            pt_sonar = vec(i,0)

            # transform to map reference frame
            pt_map = mul(T_sonar_map,pt_sonar)

            # get integer location in map
            r = int(pt_map[1])
            c = int(pt_map[0])

            # test for location outside map
            if r < 0 or r >= self.grid.shape[0]:
                continue
            if c < 0 or c >= self.grid.shape[1]:
                continue

            # test if cell is occupied
            if self.grid[r,c] > 0:
                # return rangefinder measurement
                return i

        # return 0 for no hit
        return 0.

if __name__ == '__main__':
    # run this script to make an example map

    # create a map
    grid = np.zeros((128,128))

    # border
    grid[:,0] = 1
    grid[:,127] = 1
    grid[0,:] = 1
    grid[127,:] = 1

    log_odds[:,0] = 1
    log_odds[:,127] = 1
    log_odds[0,:] = 1
    log_odds[127,:] = 1
    
    # obstacle
    grid[75:100,75:100] = 1
    
    imwrite('map.png',(grid*255.).astype('uint8'))

