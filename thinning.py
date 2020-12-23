import cv2
from matplotlib import pyplot as plt
import numpy as np
img = cv2.imread('ed5abf77a5c35b9d02d2.jpg',0)
kernel = np.ones((5,5),np.uint8)
erosion = cv2.erode(img,kernel,iterations = 1)
cv2.imwrite('thining.jpg', img)