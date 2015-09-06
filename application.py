import cv2
import numpy as np
from gestures import gesture
import cv2.cv as cv
import Queue

from subprocess import check_output
import re

# from volume import Volume
def get_volume():
    regex = 'output volume:([0-9]*)'
    a = check_output(["osascript", "-e", "get volume settings"])
    vol = re.search(regex, a).group(1)
    print vol 
    return int(vol) 

def set_volume(volume):
    a = check_output(["osascript", "-e", "set volume output volume %i" % volume])

def gestureRecognize():
    cap = cv2.VideoCapture(0)

    gesture_cache = []
    lag = 0
    while(1):
        lag += 1
        if lag > 10 and len(gesture_cache) > 0:
            # flush the gesture
            g = gesture.lookup(gesture_cache)
            print g 
            if g == "up":
                set_volume(get_volume() + 5)
            elif g == "down":
                set_volume(get_volume() - 5)

            gesture_cache = []
        # Take each frame
        _, frame = cap.read()
        # frame = cv2.imread('led.jpg')
        frame = cv2.flip(frame,1)

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


        pink = np.uint8([[[186, 109, 199]]])
        # define range of pink color in HSV
        hsv_pink = cv2.cvtColor(pink, cv2.COLOR_BGR2HSV)[0][0]

        lower = np.array([hsv_pink[0]-20, 100, 100])
        upper = np.array([hsv_pink[0] + 5, 255, 255])
        
        #define range of white when looking inside? (not currently used)
        lw = np.array([0,0,0], dtype=np.uint8)
        uw = np.array([255,255,50], dtype=np.uint8)
        
        # Threshold the HSV image to get only pink color
        mask = cv2.inRange(hsv, lower, upper)
    # 
        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame,frame, mask= mask)

        centres = []
        contours, hierarchy = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        maxcontour = (0, None)
        for idx, contour in enumerate(contours):
            area = cv2.contourArea(contour) 
            if area > maxcontour[0]:
                maxcontour = (area, contour)
        cv2.imshow('frame',frame)
        cv2.imshow('mask',mask)
        cv2.imshow('res', res)


        if maxcontour[1] == None or maxcontour[0] < 30:
            continue 
            
        moments = cv2.moments(maxcontour[1])
        centres.append((int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00'])))
        cv2.circle(mask, centres[-1], 3, (0, 255, 0), -1)
        print centres[-1]
        gesture_cache.append(centres[-1])
        lag = 0

        
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
def main():
    # v = Volume()
    # v.start()
    gestureRecognize()


if __name__ == '__main__':
    main()