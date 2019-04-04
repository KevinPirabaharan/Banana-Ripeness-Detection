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

inputFolder = "../data/"
fileCount = 0

data = open("results_of_Results.txt", 'w')
for file in glob.glob(inputFolder + "*.txt"):
    fileCount += 1
    fname = os.path.basename(file)
    print("")
    f = open(file, "r")
    for x in f:
        if (len(x) > 80):
            print(x[83:88])

data.close()
