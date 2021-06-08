#Daniel Karkhut
#Imports
import math
import numpy as np
import scipy.signal
from matplotlib import pyplot as plt
import os

import globals
import cell 
import frame
from video import Video

for filename in sorted(os.listdir("./CELL_FOOTAGE/PC3_Squeezing_Deformation_Channel_Size_7_um")):
    if filename.endswith("avi"):
        #Initialize

        #########
        ####### camera video source and background source 
        ####
        
        cameraSource = ("./CELL_FOOTAGE/PC3_Squeezing_Deformation_Channel_Size_7_um/{}".format(str(filename))) #cv2.VideoCapture('./CELL_FOOTAGE/PC3_Squeezing_Deformation_Channel_Size_7_um/1_6.avi') #was './PC3-20X/Data527.avi' used to pick which video to analyze
        backGroundSource = "./CELL_FOOTAGE/PC3_Squeezing_Deformation_Channel_Size_7_um/1_1_to_1_10_background.png"#cv2.imread('./CELL_FOOTAGE/PC3_Squeezing_Deformation_Channel_Size_7_um/1_1_to_1_10_background.png', 0)

        globals.initialize()
        vid1 = Video(cameraSource, backGroundSource, filename)
        ####
        #######
        #########

        ##calculations

        diff = []

        for x in vid1.cells:
            print(x.xCoordCenter)
            #print(x.yCoordCenter)

        for x in (range(len(vid1.cells))):
            z = abs(int(math.sqrt((vid1.cells[x].yCoordCenter ** 2) + (vid1.cells[x].xCoordCenter ** 2)) - math.sqrt((vid1.cells[x-1].yCoordCenter ** 2) + (vid1.cells[x-1].xCoordCenter ** 2))))
            if (z > 200) and (x > 0):
                diff.append(diff[x-1])
                continue
            elif x == 0:
                diff.append(0)
                continue

            diff.append(z) 

        if(len(diff) <= 51):
            continue

        xhat = scipy.signal.savgol_filter(diff, 51, 3) # window size 51, polynomial order 3

        plt.title("Speed vs Time") 
        plt.xlabel("Time") 
        plt.ylabel("Speed") 
        plt.plot(range(len(vid1.cells)), diff) 
        plt.plot(range(len(vid1.cells)), xhat) 
        plt.show()

        # plt.savefig("E:/Lehigh/Writings/Conference/CellMe Conference/MAIN 2/MAIN/graphs/{}.png".format(str(filename)[:-4]))

        plt.clf()