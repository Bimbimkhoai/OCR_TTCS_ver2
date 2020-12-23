from PIL import Image
import cv2
import numpy as np
import sys
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image as im
from scipy.ndimage import interpolation as inter
import scipy.ndimage


def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


if __name__ == '__main__':
    image = cv2.imread('.jpg')
    img = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 15)
    cv2.imwrite('round1.jpg', image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    img = deskew(img)
    img = cv2.medianBlur(img, 1)
    cv2.imwrite('round2.jpg', img)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    cv2.imwrite('round3.jpg', img)
    img = scipy.ndimage.median_filter(img, (1, 1))
    kernel = np.ones((2, 2), np.uint8)
    img = cv2.erode(img, kernel, iterations=1)
    cv2.imwrite('round4.jpg', img)
    img = cv2.medianBlur(img, 1)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    cv2.imwrite('round5.jpg', img)
    img = scipy.ndimage.median_filter(img, (1, 1))
    kernel = np.ones((2, 2), np.uint8)
    cv2.imwrite('round6.jpg', img)
    img = cv2.medianBlur(img, 1)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    cv2.imwrite('round7.jpg', img)
