import numpy as np
import cv2
import pytesseract
import time
from imutils.video import VideoStream
from imutils.video import FPS
cam = cv2.VideoCapture(0)
cam.set(4, 480)  # Width=480
cam.set(5, 480)  # Height=480
cam.set(6, 30)  # FrameRate = 30

time.sleep(0.1)
t = 0
t1 = time.time()
while t < 5 and cam.isOpened():
    # Capture frame-by-frame
    ret, frame = cam.read()
    image = np.array(frame)
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    key = cv2.waitKey(1) & 0xFF
    # Display the resulting frame
    cv2.imshow('frame', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if key == ord("s"):
        text = pytesseract.image_to_string(image, lang="vie")
        print(text)
        t2 = time.time()
        t = t2 - t1
        # cv2.imshow("Frame", image)
        cv2.waitKey(0)
        # break

# When everything done, release the capture
cam.release()
cv2.destroyAllWindows()
