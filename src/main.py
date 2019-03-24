#Banana Ripeness Detection
#Kevin Pirabaharan (0946212), Ena So (), Muhammad Jaffar (911)
#This program creates segments bananas from images and detects brown spots
# on the banana to determine the ripeness of the bananas.
from imageIO import *
from imthr_lib import*
from PIL import Image
import cv2
import datetime

def rgb_to_hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df/mx)*100
    v = mx*100
    return h, s, v

# TODO: Image Segmentation
def imageSegment(imageName):
    red, green, blue = imread_colour(imageName)
    im = Image.open(imageName)
    height, width = im.size
    redB = np.zeros((width,height))
    greenB = np.zeros((width,height))
    blueB = np.zeros((width,height))
    startDT = datetime.datetime.now()
    thr = otsu(blue)
    imgBlueOtsu = im2bw(blue,thr)
    imwrite_gray("Blue.jpeg", imgBlueOtsu)
    bananaSA = 0

    for i in range(0, width-1):
        for j in range(0, height-1):
            if (imgBlueOtsu[i,j] == 0):
                redB[i,j] = red[i,j]
                greenB[i,j] = green[i,j]
                blueB[i,j] = blue[i,j]
                bananaSA += 1
            else:
                redB[i,j] = 0
                greenB[i,j] = 0
                blueB[i,j] = 0

    imwrite_colour("../images/Output.png", redB, greenB, blueB)
    endDT = datetime.datetime.now()
    currentDT = endDT - startDT
    print ("Time Taken: " + str(currentDT))

    #Returns the surface area of the banana for BrownSpot Analysis
    return bananaSA


# TODO: BrownSpot Analysis

fname = "../images/testBanana.jpg"
bananaSize = imageSegment(fname)
