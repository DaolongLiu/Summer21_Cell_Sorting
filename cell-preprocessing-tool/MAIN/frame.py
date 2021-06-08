#Daniel Karkhut
#Imports
import cv2
import numpy as np

#represents frame object

import globals
from cell import Cell

class Frame:

    def __init__(self, frame, background, filename):
        #initializej
        self.OriginalFrame = frame
        self.frame_width= int(self.OriginalFrame.shape[1]*0.7)
        self.frame_hight= int(self.OriginalFrame.shape[0]*0.7)
        self.frame_dim= (self.frame_width, self.frame_hight)
        
        
        
        self.BackgroundFrame = background
        self.GrayFrame = None
        self.ContourFrame = None
        self.filename= filename
        #dimensions
        self.height = np.size(frame, 0)
        self.width = np.size(frame, 1)

        #cell
        self.cellInFrame = None
        
        #adjust
        self.CoorXEntranceLine = 950
        #self.CoorXExitLine = int(round(( self.width /2) + 300)) #begin and end line are offset by 300
        self.CoorXExitLine = 1735
        self.MinContourArea = 500
        self.MaxContourArea = 5006000
        self.BinarizationThreshold = 9

        #method calls
        self.Contours = self.getContours()
        self.processContours() #process contours



    def getContours(self):
        self.GrayFrame = cv2.cvtColor(self.OriginalFrame, cv2.COLOR_BGR2GRAY) #turn black and white
        self.GrayFrame = cv2.GaussianBlur(self.GrayFrame, (7,7), 0) #reduce detail with gaussian blur

        self.ContourFrame = cv2.absdiff(self.GrayFrame, self.BackgroundFrame) #background subtraction
        self.ContourFrame = cv2.threshold(self.ContourFrame, self.BinarizationThreshold, 255, cv2.THRESH_BINARY)[1] #binarization threshold set to 5
        self.ContourFrame = cv2.dilate(self.ContourFrame, None, iterations=8) # when we apply the blur, details get lost. So, the cell detail is getting lost, losing a well-defined contour of the cell so we are padding it (adding pixel value)
        cnts, hierarchy = cv2.findContours(self.ContourFrame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) #find Contours

        #cv2.imshow("Contour frame", self.ContourFrame)

        return cnts

    def processContours(self):
        for c in self.Contours:
            # if a contour has small area, it'll be ignored
            if (cv2.contourArea(c) < self.MinContourArea) or (cv2.contourArea(c) > self.MaxContourArea) or ( len(self.Contours) > 1 ):
                self.cellInFrame = Cell(0, 0, 0, 0, self.filename)

            else:
                #draw a rectangle "around" the object 
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(self.OriginalFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)
 
                self.cellInFrame = Cell(h, w, x, y, self.filename)

                if (x > (self.width/2)) and (globals.MiddleCounter == 0):
                    self.cellInFrame.takeImage(self.OriginalFrame)
                    globals.MiddleCounter = globals.MiddleCounter + 1

                self.CheckEntranceLineCrossing() #updates value

                self.CheckExitLineCrossing() #updates value
    
    def showFrames(self):
        # Write entrance and exit counter values on frame and shows it
        cv2.putText(self.OriginalFrame, "Entrances: {}".format(str(globals.EntranceCounter)), (self.CoorXEntranceLine + 25, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250, 0, 1), 2)
        cv2.putText(self.OriginalFrame, "Exits: {}".format(str(globals.ExitCounter)), (self.CoorXExitLine + 25, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
       
        # plot reference lines
        cv2.line(self.OriginalFrame, (self.CoorXEntranceLine, 0),(self.CoorXEntranceLine, self.height), (255, 0, 0), 2)
        cv2.line(self.OriginalFrame, (self.CoorXExitLine, 0),(self.CoorXExitLine, self.height), (0, 0, 255), 2)
        self.resized = cv2.resize(self.OriginalFrame, self.frame_dim, interpolation = cv2.INTER_AREA)
        cv2.imshow("Original Frame", self.resized)
        
        # WAIT 
        cv2.waitKey(1)

    def CheckEntranceLineCrossing(self):
        Distance = (self.cellInFrame.xCoordCenter - self.CoorXEntranceLine)
        if( (Distance > 0) and (globals.EntranceCounter == 0) ):
            globals.EntranceCounter = globals.EntranceCounter + 1
            self.cellInFrame.takeImage(self.OriginalFrame)
        
    def CheckExitLineCrossing(self):
        Distance = (self.cellInFrame.xCoordCenter - self.CoorXExitLine)
        if( (Distance > 0) and (globals.ExitCounter == 0) ):
            globals.ExitCounter = globals.ExitCounter + 1
            self.cellInFrame.takeImage(self.OriginalFrame)