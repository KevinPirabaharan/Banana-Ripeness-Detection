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
    f = open(file, "r")
    for x in f:
        if (len(x) > 90):
            offset = 99 - len(x)
            if (is_number(x[83-offset:88-offset])):
                it = float(x[83-offset:88-offset])
                lists.append(it)
    avg = sum(lists) / float(len(lists))
    MAX = max(lists)
    MIN = min(lists)

    print(file + ": \t avg = " + str(avg) + "\t Max: " + str(MAX) + "\t Min: " + str(MIN))
    f.write(file + ": \t avg = " + str(avg) + "\t Max: " + str(MAX) + "\t Min: " + str(MIN))

data.close()
