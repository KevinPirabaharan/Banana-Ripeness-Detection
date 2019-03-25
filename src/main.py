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

def loadingBar(count,total,size):
    percent = float(count)/float(total)*100
    sys.stdout.write("\r" + str(int(count)).rjust(3,'0')+"/"+str(int(total)).rjust(3,'0') + ' [' + '='*int(percent/10)*size + ' '*(10-int(percent/10))*size + ']')
# def rgb_to_hsv(r, g, b):
#     r, g, b = r/255.0, g/255.0, b/255.0
#     mx = max(r, g, b)
#     mn = min(r, g, b)
#     df = mx-mn
#     if mx == mn:
#         h = 0
#     elif mx == r:
#         h = (60 * ((g-b)/df) + 360) % 360
#     elif mx == g:
#         h = (60 * ((b-r)/df) + 120) % 360
#     elif mx == b:
#         h = (60 * ((r-g)/df) + 240) % 360
#     if mx == 0:
#         s = 0
#     else:
#         s = (df/mx)*100
#     v = mx*100
#     return h, s, v

# TODO: Image Segmentation
def imageSegment(imagePath, imageName, output):
    red, green, blue = imread_colour(imagePath)
    im = Image.open(imagePath)
    height, width = im.size
    redB = np.zeros((width,height))
    greenB = np.zeros((width,height))
    blueB = np.zeros((width,height))
    startDT = datetime.datetime.now()
    thr = otsu(blue)
    imgBlueOtsu = im2bw(blue,thr)
    # imwrite_gray("Blue.jpeg", imgBlueOtsu)
    bananaSA = 0

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

    imwrite_colour("../images/processed/" + imageName.rsplit('.', 1)[0] + '.png', redB, greenB, blueB)
    endDT = datetime.datetime.now()
    currentDT = endDT - startDT
    output.write(imageName + ": \tTime Taken: " + str(currentDT) + "\tBanana Size: " + str(bananaSA) + "\n\n")

    #Returns the surface area of the banana for BrownSpot Analysis
    return bananaSA

# TODO: BrownSpot Analysis

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
