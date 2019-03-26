#Banana Ripeness Detection
#Kevin Pirabaharan (0946212), Ena So (), Muhammad Jaffar (911)
#This program creates segments bananas from images and detects brown spots
# on the banana to determine the ripeness of the bananas.
from imageIO import *
from imthr_lib import*
from PIL import Image
# import cv2
import datetime
import glob
import os
import sys

# Loading bar function to show progress of tasks
#
# Parameters:
# (in)    count,total,size     :  progress so far; total tasks to accomplish; size of loading bar pixels
#
def loadingBar(count,total,size):
    percent = float(count)/float(total)*100
    sys.stdout.write("\r" + str(int(count)).rjust(3,'0')+"/"+str(int(total)).rjust(3,'0') + ' [' + '='*int(percent/10)*size + ' '*(10-int(percent/10))*size + ']')

# Function: Image Segmentation
#
# The function takes in an image and aims to segment the banana out, exporting a .png with just the bananaand the background turned to black
#
# Parameters:
# (in)    imagePath, imageName, output :  file path of the image; fileName; datafile to print results of the function
# (out)   bananaSA                     :  Returns the surface area of the banana in pixels
#
def imageSegment(imagePath, imageName, output):
    #start timer for the function
    startDT = datetime.datetime.now()

    #initialize color channels and size variables
    red, green, blue = imread_colour(imagePath)
    redB = np.zeros((width,height))
    greenB = np.zeros((width,height))
    blueB = np.zeros((width,height))
    im = Image.open(imagePath)
    height, width = im.size
    bananaSA = 0

    #find the otsu threshold of the blue channel and then binarized into a black and white image
    #the pixels of the banana should be black (0), whilst the rest of the image should be white (255)
    thr = otsu(blue)
    imgBlueOtsu = im2bw(blue,thr)
    # imwrite_gray("Blue.jpeg", imgBlueOtsu)

    #the Black and White image is looked at pixel by pixel
    #the black pixels of the the image are saved as the color of the original image, whilst the white pixels are turned Black
    #this allows the banana to keep it's color while the rest of the image is blackened
    for i in range(0, width-1):
        for j in range(0, height-1):
            avg = (float(red[i,j]) + float(blue[i,j]) + float(green[i,j])) / 3
            if (imgBlueOtsu[i,j] == 0 and avg <= 127):
                redB[i,j] = red[i,j]
                greenB[i,j] = green[i,j]
                blueB[i,j] = blue[i,j]
                bananaSA += 1
            else:
                redB[i,j] = 0
                greenB[i,j] = 0
                blueB[i,j] = 0

    #image is saved and total time taken, total pixel size are all written to a text file
    imwrite_colour("../images/processed/" + imageName.rsplit('.', 1)[0] + '.png', redB, greenB, blueB)
    endDT = datetime.datetime.now()
    currentDT = endDT - startDT
    output.write(imageName + ": \tTime Taken: " + str(currentDT) + "\t\tBanana Size: " + str(bananaSA) + " pixels\n\n")

    #Returns the surface area of the banana for BrownSpot Analysis
    return bananaSA

# TODO: BrownSpot Analysis


#Program loop to run the program
inputFolder = "../images/raw/"
data = open("../data/segmentationResults.txt", 'w')
fileCount = 0
progExit = False
while (progExit == False):
    inp = raw_input("\n \nExecute Algorithm on a single (F)ile, Run (T)est Suite, (Q)uit? ")
    if (inp == 'f') or (inp == 'F'):
        print("Make sure the image is inside the \'image/raw/\' folder")
        fileName = raw_input("Enter File Name: ")
        bananaSize = imageSegment(inputFolder + fileName, fileName, data)
        print(str(bananaSize))

    elif (inp == 't') or (inp == 'T'):
        print("Testing Algorithms...")
        for file in glob.glob(inputFolder + "*.jpg"):
            fileCount += 1
            print("")
            fname = os.path.basename(file)
            bananaSize = imageSegment(file, fname, data)
            loadingBar(fileCount,len(glob.glob(inputFolder + "*.jpg")),2)
        data.close()

    elif (inp == "q") or (inp == "Q"):
        print("Ending Program...")
        progExit = True

    else:
        print("Please check your input")
