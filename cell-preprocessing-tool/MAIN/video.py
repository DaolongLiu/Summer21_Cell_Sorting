#Daniel Karkhut
#Imports
import cv2

#represents video object

import globals
from cell import Cell
from frame import Frame

class Video:

    def __init__(self, camera, backGround, filename):
        #initialize
        self.height = 0
        self.width = 0
        self.center = (self.height/2, self.width/2) 
        self.cells = []
        self.frames = []

        self.camera = cv2.VideoCapture(camera) #was './PC3-20X/Data527.avi' used to pick which video to analyze
        self.backGround = cv2.imread(backGround, 0)
        self.filename= filename
        self.processFrames() #process
        

    def processFrames(self):
        #hello, it begins here!

        self.backGround = cv2.GaussianBlur(self.backGround, (7, 7), 0) # reduces the details a little bit

        while True:
            #########
            ####### Check Frame
            ####
            grabbed, frameArray = self.camera.read()

            if not grabbed:
                break
            ####
            #######
            #########
            currFrame = Frame(frameArray, self.backGround, self.filename) ##current Frame after processing

            currFrame.showFrames()
            
            self.frames.append(currFrame)
            self.cells.append(currFrame.cellInFrame)

    def numFrames(self):
        return len(frames)

    def numCells(self):
        return len(cell)