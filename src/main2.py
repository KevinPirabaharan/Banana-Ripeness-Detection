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
import cv2
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
def imageSegment(imagePath, imageName, output):
    object = []
    #start timer for the function
    startDT = datetime.datetime.now()
    im = Image.open(imagePath)
    #initialize color channels and size variables
    im = Image.open(imagePath)
    height, width = im.size
    img = cv2.imread(imagePath)
    r, g ,b = imread_colour(imagePath)
    thr = otsu(b)
    imgBlueOtsu = im2bw(b,thr)
    imwrite_gray("BLUE.jpeg", imgBlueOtsu)
    HSV = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    cv2.imwrite('hsv.jpg',HSV)
    red, green, blue = imread_colour('hsv.jpg')
    redB = np.zeros((width,height))
    greenB = np.zeros((width,height))
    blueB = np.zeros((width,height))
    rB = np.zeros((width,height))
    gB = np.zeros((width,height))
    bB = np.zeros((width,height))
    bananaSA = 0

    #find the otsu threshold of the red channel and then binarized LAB image into a black and white image
    #the pixels of the banana should be white (255), whilst the rest of the image should be white (0)
    thr = otsu(red)
    imgRedOtsu = im2bw(red,thr)
    # # imwrite_gray("Red2.jpeg", imgRedOtsu)
    red, green, blue = imread_colour(imagePath)

    #the Black and White image is looked at pixel by pixel
    #the white pixels of the the image are saved as the color of the original image, whilst the rest of the image is saved as black pixels
    #this allows the banana to keep it's color while the rest of the image is blackenes
    for i in range(0, width-1):
        for j in range(0, height-1):
            # avg = (float(red[i,j]) + float(blue[i,j]) + float(green[i,j])) / 3
            if imgRedOtsu[i,j] == 255:
                 redB[i,j] = red[i,j]
                 greenB[i,j] = green[i,j]
                 blueB[i,j] = blue[i,j]
                 bananaSA += 1
            else:
                 redB[i,j] = 255
                 greenB[i,j] = 255
                 blueB[i,j] = 255

            if imgBlueOtsu[i,j] != 255:
                rB[i,j] = red[i,j]
                gB[i,j] = green[i,j]
                bB[i,j] = blue[i,j]
                #bananaSA += 1
            else:
                rB[i,j] = 255
                gB[i,j] = 255
                bB[i,j] = 255

    #image is saved and total time taken, total pixel size are all written to a text file
    #imwrite_colour("../images/processed/" + imageName.rsplit('.', 1)[0] + '.png', redB, greenB, blueB)
    imwrite_colour("../images/processed/" + imageName.rsplit('.', 1)[0] + '.png', rB, gB, bB)
    endDT = datetime.datetime.now()
    currentDT = endDT - startDT
    output.write(imageName + ": \tTime Taken: " + str(currentDT) + "\tBanana Size: " + str(bananaSA) + "\t")
    object.append(bananaSA)
    object.append("../images/processed/" + imageName.rsplit('.', 1)[0] + '.png')
    #Returns the surface area of the banana for BrownSpot Analysis
    print (bananaSA)
    return object

def ColorAnaysis(imagePath):


    pass


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
"""
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

    #Minimum error is used to get the thresholding value
    #what does this minimum error mean?
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

    # 130 threshold to create mask from brown spot mask image
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
"""
def difference(a,b):
    diff = abs(a-b)
    return diff

def brownSpotAnalysis(bananaSize,imagePath):
    im = io.imread(imagePath)
    # original image is converted to lab color space
    lab_color = color.rgb2lab(im)
    brown_spot = 0
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            if difference(lab_color[i, j][0], lab_color[i, j][1]) < 25 and difference(lab_color[i, j][1], lab_color[i, j][2]) < 25: # it is brown spot
                if im[i, j][0] != 255 and im[i, j][1] != 255 and im[i, j][2] != 255:
                    im[i, j][0] = 255
                    im[i, j][1] = 255
                    im[i, j][2] = 255
                    brown_spot += 1

    misc.imsave("../images/brownSpot/brownSpot_" + os.path.basename(imagePath), im)
    print"brown spot " + str((float(brown_spot) / float(bananaSize)) * 100) + " %"
    pass

#Program loop to run the program
inputFolder = "../images/raw/"
data2 = open("../data/testing.txt", 'w')
fileCount = 0
obj = []
progExit = False
while (progExit == False):
    inp = raw_input("\n \nExecute Algorithm on a single (F)ile, Run (T)est Suite, (Q)uit? ")
    if (inp == 'f') or (inp == 'F'):
        print("Make sure the image is inside the \'image/raw/\' folder")
        fileName = raw_input("Enter File Name: ")
        obj = imageSegment(inputFolder + fileName, fileName, data2)
        bananaSize = obj[0]
        print(str(bananaSize))
        brownSpotAnalysis(bananaSize, obj[1]);

    elif (inp == 't') or (inp == 'T'):
        print("Testing Algorithms...")
        data = open("../data/segmentationResults.txt", 'w')
        for file in glob.glob(inputFolder + "*.jpg"):
            fileCount += 1
            print("")
            fname = os.path.basename(file)
            bananaSize = imageSegment(file, obj[1], data)
            brownSpotAnalysis(bananaSize,obj[1])
            loadingBar(fileCount,len(glob.glob(inputFolder + "*.jpg")),2)
        data.close()

    elif (inp == "q") or (inp == "Q"):
        print("Ending Program...")
        progExit = True

    else:
        print("Please check your input")
