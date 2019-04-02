#Banana Ripeness Detection
#Kevin Pirabaharan (0946212), Ena So (), Muhammad Jaffar (911)
#This program creates segments bananas from images and detects brown spots
# on the banana to determine the ripeness of the bananas.
from imageIO import *
from imthr_lib import*
from PIL import Image
import cv2
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
    im = Image.open(imagePath)
    height, width = im.size
    img = cv2.imread(imagePath)
    HSV = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    cv2.imwrite('hsv.jpg',HSV)
    red, green, blue = imread_colour('hsv.jpg')
    redB = np.zeros((width,height))
    greenB = np.zeros((width,height))
    blueB = np.zeros((width,height))
    bananaSA = 0

    #find the otsu threshold of the red channel and then binarized LAB image into a black and white image
    #the pixels of the banana should be white (255), whilst the rest of the image should be white (0)
    thr = otsu(red)
    imgRedOtsu = im2bw(red,thr)
    imwrite_gray("Red2.jpeg", imgRedOtsu)

    red, green, blue = imread_colour(imagePath)

    #the Black and White image is looked at pixel by pixel
    #the white pixels of the the image are saved as the color of the original image, whilst the rest of the image is saved as black pixels
    #this allows the banana to keep it's color while the rest of the image is blackenes
    for i in range(0, width-1):
        for j in range(0, height-1):
            avg = (float(red[i,j]) + float(blue[i,j]) + float(green[i,j])) / 3
            if (imgRedOtsu[i,j] == 255):
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


    # for i in range(0, HSV.shape[0]):
    #     for j in range(0, HSV.shape[1]):
    #         HSV[i,j][0] = HSV[i,j][0]*1.4
    #         HSV[i,j][1] = HSV[i,j][0]/2.55
    #         HSV[i,j][2] = HSV[i,j][0]/2.55
    #
    # im4 = cv2.imread(imagePath)
    #
    # for i in range(0, HSV.shape[0]):
    #     for j in range(0, HSV.shape[1]):
    #         sum = float(HSV[i,j][0]) + float(HSV[i,j][1]) + float(HSV[i,j][2])
    #         if (sum != 0):
    #             if (sum > 90):
    #                 # print("hi")
    #                 HSV[i,j][0] = 0
    #                 HSV[i,j][1] = 0
    #                 HSV[i,j][2] = 0
    #             else:
    #                 HSV[i,j][0] = im4[i,j][0]
    #                 HSV[i,j][1] = im4[i,j][1]
    #                 HSV[i,j][2] = im4[i,j][2]
    #
    # cv2.imwrite("../images/processed/rgbConvert.png", HSV)
    #
    # redC, greenC, blueC = imread_colour("../images/processed/rgbConvert.png")
    # thr = otsu(blueC)
    # imgBlueCOtsu = im2bw(blueC,thr)
    # imwrite_gray("Blue3.jpeg", imgBlueCOtsu)


# TODO: BrownSpot Analysis


#Program loop to run the program
inputFolder = "../images/raw/"
data2 = open("../data/testing.txt", 'w')
fileCount = 0
progExit = False
while (progExit == False):
    inp = raw_input("\n \nExecute Algorithm on a single (F)ile, Run (T)est Suite, (Q)uit? ")
    if (inp == 'f') or (inp == 'F'):
        print("Make sure the image is inside the \'image/raw/\' folder")
        fileName = raw_input("Enter File Name: ")
        bananaSize = imageSegment(inputFolder + fileName, fileName, data2)
        print(str(bananaSize))

    elif (inp == 't') or (inp == 'T'):
        print("Testing Algorithms...")
        data = open("../data/segmentationResults.txt", 'w')
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
