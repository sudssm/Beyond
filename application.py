import cv2
import numpy as np
from gestures import gesture
import cv2.cv as cv
import Queue

import re
import actuator
import threading
import pyautogui

import socket, sys

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 800

host = "45.79.152.183"
port = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)

try :
    s.connect((host, port))

    s.setblocking(0)
except :
    print 'Unable to connect to socket'
    sys.exit()
 
def log(message):
    s.send(str(message))
    print message

def getUrl():
    s.send("&")
    url = s.recv(4096)
    print url

def setUrl(url):
    s.send("*" + url)

# Mode can be None or MOUSE
def gestureRecognize():
    global MODE
    cap = cv2.VideoCapture(0)

    gesture_cache = []
    lag = 0

    print "ready"

    while(1):
        lag += 1
        if lag > 10 and len(gesture_cache) > 0:
            # flush the gesture
            g = gesture.lookup(gesture_cache)
            if MODE != "MOUSE":
                log(g)
            if g != None:
                # if g == "long_hold":
                #     MODE = "MOUSE" if MODE == None else None
                #     log("Mouse Mode: " + str(MODE))
                # if g == "short_hold" and MODE == "MOUSE":
                #     log("click")
                #     pyautogui.click()
                if MODE != "MOUSE":
                    thread = threading.Thread(target=actuator.on_gesture_made, args=(g,))
                    thread.daemon = True                            # Daemonize thread
                    thread.start()                                  # Start the execution

            gesture_cache = []
        # Take each frame
        _, frame = cap.read()
        # frame = cv2.imread('led.jpg')
        frame = cv2.flip(frame,1)
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # pink = np.uint8([[[186, 109, 199]]])
        pink = np.uint8([[[221, 136, 200 ]]])

        # define range of pink color in HSV
        hsv_pink = cv2.cvtColor(pink, cv2.COLOR_BGR2HSV)[0][0]

        lower = np.array([hsv_pink[0]-20, 100, 100])
        upper = np.array([hsv_pink[0] + 20, 255, 255])
        
        #define range of white when looking inside? (not currently used)
        lw = np.array([0,0,0], dtype=np.uint8)
        uw = np.array([255,255,50], dtype=np.uint8)
        
        # Threshold the HSV image to get only pink color
        mask = cv2.inRange(hsv, lower, upper)
    # 
        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame,frame, mask= mask)

        contours, hierarchy = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        maxcontour = (0, None)
        for idx, contour in enumerate(contours):
            area = cv2.contourArea(contour) 
            if area > maxcontour[0]:
                maxcontour = (area, contour)
        cv2.imshow('frame',frame)
        # cv2.imshow('mask',mask)
        cv2.imshow('res', res)


        if maxcontour[1] == None or maxcontour[0] < 30:
            continue 
            
        moments = cv2.moments(maxcontour[1])
        centre = (int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00']))
        cv2.circle(mask, centre, 3, (0, 255, 0), -1)
        log(centre)
        gesture_cache.append(centre)
        lag = 0

        if MODE == "MOUSE":
            width = cap.get(3)
            height = cap.get(4)
            pyautogui.moveTo(float(centre[0]) / width * SCREEN_WIDTH, float(centre[1])/ height * SCREEN_HEIGHT)
        
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
def main():
    gestureRecognize()


if __name__ == '__main__':
    MODE = None
    main()