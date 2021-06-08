#Daniel Karkhut
#Imports
import cv2

#represents cell object

import globals

class Cell:

    def __init__(self, height, width, x, y, filename):
        #initialize
        self.height = height
        self.width = width
        self.xCoordCenter = (int)((x+x+width)/2)
        self.yCoordCenter = (int)((y+y+height)/2)
        self.imageSize = 50 #change for image size
        self.filename= filename
        self.name_length= len(self.filename)
        self.cropped_filename= self.filename[:self.name_length - 3]
        self.global_number= str(globals.imagesTaken)
        self.string= filename+self.global_number

    def takeImage(self, frame):
        crop = frame[(abs(self.yCoordCenter - self.imageSize)):(abs(self.yCoordCenter + self.imageSize)), (abs(self.xCoordCenter - self.imageSize)):abs((self.xCoordCenter + self.imageSize))]
        cv2.imshow('Image',crop)
        cv2.imwrite('E:/Lehigh/Writings/Conference/CellMe Conference/MAIN 2/MAIN/crops/crop_{}.tif'.format(self.string), crop)
        globals.imagesTaken = globals.imagesTaken + 1 