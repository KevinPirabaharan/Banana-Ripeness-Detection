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


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

inputFolder = "../data/"
fileCount = 0

data = open("results_of_Results.txt", 'w')
for file in glob.glob(inputFolder + "*.txt"):
    lists = []
    fileCount += 1
    fname = os.path.basename(file)
    print("")
    avg = 0
    MAX = 0
    MIN = 0
    f = open(file, "r")

    for x in f:
        if (len(x) > 80):
            offset = 87 - len(x)
            # print(x[70-offset:81-offset])
            if (is_number(x[70-offset:81-offset])):
                it = float(x[70-offset:81-offset])
                lists.append(it)
    # print(str(lists) + "\n size is: " + str(len(lists)))
    if(len(lists) > 0):
        avg = sum(lists) / float(len(lists))
        MAX = max(lists)
        MIN = min(lists)
        print(file + ": \t avg = " + str(avg) + "\t Max: " + str(MAX) + "\t Min: " + str(MIN))
        data.write(file + ": \t avg = " + str(avg) + "\t Max: " + str(MAX) + "\t Min: " + str(MIN))

data.close()
