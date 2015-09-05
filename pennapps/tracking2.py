import cv2 
import numpy as np 
import cv2.cv as cv


# cap = cv2.VideoCapture(0)
while(1):
    # _, frame = cap.read()
    frame=cv2.imread('led_crop.jpeg')
    img=cv2.GaussianBlur(frame, (5,5), 0)

    img=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    orange = np.uint8([[[186, 109, 199]]])
    hsv_orange = cv2.cvtColor(orange, cv2.COLOR_BGR2HSV)[0][0]
    lower_pink = np.array([hsv_orange[0]-20, 100, 100])
    upper_pink = np.array([hsv_orange[0] + 80, 255, 255])

    lw = np.array([0,0,0], dtype=np.uint8)
    uw = np.array([10,20,255], dtype=np.uint8)

    # lower=np.array([0, 0, 0],np.uint8)
    # upper=np.array([10, 20, 255],np.uint8)

    black=np.uint8([[[10,10,10]]])
    hsv_black = cv2.cvtColor(black, cv2.COLOR_BGR2HSV)[0][0]


    lower = np.array([0,0,0], dtype=np.uint8)
    upper = np.array([255,255,50], dtype=np.uint8)

    separated=cv2.inRange(img,lower,upper)

    def findCenter(mask): 
        circles = cv2.HoughCircles(mask, cv.CV_HOUGH_GRADIENT, 1, 20, param1=50,\
                param2=50, minRadius=1, maxRadius=0)
        if circles != None:
            circles = np.uint16(np.around(circles))
            if len(circles) > 1: 
                return
            for i in circles[0,:]:
                # draw the outer circle
                cv2.circle(mask,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv2.circle(mask,(i[0],i[1]),2,(0,0,255),3)
                print i[0],i[1]

    #this bit draws a red rectangle around the detected region
    contours,hierarchy=cv2.findContours(separated,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    max_area = 0
    largest_contour = None
    for idx, contour in enumerate(contours):
        area = cv2.contourArea(contour)        
        moment = cv2.moments(contour)
        if moment["m00"] > 500:
            rect = cv2.minAreaRect(contour)
            rect_perim = ((rect[0][0], rect[0][1]), (rect[1][0], rect[1][1]), rect[2])
            box = cv2.cv.BoxPoints(rect_perim)
            box = np.int0(box)
            crop = gray[box[0][0]:box[0][1], box[1][0]:box[1][1]]
            findCenter(crop)
    cv2.imshow('crop', crop)        
    cv2.imshow('frame', frame)
    cv2.imshow('sep', separated)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()