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
from skimage import io, color
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage import color
from skimage import io
from scipy import ndimage, misc
import matplotlib.cm as cm #
from scipy import misc
import numpy as np
import matplotlib.pyplot as plt # import

banCount = 0.0
brownSpot = 0.0

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
    bananaSA = 0

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
    output.write(imageName + ": \tTime Taken: " + str(currentDT) + "\tBanana Size: " + str(bananaSA) + "\n\n")

    #Returns the surface area of the banana for BrownSpot Analysis
    return bananaSA

# TODO: BrownSpot Analysis
def brownSpotAnalysis(bananaSize,imagePath,imageName):
    im = io.imread(imagePath)

    # original image is converted to lab color space
    lab_color = color.rgb2lab(im);
    #converted to yCbCr color space and gray
    yCbCr_color = cv2.cvtColor(im,cv2.COLOR_BGR2YCR_CB)
    gray = color.rgb2gray(yCbCr_color)

    # save the gray image and read it
    misc.imsave("../images/processed/gray.png",gray);
    gray = misc.imread("../images/processed/gray.png");

    #Minimum error is used to get thethresholding value
    val = minError(gray)
    print "min error threshold value: " + str(val)

    # Masks are created from gray image based on the threshold value
    ret, mask = cv2.threshold(gray, val, 255, cv2.THRESH_BINARY)
    mask2 = cv2.bitwise_not(mask)

    #a mask is created based on the l.a.b color space for brown spots on the banana
    brownSpotMask = np.zeros((im.shape[0], im.shape[1]))
    for rowNum in range(len(lab_color)):
        for colNum in range (len(lab_color[rowNum])):
            if((lab_color[rowNum][colNum][1] < 12 ) and (lab_color[rowNum][colNum][2] > 28) and mask2[rowNum][colNum] !=0):
                brownSpotMask[rowNum][colNum]= 255
            else:
                brownSpotMask[rowNum][colNum] = 0

    misc.imsave("../images/processed/lab.png",lab_color);
    misc.imsave("../images/processed/brownspotmask.png",brownSpotMask);

    browspotmask = misc.imread("../images/processed/brownspotmask.png");

    # 130 threshold to creake mask from brownspot mask image
    ret, mask3 = cv2.threshold(browspotmask, 130, 255, cv2.THRESH_BINARY);
    mask4 = cv2.bitwise_not(mask3)

    banCount = cv2.bitwise_and(mask4,mask4, mask = mask2)
    brownSpot = np.count_nonzero(banCount)
    bananaCount2 = cv2.bitwise_and(mask3,mask3,mask = mask2)
    banana = np.count_nonzero(bananaCount2)

    print "Ripeness Level is: " + str((float(brownSpot)/(banana+brownSpot)) * 100);

    #Union is made of the original image and the mask for viewing
    union = cv2.bitwise_and(im,im,mask = mask2)
    #Images are created with the minimum error union and the lab masks
    brownSpotsIm= cv2.bitwise_and(union,union,mask = mask4)
    bananaIm = cv2.bitwise_and(union,union,mask = mask3)

    # saving images
    # misc.imsave("../images/processed/brownSpotsimage.png",brownSpotsIm);
    misc.imsave("../images/processed/bananaIm.png",bananaIm);



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
        brownSpotAnalysis(bananaSize,inputFolder + fileName,fileName);

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
