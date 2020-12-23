from imutils.video import VideoStream
from imutils.video import FPS
from imutils.object_detection import non_max_suppression
import numpy as np
import argparse
import imutils
import time
import cv2
import pytesseract


# setting up tesseract path

if __name__ == '__main__':
    # vs = cv2.VideoCapture(0)
    fps = FPS().start()
    w, h = None, None
    new_w, new_h = 320, 320
    print("[INFO] starting video stream...")
    vs = VideoStream(src="http://192.168.0.108:8080/video").start()
    time.sleep(1)
    fps = FPS().start()
    while True:
        frame = vs.read()
        if frame is None:
            break

        frame = imutils.resize(frame, width=1000)
        orig = frame.copy()
        orig_h, orig_w = orig.shape[:2]

        if w is None or h is None:
            h, w = frame.shape[:2]
            ratio_w = w / float(new_w)
            ratio_h = h / float(new_h)

        frame = cv2.resize(frame, (new_w, new_h))
        orig = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # orig = cv2.threshold(orig, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        roi = orig
        # recognizing text
        config = '-l eng --oem 1 --psm 7'
        text = pytesseract.image_to_string(roi, config=config)
        print(text)
        fps.update()

        cv2.imshow("Detection", orig)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break


    fps.stop()
    print(f"[INFO] elapsed time {round(fps.elapsed(), 2)}")
    print(f"[INFO] approx. FPS : {round(fps.fps(), 2)}")

    vs.stop()
    cv2.destroyAllWindows()
