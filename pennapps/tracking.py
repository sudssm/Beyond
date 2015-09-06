import cv2
import numpy as np
from gestures import gesture
import cv2.cv as cv

cap = cv2.VideoCapture(0)

gesture_cache = []
lag = 0
while(1):
    lag += 1
    if lag > 5 and len(gesture_cache) > 0:
        # flush the gesture
        print gesture.lookup(gesture_cache)
        gesture_cache = []
    # Take each frame
    _, frame = cap.read()
    # frame = cv2.imread('led.jpg')
    frame = cv2.flip(frame,1)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    

    # in rgb format orange = np.uint8([[[115, 50, 40]]])
    orange = np.uint8([[[186, 109, 199]]])
    # define range of orange color in HSV
    hsv_orange = cv2.cvtColor(orange, cv2.COLOR_BGR2HSV)[0][0]

    white=np.uint8([[[255,255,255]]])
    hsv_white = cv2.cvtColor(white, cv2.COLOR_BGR2HSV)[0][0]

    lower = np.array([hsv_orange[0]-20, 100, 100])
    upper = np.array([hsv_orange[0] + 20, 255, 255])
    lw = np.array([0,0,0], dtype=np.uint8)
    uw = np.array([10,20,255], dtype=np.uint8)
    
    # Threshold the HSV image to get only specified colors
    mask = cv2.inRange(hsv, lower, upper)
    mask_white = cv2.inRange(hsv, lw, uw)
# 

    # mask = cv2.bitwise_or(mask, mask_white)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)


    centres = []
    contours, hierarchy = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(contours)):
        rect = cv2.minAreaRect(contours[i])
        rect_perim = ((rect[0][0], rect[0][1]), (rect[1][0], rect[1][1]), rect[2])
        box = cv2.cv.BoxPoints(rect_perim)
        import pdb
        pdb.set_trace()
        # cv2.Rectangle(mask, (box[0])
        if cv2.contourArea(contours[i]) < 100:
            continue
        moments = cv2.moments(contours[i])
        if moments['m00'] > 0:
            centres.append((int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00'])))
            cv2.circle(mask, centres[-1], 3, (0, 255, 0), -1)
            print centres[-1]
            gesture_cache.append(centres[-1])
            lag = 0



    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res', res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()