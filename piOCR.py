from imutils.video import VideoStream
from imutils.video import FPS

import imutils
import time

import matplotlib.pyplot as plt
import pytesseract
import numpy as np
import string

import cv2


def resize(im):
    width =  640
    height = 480
    dim = (width, height)
    # resize image
    im = cv2.resize(im, dim, interpolation=cv2.INTER_AREA)
    return im


def remove_non_ascii(text):
    listascii = string.ascii_letters + string.digits
    removed = ''
    for i in text:
        if (i in listascii):
            removed += i

    return removed


def mark_region(im):
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 30)

    # Dilate to combine adjacent text contours
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 3))
    dilate = cv2.dilate(thresh, kernel, iterations=3)
    erode = cv2.erode(dilate, kernel, iterations=3)
    dilate = cv2.dilate(erode, kernel, iterations=2)
    cv2.imshow("ORIGINAL", dilate)
    cv2.waitKey(0)
    # Find contours, highlight text areas, and extract ROIs
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    line_items_coordinates = []
    for c in cnts:
        area = cv2.contourArea(c)
        print(area)
        x, y, w, h = cv2.boundingRect(c)
        print(x, y, w, h)



        if y >= 20 and x <= 640:
            if area > 7000:
                im = cv2.rectangle(im, (x, y), (620, y + h), color=(26, 232, 39), thickness=1)
                line_items_coordinates.append([(x, y), (620, y + h)])

    return im, line_items_coordinates


def skew_correction(image):
    # convert the image to grayscale and flip the foreground
    # and background to ensure foreground is now "white" and
    # the background is "black"
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)

    # threshold the image, setting all foreground pixels to
    # 255 and all background pixels to 0
    thresh = cv2.threshold(gray, 0, 255,
                           cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # grab the (x, y) coordinates of all pixel values that
    # are greater than zero, then use these coordinates to
    # compute a rotated bounding box that contains all
    # coordinates
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    print(cv2.minAreaRect(coords))

    # the `cv2.minAreaRect` function returns values in the
    # range [-90, 0); as the rectangle rotates clockwise the
    # returned angle trends to 0 -- in this special case we
    # need to add 90 degrees to the angle
    if angle < -45:
        angle = -(90 + angle)

    # otherwise, just take the inverse of the angle to make
    # it positive
    else:
        angle = -angle

    # rotate the image to deskew it
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h),
                             flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    # show the output image
    print("[INFO] angle: {:.3f}".format(angle))

    return rotated


if __name__ == '__main__':
    vs = VideoStream(src="http://192.168.137.228:8081/").start()
    time.sleep(1)
    fps = FPS().start()
    ketqua = ""
    while True:
        frame = vs.read()
        if frame is None:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame = imutils.resize(frame, width=1000)
        orig = frame.copy()
        orig_h, orig_w = orig.shape[:2]

        fps.update()
        key = cv2.waitKey(1) & 0xFF
        if key == ord("s"):
            im = orig
            im = resize(im)
            im = skew_correction(im)
            cv2.imshow("im", im)
            # Start Mark
            image, line = mark_region(im)
            cv2.imshow("After Mark", image)
            im = orig
            im = resize(im)
            pagetext = ""
            for c in line:
                # cropping image img = image[y0:y1, x0:x1]
                img = im[c[0][1]:c[1][1], c[0][0]:c[1][0]]

                plt.figure(figsize=(10, 10))

                # convert the image to black and white for better OCR
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # (ret, thresh) = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)
                th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
                                            cv2.THRESH_BINARY, 11, 12)
                # cv2.imshow("tr", th2)
                # cv2.waitKey(0)
                # pytesseract image to string to get results
                text = str(pytesseract.image_to_string(th2, config='-l eng --psm 6'))
                # text1 = remove_non_ascii(text)
                text = remove_non_ascii(text)
                text = text.strip()

                print("====", text, len(text))
                if len(text.strip()) < 16 or len(text.strip()) > 50:
                    continue
                pagetext = text + "\n" + pagetext
            ketqua = ketqua + pagetext

            # print(text)

        f = open("ketqua.txt", "w")
        f.write(ketqua)
        print(ketqua)
        cv2.imshow("Detection", orig)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

    fps.stop()
    print(f"[INFO] elapsed time {round(fps.elapsed(), 2)}")
    print(f"[INFO] approx. FPS : {round(fps.fps(), 2)}")

    vs.stop()
    cv2.destroyAllWindows()
