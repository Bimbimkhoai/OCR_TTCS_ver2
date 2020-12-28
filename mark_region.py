import cv2
from PIL import Image
import matplotlib.pyplot as plt
import pytesseract
import numpy as np


def resize(im):
    scale_percent = 20  # percent of original size
    width = int(im.shape[1] * scale_percent / 100)
    height = int(im.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    im = cv2.resize(im, dim, interpolation=cv2.INTER_AREA)
    return im


def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])


def mark_region(im):
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 30)

    # Dilate to combine adjacent text contours
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 3))
    dilate = cv2.dilate(thresh, kernel, iterations=2)
    erode = cv2.erode(dilate, kernel, iterations=2)
    dilate = cv2.dilate(erode, kernel, iterations=2)
    cv2.imshow("ORIGINAL", dilate)
    cv2.waitKey(0)
    # Find contours, highlight text areas, and extract ROIs
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    line_items_coordinates = []
    for c in cnts:
        area = cv2.contourArea(c)

        x, y, w, h = cv2.boundingRect(c)

        im = cv2.rectangle(im, (x, y), (600, y + h), color=(255, 0, 255), thickness=1)
        line_items_coordinates.append([(x, y), (600, y + h)])

        # if y >= 600 and x <= 1000:
        #     if area > 10000:
        #         print("OK")
        #         im = cv2.rectangle(im, (x, y), (2200, y + h), color=(255, 0, 255), thickness=3)
        #         line_items_coordinates.append([(x, y), (2200, y + h)])
        #
        # if y >= 2400 and x <= 2000:
        #     im = cv2.rectangle(im, (x, y), (2200, y + h), color=(255, 0, 255), thickness=3)
        #     line_items_coordinates.append([(x, y), (2200, y + h)])

    return im, line_items_coordinates


if __name__ == '__main__':
    im = cv2.imread("Page_2.jpg")
    im = resize(im)
    cv2.imshow("im", im)
    # Start Mark
    image, line = mark_region(im)
    ketqua = ""
    cv2.imshow("After Mark", image)
    im = cv2.imread("Page_2.jpg")
    im = resize(im)
    for c in line:
        # cropping image img = image[y0:y1, x0:x1]
        img = im[c[0][1]:c[1][1], c[0][0]:c[1][0]]

        # plt.figure(figsize=(10, 10))

        # convert the image to black and white for better OCR
        ret, thresh1 = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
        # cv2.imshow("tr", img)
        # cv2.waitKey(0)
        # pytesseract image to string to get results
        text = str(pytesseract.image_to_string(img, config='-l eng --psm 6'))
        # text1 = remove_non_ascii(text)

        text = remove_non_ascii(text)
        text = text.strip()
        text = text.replace(" ","")
        # print(text)

        ketqua = text +"\n"+ ketqua
    f = open("ketqua.txt", "w")
    f.write(ketqua)
    print(ketqua)
    cv2.waitKey(0)
